#!/usr/bin/env python3
import argparse, socket
p = argparse.ArgumentParser(); p.add_argument('--host', default='10.0.0.2'); p.add_argument('--port', type=int, default=8080); p.add_argument('--message', default='Hello TCP from WSL2')
p.add_argument('--repeat',type=int,default=1,help='repeat message in one connection')
a = p.parse_args()
data = a.message.encode('utf-8')
if len(data) > 1000: p.error('message must be at most 1000 bytes for this demo')
if not 1 <= a.repeat <= 4: p.error('--repeat must be 1..4 for this bounded demo')
data *= a.repeat
with socket.create_connection((a.host,a.port), timeout=5) as s:
    s.sendall(data)
    received = b''
    while len(received) < len(data):
        part = s.recv(len(data)-len(received))
        if not part: raise RuntimeError('connection closed before complete echo')
        received += part
    print('Sent:    ', data.decode('utf-8'))
    print('Received:', received.decode('utf-8'))
    print('Result:  ', 'PASS' if received == data else 'FAIL')
    if received != data: raise SystemExit(1)
