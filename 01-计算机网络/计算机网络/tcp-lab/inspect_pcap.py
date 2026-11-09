#!/usr/bin/env python3
"""Inspect packet captures produced by stack.py --pcap without external packages."""
import argparse, struct
from stack import parse, FIN, SYN, RST, PSH, ACK
def flags(value): return '|'.join(name for bit,name in ((SYN,'SYN'),(ACK,'ACK'),(PSH,'PSH'),(FIN,'FIN'),(RST,'RST')) if value & bit) or '-'
def inspect(path):
    with open(path,'rb') as f:
        header=f.read(24)
        if len(header)!=24: raise ValueError('truncated pcap header')
        magic,major,minor,_,_,snaplen,link=struct.unpack('<IHHIIII',header)
        if (magic,major,minor,link)!=(0xa1b2c3d4,2,4,101): raise ValueError('expected little-endian pcap with LINKTYPE_RAW')
        index=0
        while True:
            rec=f.read(16)
            if not rec: break
            if len(rec)!=16: raise ValueError('truncated record header')
            sec,usec,n,orig=struct.unpack('<IIII',rec)
            if n>snaplen or n>orig: raise ValueError('invalid packet length')
            raw=f.read(n)
            if len(raw)!=n: raise ValueError('truncated packet')
            index+=1
            try:
                p=parse(raw)
                print(f"{index:04d} {sec}.{usec:06d} {p['src']}:{p['sport']} -> {p['dst']}:{p['dport']} {flags(p['flags'])} seq={p['seq']} ack={p['ack']} bytes={len(p['payload'])}")
            except ValueError as e: print(f'{index:04d} invalid packet: {e}')
        print(f'Packets: {index}')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('path'); a=ap.parse_args(); inspect(a.path)
if __name__=='__main__': main()
