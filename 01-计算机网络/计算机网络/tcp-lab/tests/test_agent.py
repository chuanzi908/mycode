import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent_fuzz import run_episode, OPS

class AgentTests(unittest.TestCase):
    def test_reproducible_episode(self):
        weights = {op:1 for op in OPS}
        a, b = run_episode(123,weights,20), run_episode(123,weights,20)
        self.assertEqual(a,b)
        self.assertIn('syn_received.established',a['events'])
        self.assertEqual(a['failures'],[])

if __name__ == '__main__': unittest.main()
