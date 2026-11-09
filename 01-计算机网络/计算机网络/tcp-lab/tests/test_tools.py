import contextlib, io, json, os, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from stack import PcapWriter, packet, SYN
from inspect_pcap import inspect
from fuzz import llm_plan, OPERATORS
from experiment import trial

class Response:
    def __init__(self, obj): self.body=json.dumps(obj).encode()
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def read(self): return self.body

class ToolTests(unittest.TestCase):
    def test_pcap_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            path=str(Path(d)/'out.pcap'); w=PcapWriter(path)
            w.write(packet('10.0.0.1','10.0.0.2',1,8080,12,0,SYN)); w.close()
            output=io.StringIO()
            with contextlib.redirect_stdout(output): inspect(path)
            self.assertIn('SYN seq=12',output.getvalue()); self.assertIn('Packets: 1',output.getvalue())
    def test_pcap_truncation_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'bad.pcap'; path.write_bytes(b'bad')
            with self.assertRaises(ValueError): inspect(path)
    def test_llm_response_and_feedback(self):
        weights={name:2 for name in OPERATORS}
        response={'choices':[{'message':{'content':json.dumps(weights)}}]}
        with patch.dict(os.environ,{'LLM_API_KEY':'test'}), patch('urllib.request.urlopen',return_value=Response(response)) as mock:
            self.assertEqual(llm_plan('https://example.invalid','test-model',{'events':['x']}),weights)
            body=json.loads(mock.call_args.args[0].data)
            self.assertIn('events',body['messages'][1]['content'])
    def test_llm_rejects_bad_weights(self):
        response={'choices':[{'message':{'content':json.dumps({x:99 for x in OPERATORS})}}]}
        with patch.dict(os.environ,{'LLM_API_KEY':'test'}), patch('urllib.request.urlopen',return_value=Response(response)):
            with self.assertRaises(ValueError): llm_plan('https://example.invalid','test-model')
    def test_equal_experiment_budget(self):
        a=trial(42,'fixed',2,5,4); b=trial(42,'feedback',2,5,4)
        self.assertEqual((a['episodes'],b['episodes']),(10,10))
        self.assertEqual(a['trajectory'][0]['weights'],b['trajectory'][0]['weights'])

if __name__=='__main__': unittest.main()
