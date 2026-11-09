#!/usr/bin/env python3
"""Replay saved packet/time actions and re-evaluate their original properties."""
import argparse
import json
from agent_fuzz import replay_episode


def main():
    p = argparse.ArgumentParser()
    p.add_argument('result')
    p.add_argument('--index',type=int,default=0)
    a = p.parse_args()
    with open(a.result,encoding='utf-8') as f:
        report = json.load(f)
    episodes = report.get('failures',[])
    if not 0 <= a.index < len(episodes):
        p.error('failure index does not exist; a zero-failure report has nothing to replay')
    episode = episodes[a.index]
    try:
        actual = replay_episode(episode)
    except ValueError as exc:
        p.error(str(exc))
    expected = {(f['step'],f['property']) for f in episode['failures']}
    observed = {(f['step'],f['property']) for f in actual}
    reproduced = bool(expected) and expected <= observed
    print(json.dumps({'reproduced':reproduced,'expected':episode['failures'],
                      'observed':actual},ensure_ascii=False,indent=2))
    return 0 if reproduced else 1


if __name__=='__main__':
    raise SystemExit(main())
