#!/usr/bin/env python3
"""Local stateful fuzzing with replayable packet AND virtual-time actions."""
import argparse
import json
import random
import time
from stack import Stack, packet, parse, SYN, ACK, FIN, RST, PSH
from fuzz import llm_plan

OPS = ('valid', 'bad_seq', 'bad_ack', 'duplicate', 'rst', 'bad_checksum', 'wait')
SRC, DST, PORT = '10.0.0.1', '10.0.0.2', 40000
KEY = (SRC, PORT)


def make(flags, seq, ack, data=b''):
    return packet(SRC, DST, PORT, 8080, seq, ack, flags, data)


def snapshot(flow):
    if flow is None:
        return None
    return (flow.state, flow.snd, flow.una, flow.rcv, flow.queued,
            flow.pending, flow.peer_fin)


def apply_action(stack, action, now):
    """The same executable properties are used during testing and replay."""
    failures = []
    before = snapshot(stack.flows.get(KEY))
    try:
        if action['kind'] == 'tick':
            now[0] += action['seconds']
            replies = stack.tick()
        else:
            replies = stack.handle(bytes.fromhex(action['hex']))
        for reply in replies:
            parse(reply)
        after = snapshot(stack.flows.get(KEY))
        if action.get('operator') in ('bad_seq', 'bad_ack', 'duplicate', 'bad_checksum') and before != after:
            failures.append({'property':'invalid_input_changed_flow'})
        if 'expected_state' in action:
            state = stack.flows[KEY].state if KEY in stack.flows else None
            if state != action['expected_state']:
                failures.append({'property':'unexpected_state', 'actual':state})
    except Exception as exc:
        failures.append({'property':'unhandled_exception', 'exception':repr(exc)})
    for failure in failures:
        failure['operator'] = action.get('operator')
    return failures


def replay_episode(episode):
    if 'actions' not in episode:
        raise ValueError('legacy trace lacks executable actions/properties; regenerate with this version')
    now = [0.0]
    stack = Stack(isn=lambda:1000, clock=lambda:now[0])
    failures = []
    for index, action in enumerate(episode['actions']):
        for failure in apply_action(stack, action, now):
            failures.append(dict(failure, step=index))
    return failures


def run_episode(seed, weights, steps):
    rng = random.Random(seed)
    now = [0.0]
    stack = Stack(isn=lambda:1000, clock=lambda:now[0])
    actions, failures, packets = [], [], []
    last_valid = None

    def execute(action):
        actions.append(action)
        if action['kind'] == 'packet':
            packets.append(action['hex'])
        for failure in apply_action(stack, action, now):
            failures.append(dict(failure, step=len(actions)-1))

    for raw, state in ((make(SYN,100,0),'SYN_RECEIVED'), (make(ACK,101,1001),'ESTABLISHED')):
        execute({'kind':'packet', 'operator':'handshake', 'hex':raw.hex(), 'expected_state':state})
    for _ in range(steps):
        flow = stack.flows.get(KEY)
        if not flow or failures:
            break
        # White-box generator: independent boundary expectations live in unit tests.
        seq, ack = flow.rcv, flow.snd
        op = rng.choices(OPS, weights=[weights[x] for x in OPS])[0]
        if op == 'wait':
            execute({'kind':'tick', 'operator':op, 'seconds':1.1})
            continue
        if op == 'valid':
            flags, data = (ACK | FIN,b'') if rng.randrange(4) == 0 else (ACK | PSH,bytes([65+rng.randrange(26)]))
        elif op == 'bad_seq':
            flags, data, seq = ACK | PSH, b'x', (seq+5) & 0xffffffff
        elif op == 'bad_ack':
            flags, data, ack = ACK | PSH, b'x', (ack+100) & 0xffffffff
        elif op == 'duplicate':
            flags, data, seq = ACK | PSH, b'x', (seq-1) & 0xffffffff
        elif op == 'rst':
            flags, data = RST, b''
        else:
            flags, data = ACK | PSH, b'x'
        raw = bytearray(make(flags,seq,ack,data))
        if op == 'bad_checksum':
            raw[-1] ^= 1
        if op == 'duplicate' and last_valid is not None:
            raw = last_valid
        execute({'kind':'packet', 'operator':op, 'hex':bytes(raw).hex()})
        if op == 'valid':
            last_valid = bytes(raw)
    return {'seed':seed, 'events':sorted(stack.events), 'failures':failures,
            'packets':packets, 'actions':actions,
            'input_packets':len(packets), 'timer_actions':sum(a['kind']=='tick' for a in actions),
            'output_packets':stack.stats['sent']+stack.stats['retransmissions']}


