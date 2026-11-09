import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from stack import Stack, packet, parse, SYN, ACK, FIN, PSH
from agent_fuzz import OPS, make, replay_episode, run_episode, main
from fuzz import llm_plan
from experiment import trial

KEY = ('10.0.0.1',40000)


class DeliveryTests(unittest.TestCase):
    def opened(self, isn=1000, client_isn=100):
        self.now = [0.0]
        s = Stack(isn=lambda:isn,clock=lambda:self.now[0])
        s.handle(make(SYN,client_isn,0))
        s.handle(make(ACK,(client_isn+1)&0xffffffff,(isn+1)&0xffffffff))
        return s

    def test_pipeline_preserves_pending_and_drains_in_order(self):
        s = self.opened()
        first = s.handle(make(ACK|PSH,101,1001,b'abc'))[0]
        reply = parse(s.handle(make(ACK|PSH,104,1001,b'def'))[0])
        self.assertEqual((reply['payload'],reply['ack']),(b'',107))
        self.assertEqual(s.flows[KEY].pending,first)
        self.now[0] = 1.1
        self.assertEqual(s.tick(),[first])
        second = parse(s.handle(make(ACK,107,1004))[0])
        self.assertEqual((second['seq'],second['payload']),(1004,b'def'))
        s.handle(make(ACK,107,1007))
        self.assertFalse(s.flows[KEY].pending)

    def test_partial_ack_retransmits_only_unacknowledged_bytes(self):
        s = self.opened()
        s.handle(make(ACK|PSH,101,1001,b'abc'))
        s.handle(make(ACK,104,1002))
        self.now[0] = 1.1
        reply = parse(s.tick()[0])
        self.assertEqual((reply['seq'],reply['payload']),(1002,b'bc'))
        self.assertEqual(s.flows[KEY].una,1002)
        s.handle(make(ACK,104,1004))
        self.assertFalse(s.flows[KEY].pending)

    def test_2700_byte_stream_is_echoed_without_loss(self):
        s = self.opened()
        data = bytes(range(250))*10+b'z'*200
        reply = parse(s.handle(make(ACK|PSH,101,1001,data))[0])
        echoed = reply['payload']
        self.assertEqual(reply['ack'],2801)
        for ack in (2001,3001):
            reply = parse(s.handle(make(ACK,2801,ack))[0])
            echoed += reply['payload']
        self.assertEqual(echoed,data)
        s.handle(make(ACK,2801,3701))
        self.assertFalse(s.flows[KEY].queued)
        self.assertFalse(s.flows[KEY].pending)

    def test_both_sequence_numbers_wrap(self):
        s = self.opened(0xfffffffe,0xfffffffe)
        first = parse(s.handle(make(ACK|PSH,0xffffffff,0xffffffff,b'abc'))[0])
        self.assertEqual(first['ack'],2)
        s.handle(make(ACK|PSH,2,0xffffffff,b'def'))
        second = parse(s.handle(make(ACK,5,2))[0])
        self.assertEqual((second['seq'],second['payload']),(2,b'def'))
        s.handle(make(ACK,5,5))
        self.assertFalse(s.flows[KEY].pending)

    def test_fin_waits_for_queued_echo_and_is_retransmitted(self):
        s = self.opened()
        s.handle(make(ACK|PSH,101,1001,b'abc'))
        s.handle(make(ACK|PSH|FIN,104,1001,b'def'))
        self.assertEqual(s.flows[KEY].state,'CLOSE_WAIT')
        raw = s.handle(make(ACK,108,1004))[0]
        reply = parse(raw)
        self.assertEqual((reply['payload'],reply['ack']),(b'def',108))
        self.assertTrue(reply['flags'] & FIN)
        self.now[0] = 1.1
        self.assertEqual(s.tick(),[raw])
        s.handle(make(ACK,108,1008))
        self.assertFalse(s.flows)

    def test_bounded_queue_does_not_ack_unstored_data(self):
        s = self.opened()
        s.handle(make(ACK|PSH,101,1001,b'abc'))
        s.handle(make(ACK|PSH,104,1001,b'x'*4096))
        reply = parse(s.handle(make(ACK|PSH,4200,1001,b'y'))[0])
        self.assertEqual(reply['ack'],4200)
        self.assertEqual(len(s.flows[KEY].queued),4096)
        self.assertIn('buffer.full',s.events)

    def test_replay_packet_does_not_duplicate_echo(self):
        s = self.opened()
        raw = make(ACK|PSH,101,1001,b'abc')
        original = s.handle(raw)[0]
        reply = parse(s.handle(raw)[0])
        self.assertEqual(reply['payload'],b'')
        self.assertEqual(s.flows[KEY].rcv,104)
        self.assertEqual(s.flows[KEY].pending,original)

    def test_connection_limit_and_bad_handshake_ack(self):
        s = Stack(max_flows=1,isn=lambda:1000)
        s.handle(make(SYN,100,0))
        s.handle(make(ACK,101,1002))
        self.assertEqual(s.flows[KEY].state,'SYN_RECEIVED')
        other = packet('10.0.0.1','10.0.0.2',40001,8080,200,0,SYN)
        self.assertEqual(s.handle(other),[])
        self.assertEqual(len(s.flows),1)

    def test_wait_actions_replay_deterministically(self):
        weights = {op:0 for op in OPS}
        weights['wait'] = 1
        episode = run_episode(42,weights,8)
        self.assertEqual(episode['timer_actions'],8)
        # Waiting with no pending data must not invent a retransmission.
        self.assertNotIn('timer.retransmit',episode['events'])
        self.assertEqual(replay_episode(episode),[])

    def test_replay_rechecks_invariant_with_injected_fault(self):
        damaged = bytearray(make(ACK|PSH,101,1001,b'x'))
        damaged[-1] ^= 1
        episode = {'actions':[
            {'kind':'packet','operator':'handshake','hex':make(SYN,100,0).hex()},
            {'kind':'packet','operator':'handshake','hex':make(ACK,101,1001).hex()},
            {'kind':'packet','operator':'bad_checksum','hex':damaged.hex()}]}
        original = Stack.handle
        def faulty(stack, raw):
            out = original(stack,raw)
            if raw == bytes(damaged):
                stack.flows[KEY].rcv += 1
            return out
        with patch.object(Stack,'handle',faulty):
            failures = replay_episode(episode)
        self.assertEqual(failures[0]['property'],'invalid_input_changed_flow')
        self.assertEqual(failures[0]['step'],2)
        self.assertEqual(replay_episode(episode),[])

    def test_stateful_model_uses_actual_operator_names(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self):
                return json.dumps({'choices':[{'message':{'content':json.dumps({op:2 for op in OPS})}}]}).encode()
        record = {}
        with patch.dict(os.environ,{'LLM_API_KEY':'test'}), patch('urllib.request.urlopen',return_value=Response()):
            result = llm_plan('https://example.invalid','test',operators=OPS,record=record)
        self.assertEqual(set(result),set(OPS))
        self.assertIn('wait',record['request']['messages'][0]['content'])
        self.assertNotIn('Authorization',json.dumps(record))

    def test_model_error_saves_partial_result_without_fake_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory)/'result.json')
            argv = ['agent_fuzz.py','--rounds','2','--episodes','2','--policy','llm',
                    '--llm-url','https://example.invalid','--model','test','--output',path]
            with patch.object(sys,'argv',argv), patch('agent_fuzz.next_plan',side_effect=ValueError('invalid plan')), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(),1)
            report = json.loads(Path(path).read_text(encoding='utf-8'))
            self.assertEqual(report['status'],'error')
            self.assertEqual(len(report['rounds']),1)
            self.assertNotEqual(report['planner'],'feedback_heuristic')

    def test_model_comparison_uses_plan_and_marks_incomplete_trials(self):
        proposal = {op:2 for op in OPS}
        with patch('experiment.next_plan',return_value=proposal) as planner:
            result = trial(42,'llm',2,3,4,'https://example.invalid','test')
        self.assertEqual(planner.call_count,1)
        self.assertEqual(result['status'],'complete')
        self.assertEqual(result['trajectory'][1]['weights'],proposal)
        self.assertEqual(result['episodes'],6)
        with patch('experiment.next_plan',side_effect=ValueError('invalid plan')):
            failed = trial(42,'llm',2,3,4,'https://example.invalid','test')
        self.assertEqual(failed['status'],'error')
        self.assertEqual(failed['episodes'],3)
