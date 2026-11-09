#!/usr/bin/env python3
"""A deliberately small IPv4/TCP endpoint for a Linux TUN device."""
import argparse
try: import fcntl
except ImportError: fcntl = None  # Offline tests also run on Windows.
import ipaddress
import os
import select
import struct
import time
from dataclasses import dataclass

FIN, SYN, RST, PSH, ACK = 1, 2, 4, 8, 16

def checksum(data):
    if len(data) % 2: data += b'\0'
    total = sum(struct.unpack('!%dH' % (len(data) // 2), data))
    while total >> 16: total = (total & 0xffff) + (total >> 16)
    return (~total) & 0xffff

def packet(src, dst, sport, dport, seq, ack, flags, payload=b'', ident=0):
    src, dst = ipaddress.IPv4Address(src).packed, ipaddress.IPv4Address(dst).packed
    tcp = struct.pack('!HHIIBBHHH', sport, dport, seq & 0xffffffff, ack & 0xffffffff, 0x50, flags, 4096, 0, 0) + payload
    pseudo = src + dst + struct.pack('!BBH', 0, 6, len(tcp))
    c = checksum(pseudo + tcp)
    tcp = tcp[:16] + struct.pack('!H', c) + tcp[18:]
    ip = struct.pack('!BBHHHBBH4s4s', 0x45, 0, 20 + len(tcp), ident & 0xffff, 0x4000, 64, 6, 0, src, dst)
    ip = ip[:10] + struct.pack('!H', checksum(ip)) + ip[12:]
    return ip + tcp

def parse(data):
    if len(data) < 20: raise ValueError('short IP header')
    vihl, _, length, _, frag, _, proto, _, src, dst = struct.unpack('!BBHHHBBH4s4s', data[:20])
    ihl = (vihl & 15) * 4
    if vihl >> 4 != 4 or ihl < 20 or ihl > len(data): raise ValueError('invalid IP header')
    if length < ihl + 20 or length > len(data): raise ValueError('invalid IP length')
    if checksum(data[:ihl]): raise ValueError('bad IP checksum')
    if proto != 6 or frag & 0x3fff: raise ValueError('not unfragmented TCP')
    tcp = data[ihl:length]
    sport, dport, seq, ack, off, flags, window, _, _ = struct.unpack('!HHIIBBHHH', tcp[:20])
    hlen = (off >> 4) * 4
    if hlen < 20 or hlen > len(tcp): raise ValueError('invalid TCP header length')
    if checksum(src + dst + struct.pack('!BBH', 0, 6, len(tcp)) + tcp): raise ValueError('bad TCP checksum')
    return dict(src=str(ipaddress.IPv4Address(src)), dst=str(ipaddress.IPv4Address(dst)), sport=sport, dport=dport, seq=seq, ack=ack, flags=flags, payload=tcp[hlen:])

@dataclass
class Flow:
    state: str
    snd: int
    rcv: int
    pending: bytes = b''
    sent_at: float = 0.0
    retries: int = 0
    last_seen: float = 0.0
    una: int = 0
    queued: bytes = b''
    peer_fin: bool = False

class Stack:
    def __init__(self, address='10.0.0.2', port=8080, clock=time.monotonic, isn=None, idle_timeout=120, max_flows=256):
        self.address, self.port, self.clock = address, port, clock
        self.isn = isn or (lambda: int.from_bytes(os.urandom(4), 'big'))
        self.idle_timeout, self.max_flows = idle_timeout, max_flows
        self.flows = {}
        self.stats = {'received': 0, 'rejected': 0, 'sent': 0, 'retransmissions': 0, 'expired': 0}
        self.events = set()

    def emit(self, key, f, flags, payload=b'', track=False):
        peer, peerport = key
        out = packet(self.address, peer, self.port, peerport, f.snd, f.rcv, flags, payload)
        if track:
            f.pending, f.sent_at, f.retries = out, self.clock(), 0
            f.snd = (f.snd + len(payload) + bool(flags & SYN) + bool(flags & FIN)) & 0xffffffff
        self.stats['sent'] += 1
        return out

    def flush(self, key, f):
        """Keep one segment in flight; buffer accepted, in-order echo data."""
        if f.pending:
            return []
        data, f.queued = f.queued[:1000], f.queued[1000:]
        flags = ACK | (PSH if data else 0)
        if f.peer_fin and not f.queued:
            flags |= FIN
            f.state = 'LAST_ACK'
        if data or flags & FIN:
            return [self.emit(key, f, flags, data, track=True)]
        return []

    def handle(self, raw):
        self.stats['received'] += 1
        try: p = parse(raw)
        except (ValueError, struct.error):
            self.stats['rejected'] += 1
            self.events.add('parse.reject')
            return []
        self.events.add('parse.accept')
        if p['dst'] != self.address or p['dport'] != self.port: return []
        key = (p['src'], p['sport'])
        f = self.flows.get(key)
        if p['flags'] & RST:
            if f and p['seq'] == f.rcv:
                self.flows.pop(key, None); self.events.add('flow.reset')
            return []
        if f is None:
            if p['flags'] & SYN and not p['flags'] & (ACK | FIN) and len(self.flows) < self.max_flows:
                f = Flow('SYN_RECEIVED', self.isn(), (p['seq'] + 1) & 0xffffffff, last_seen=self.clock())
                f.una = f.snd
                self.flows[key] = f
                self.events.add('closed.syn_received')
                return [self.emit(key, f, SYN | ACK, track=True)]
            return []
        if f.state == 'SYN_RECEIVED':
            if p['flags'] & SYN and p['seq'] == ((f.rcv - 1) & 0xffffffff): return [f.pending] if f.pending else []
            if p['flags'] & SYN: self.events.add('syn.unexpected'); return []
            if not (p['flags'] & ACK and p['ack'] == f.snd and p['seq'] == f.rcv): return []
            f.state = 'ESTABLISHED'
            self.events.add('syn_received.established')
        if p['seq'] != f.rcv: return [self.emit(key, f, ACK)]
        if not p['flags'] & ACK: return []
        if p['flags'] & SYN:
            self.events.add('syn.unexpected')
            return [self.emit(key, f, ACK)]
        # Modular distance is safe here: at most one small segment is in flight.
        acknowledged = (p['ack'] - f.una) & 0xffffffff
        outstanding = (f.snd - f.una) & 0xffffffff
        if acknowledged > outstanding:
            self.events.add('ack.invalid')
            return [self.emit(key, f, ACK)]
        f.last_seen = self.clock()
        if acknowledged:
            f.una = p['ack']
            if p['ack'] == f.snd:
                f.pending = b''
            elif f.pending:
                old = parse(f.pending)
                consumed = (p['ack'] - old['seq']) & 0xffffffff
                f.pending = packet(self.address, key[0], self.port, key[1],
                                   p['ack'], f.rcv, old['flags'] & ~SYN,
                                   old['payload'][consumed:])
            self.events.add('ack.progress')
        else:
            self.events.add('ack.duplicate')
        if f.state == 'LAST_ACK':
            if p['flags'] & ACK and p['ack'] == f.snd:
                self.flows.pop(key, None); self.events.add('last_ack.closed')
            return []
        if f.state == 'CLOSE_WAIT': return self.flush(key, f)
        if f.state != 'ESTABLISHED': return []
        payload = p['payload']
        if len(f.queued) + len(payload) > 4096:
            self.events.add('buffer.full')
            return [self.emit(key, f, ACK)]
        if payload:
            f.rcv = (f.rcv + len(payload)) & 0xffffffff
            f.queued += payload
            self.events.add('established.data')
        if p['flags'] & FIN:
            f.rcv = (f.rcv + 1) & 0xffffffff
            f.peer_fin = True
            f.state = 'CLOSE_WAIT'
            self.events.add('established.fin')
        out = self.flush(key, f)
        if not out and (payload or p['flags'] & FIN):
            return [self.emit(key, f, ACK)]
        return out

    def tick(self):
        out = []
        for key, f in list(self.flows.items()):
            if self.clock() - f.last_seen >= self.idle_timeout:
                del self.flows[key]; self.stats['expired'] += 1; self.events.add('flow.expired'); continue
            if f.pending and self.clock() - f.sent_at >= 1:
                if f.retries >= 5:
                    del self.flows[key]; self.events.add('retransmit.exhausted'); continue
                out.append(f.pending); f.sent_at = self.clock(); f.retries += 1
                self.stats['retransmissions'] += 1
                self.events.add('timer.retransmit')
        return out

class PcapWriter:
    """Classic pcap file with LINKTYPE_RAW: each record starts with an IP header."""
    def __init__(self, path):
        self.file = open(path, 'wb')
        self.file.write(struct.pack('<IHHIIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 101))
    def write(self, data):
        t = time.time(); sec = int(t); usec = int((t - sec) * 1000000)
        self.file.write(struct.pack('<IIII', sec, usec, len(data), len(data)))
        self.file.write(data); self.file.flush()
    def close(self): self.file.close()

def main():
    p = argparse.ArgumentParser(description='Minimal TUN TCP echo server')
    p.add_argument('--interface', default='tunlab0'); p.add_argument('--address', default='10.0.0.2'); p.add_argument('--port', type=int, default=8080); p.add_argument('--pcap', help='save raw IPv4 packets for Wireshark')
    a = p.parse_args()
    if fcntl is None: p.error('TUN service requires Linux; run offline tests on this platform')
    fd = os.open('/dev/net/tun', os.O_RDWR)
    capture = PcapWriter(a.pcap) if a.pcap else None
    try:
        name = fcntl.ioctl(fd, 0x400454ca, struct.pack('16sH', a.interface.encode(), 0x0001 | 0x1000))[:16].split(b'\0')[0].decode()
        s = Stack(a.address, a.port)
        print(f'TUN {name} ready; TCP echo {a.address}:{a.port}', flush=True)
        while True:
            if select.select([fd], [], [], .2)[0]:
                incoming = os.read(fd, 65535)
                if capture: capture.write(incoming)
                for out in s.handle(incoming):
                    if capture: capture.write(out)
                    os.write(fd, out)
            for out in s.tick():
                if capture: capture.write(out)
                os.write(fd, out)
    except KeyboardInterrupt: print('\nstatistics:', s.stats, flush=True)
    finally:
        if capture: capture.close()
        os.close(fd)

if __name__ == '__main__': main()
