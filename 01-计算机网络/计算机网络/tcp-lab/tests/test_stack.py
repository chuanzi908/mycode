import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stack import Stack, packet, parse, SYN, ACK, FIN, PSH

class StackTests(unittest.TestCase):
    def setUp(self): self.stack = Stack(); self.seq = 100
    def client(self, flags, seq, ack=0, data=b''):
        return packet('10.0.0.1','10.0.0.2',40000,8080,seq,ack,flags,data)
    def handshake(self):
        synack = parse(self.stack.handle(self.client(SYN,100))[0])
        self.assertEqual(synack['flags'], SYN | ACK)
        self.assertEqual(synack['ack'],101)
        server_seq = (synack['seq']+1)&0xffffffff
        self.assertEqual(self.stack.handle(self.client(ACK,101,server_seq)),[])
        return server_seq
    def test_handshake_echo_close(self):
        seq = self.handshake()
        response = parse(self.stack.handle(self.client(ACK | PSH,101,seq,b'hello'))[0])
        self.assertEqual((response['payload'],response['ack']), (b'hello',106))
        seq = (seq+5)&0xffffffff
        fin = parse(self.stack.handle(self.client(FIN | ACK,106,seq))[0])
        self.assertEqual(fin['flags'],FIN | ACK)
        self.stack.handle(self.client(ACK,107,(seq+1)&0xffffffff))
        self.assertFalse(self.stack.flows)
    def test_bad_checksum_dropped(self):
        data = bytearray(self.client(SYN,100)); data[-1] ^= 1
        self.assertEqual(self.stack.handle(data),[])
        self.assertEqual(self.stack.stats['rejected'],1)
    def test_out_of_order_ack(self):
        seq = self.handshake()
        reply = parse(self.stack.handle(self.client(ACK | PSH,110,seq,b'x'))[0])
        self.assertEqual(reply['ack'],101)
    def test_retransmit_and_expiry(self):
        now = [0.]; stack = Stack(clock=lambda:now[0]); original = stack.handle(self.client(SYN,100))[0]
        for i in range(1,6):
            now[0]=i; self.assertEqual(stack.tick(),[original])
        now[0]=6; self.assertEqual(stack.tick(),[]); self.assertFalse(stack.flows)
    def test_truncated_packets(self):
        raw=self.client(SYN,100)
        for n in range(len(raw)): self.assertEqual(self.stack.handle(raw[:n]),[])
    def test_data_and_fin_together(self):
        seq = self.handshake()
        response = parse(self.stack.handle(self.client(ACK | PSH | FIN,101,seq,b'abc'))[0])
        self.assertEqual(response['ack'],105)
        self.assertEqual(response['payload'],b'abc')
        self.assertTrue(response['flags'] & FIN)
        self.stack.handle(self.client(ACK,105,(seq+4)&0xffffffff))
        self.assertFalse(self.stack.flows)
    def test_invalid_ack_does_not_advance(self):
        seq = self.handshake()
        self.stack.handle(self.client(ACK | PSH,101,seq+1,b'abc'))
        self.assertEqual(self.stack.flows[('10.0.0.1',40000)].rcv,101)
    def test_out_of_window_reset_ignored(self):
        self.handshake()
        from stack import RST
        self.stack.handle(self.client(RST,999))
        self.assertTrue(self.stack.flows)
    def test_idle_flow_expiry(self):
        now = [0.]; stack = Stack(clock=lambda:now[0], idle_timeout=5)
        stack.handle(self.client(SYN,100)); now[0]=5; stack.tick()
        self.assertFalse(stack.flows)

if __name__ == '__main__': unittest.main()
