#!/usr/bin/env python3
"""Deterministic, local packet fuzzing with optional LLM-proposed mutation weights."""
import argparse, json, os, random, time, urllib.request
from stack import Stack, packet, SYN

OPERATORS = ('truncate', 'bitflip', 'length', 'flags', 'checksum', 'random')

def llm_plan(url, model, feedback=None, operators=OPERATORS, record=None):
    key = os.environ.get('LLM_API_KEY')
    if not key: raise ValueError('set LLM_API_KEY in your environment')
    body = {'model': model, 'temperature': 0.2, 'messages': [{'role':'system','content':'You are a TCP fuzz testing planner. Return only JSON mapping exactly these operators to integer weights 1..10: ' + ', '.join(operators) + '. No code.'}, {'role':'user','content':'Choose a test strategy for a small teaching stack. Previous-round summary: ' + json.dumps(feedback or {}, ensure_ascii=False)}]}
    started = time.monotonic()
    request = urllib.request.Request(url, data=json.dumps(body).encode(), headers={'Content-Type':'application/json','Authorization':'Bearer '+key})
    with urllib.request.urlopen(request, timeout=30) as response: obj = json.load(response)
    content = obj['choices'][0]['message']['content']
    if record is not None:
        record.update({'model':model, 'request':body, 'response_content':content,
                       'elapsed_seconds':round(time.monotonic()-started,3)})
    raw = json.loads(content)
    if not isinstance(raw, dict) or set(raw) != set(operators) or any(type(raw[k]) is not int or not 1 <= raw[k] <= 10 for k in operators): raise ValueError('invalid model plan')
    if record is not None: record['weights'] = dict(raw)
    return raw

def mutate(rng, op):
    b = bytearray(packet('10.0.0.1','10.0.0.2', 40000, 8080, 100, 0, SYN))
    if op == 'truncate': b = b[:rng.randrange(len(b))]
    elif op == 'bitflip': b[rng.randrange(len(b))] ^= 1 << rng.randrange(8)
    elif op == 'length': b[2:4] = rng.randrange(65536).to_bytes(2,'big')
    elif op == 'flags':
        # Rebuild the packet so flag combinations reach the state machine with valid checksums.
        b = bytearray(packet('10.0.0.1','10.0.0.2',40000,8080,100,0,rng.randrange(256)))
    elif op == 'checksum': b[rng.choice([10,11,36,37])] ^= 255
    else: b = bytearray(rng.getrandbits(8) for _ in range(rng.randrange(0,100)))
    return bytes(b)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--seed', type=int, default=42); ap.add_argument('--cases', type=int, default=10000); ap.add_argument('--output', default='fuzz-results.json'); ap.add_argument('--llm-url'); ap.add_argument('--model'); a = ap.parse_args()
    if a.cases < 1: ap.error('--cases must be positive')
    if bool(a.llm_url) != bool(a.model): ap.error('--llm-url and --model must be provided together')
    plan = llm_plan(a.llm_url, a.model) if a.llm_url else {k:1 for k in OPERATORS}
    rng = random.Random(a.seed); counts = {k:0 for k in OPERATORS}; crashes = []; start = time.monotonic()
    for i in range(a.cases):
        op = rng.choices(OPERATORS, weights=[plan[k] for k in OPERATORS])[0]; counts[op] += 1
        raw = mutate(rng, op)
        try: Stack().handle(raw)
        except Exception as e: crashes.append({'case':i,'operator':op,'packet_hex':raw.hex(),'exception':repr(e)})
    result = {'seed':a.seed,'cases':a.cases,'planner':'llm' if a.llm_url else 'fixed','weights':plan,'operator_counts':counts,'crashes':crashes,'elapsed_seconds':round(time.monotonic()-start,3)}
    with open(a.output,'w',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False,indent=2)); raise SystemExit(1 if crashes else 0)
if __name__ == '__main__': main()