def feedback_weights(weights, events):
    weights = dict(weights)
    if 'established.fin' not in events:
        weights['valid'] = min(10,weights['valid']+2)
    else:
        for op in ('bad_seq','bad_ack','duplicate','bad_checksum','wait'):
            weights[op] = min(10,weights[op]+1)
    return weights


def next_plan(url, model, events, new_events, failure_count, record):
    return llm_plan(url,model,{'events':sorted(events), 'new_events':sorted(new_events),
                    'failures':failure_count,
                    'operators':{'valid':'in-order data or FIN', 'bad_seq':'future sequence number',
                    'bad_ack':'acknowledge unsent data', 'duplicate':'replay last valid packet',
                    'rst':'reset connection', 'bad_checksum':'corrupt TCP checksum',
                    'wait':'advance virtual time 1.1 seconds to exercise retransmission'}},
                    operators=OPS, record=record)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seed',type=int,default=2026)
    p.add_argument('--rounds',type=int,default=5)
    p.add_argument('--episodes',type=int,default=200)
    p.add_argument('--steps',type=int,default=12)
    p.add_argument('--output',default='agent-results.json')
    p.add_argument('--policy',choices=('fixed','feedback','llm'),default=None)
    p.add_argument('--llm-url')
    p.add_argument('--model')
    a = p.parse_args()
    policy = a.policy or ('llm' if a.llm_url else 'feedback')
    if min(a.rounds,a.episodes,a.steps) < 1:
        p.error('rounds, episodes and steps must be positive')
    if bool(a.llm_url) != bool(a.model) or (policy=='llm' and not a.llm_url):
        p.error('LLM mode requires both --llm-url and --model, plus LLM_API_KEY')
    if a.llm_url and policy!='llm':
        p.error('LLM options require --policy llm')
    if policy=='llm' and a.rounds<2:
        p.error('LLM feedback requires at least two rounds')
    weights = {op:1 for op in OPS}
    seen, rounds, failures, plans = set(), [], [], []
    totals = {'input_packets':0, 'output_packets':0, 'timer_actions':0}
    start = time.monotonic()
    planner_error = None
    for round_no in range(a.rounds):
        fresh = set()
        for i in range(a.episodes):
            result = run_episode(a.seed+round_no*a.episodes+i,weights,a.steps)
            fresh.update(result['events'])
            for name in totals:
                totals[name] += result[name]
            if result['failures']:
                failures.append(result)
        new = fresh-seen
        seen.update(fresh)
        rounds.append({'round':round_no+1, 'weights':dict(weights), 'events':sorted(fresh),
                       'new_events':sorted(new), 'cumulative_events':len(seen)})
        if round_no+1 == a.rounds:
            continue
        if policy=='feedback':
            weights = feedback_weights(weights,fresh)
        elif policy=='llm':
            record = {'after_round':round_no+1}
            plans.append(record)
            try:
                weights = next_plan(a.llm_url,a.model,fresh,new,len(failures),record)
            except Exception as exc:
                planner_error = type(exc).__name__
                record['error'] = planner_error
                break
    report = {'schema_version':2, 'seed':a.seed, 'rounds':rounds,
              'episodes_per_round':a.episodes, 'steps_limit':a.steps,
              'planner':{'fixed':'fixed','feedback':'feedback_heuristic','llm':'llm_after_first_round'}[policy],
              'model':a.model if policy=='llm' else None, 'model_calls':plans,
              'planner_error':planner_error, 'status':'error' if planner_error else 'complete',
              'event_catalog':sorted(seen), 'failure_count':len(failures),
              'failures':failures[:20], 'elapsed_seconds':round(time.monotonic()-start,3), **totals}
    with open(a.output,'w',encoding='utf-8') as f:
        json.dump(report,f,indent=2,ensure_ascii=False)
    print(json.dumps({k:v for k,v in report.items() if k not in ('failures','model_calls')},indent=2,ensure_ascii=False))
    if planner_error:
        print('Model call failed; inspect output JSON. No heuristic fallback was substituted.')
    return int(bool(failures) or planner_error is not None)


if __name__=='__main__':
    raise SystemExit(main())
