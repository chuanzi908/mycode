#!/usr/bin/env python3
"""Run reproducible, equal-budget fixed-vs-feedback stateful experiments."""
import argparse, csv, json, statistics, time
from agent_fuzz import OPS, run_episode, feedback_weights, next_plan

def trial(seed, policy, rounds, episodes, steps, llm_url=None, model=None):
    weights = {op:1 for op in OPS}; seen = set(); first = {}; errors = 0
    counts = 0; start = time.monotonic(); trajectory = []; model_calls = []
    totals = {'input_packets':0,'output_packets':0,'timer_actions':0}
    planner_error = None
    for round_no in range(rounds):
        current = set()
        for i in range(episodes):
            result = run_episode(seed + round_no * episodes + i, weights, steps)
            counts += 1; errors += len(result['failures'])
            for name in totals: totals[name] += result[name]
            for event in result['events']:
                first.setdefault(event, counts); current.add(event)
        new = current - seen; seen.update(current)
        trajectory.append({'round':round_no + 1,'weights':dict(weights),'new_events':sorted(new),'event_count':len(seen)})
        if round_no+1 < rounds:
            if policy == 'feedback': weights = feedback_weights(weights,current)
            elif policy == 'llm':
                record = {'after_round':round_no+1}; model_calls.append(record)
                try: weights = next_plan(llm_url,model,current,new,errors,record)
                except Exception as exc:
                    planner_error = type(exc).__name__; record['error'] = planner_error; break
    return {'seed':seed,'policy':policy,'episodes':counts,'steps_limit':steps,'events':sorted(seen),'first_seen_episode':first,'failure_count':errors,'elapsed_seconds':round(time.monotonic()-start,4),'trajectory':trajectory, 'model_calls':model_calls, 'planner_error':planner_error, 'status':'error' if planner_error else 'complete', **totals}

def main():
    p = argparse.ArgumentParser(); p.add_argument('--seeds',default='10000,20000,30000,40000,50000'); p.add_argument('--rounds',type=int,default=5); p.add_argument('--episodes',type=int,default=200); p.add_argument('--steps',type=int,default=12); p.add_argument('--output',default='comparison.json'); p.add_argument('--csv',default='comparison.csv')
    p.add_argument('--llm-url'); p.add_argument('--model'); a=p.parse_args()
    if bool(a.llm_url) != bool(a.model): p.error('supply both --llm-url and --model')
    if a.llm_url and a.rounds<2: p.error('LLM feedback requires at least two rounds')
    try: seeds=[int(s) for s in a.seeds.split(',')]
    except ValueError: p.error('--seeds must be comma-separated integers')
    if len(set(seeds)) != len(seeds) or min(a.rounds,a.episodes,a.steps)<1: p.error('seeds must be unique and budgets positive')
    if any(abs(x-y) < a.rounds*a.episodes for i,x in enumerate(seeds) for y in seeds[i+1:]): p.error('seed ranges overlap for this episode budget')
    policies = ('fixed','feedback','llm') if a.llm_url else ('fixed','feedback')
    trials=[trial(seed,policy,a.rounds,a.episodes,a.steps,a.llm_url,a.model) for seed in seeds for policy in policies]
    summaries={}
    for policy in policies:
        all_runs=[x for x in trials if x['policy']==policy]
        t=[x for x in all_runs if x['status']=='complete']
        summaries[policy]={'runs':len(t),'incomplete_runs':len(all_runs)-len(t),
                          'mean_observed_events':statistics.mean(len(x['events']) for x in t) if t else None,
                          'total_failures':sum(x['failure_count'] for x in t),
                          'mean_input_packets':statistics.mean(x['input_packets'] for x in t) if t else None,
                          'mean_seconds':round(statistics.mean(x['elapsed_seconds'] for x in t),4) if t else None}
    out={'description':'Equal episode/step limits; actual packet counts may differ. Events are manually instrumented, not code coverage. Same seed does not imply identical inputs once policies diverge. Incomplete model trials are excluded from summaries.','model':a.model,'rounds':a.rounds,'episodes_per_round':a.episodes,'seeds':seeds,'summary':summaries,'trials':trials}
    with open(a.output,'w',encoding='utf-8') as f: json.dump(out,f,ensure_ascii=False,indent=2)
    with open(a.csv,'w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['seed','policy','status','episodes','input_packets','output_packets','timer_actions','observed_events','failures','elapsed_seconds']); writer.writeheader()
        for t in trials: writer.writerow({'seed':t['seed'],'policy':t['policy'],'status':t['status'],'episodes':t['episodes'],'input_packets':t['input_packets'],'output_packets':t['output_packets'],'timer_actions':t['timer_actions'],'observed_events':len(t['events']),'failures':t['failure_count'],'elapsed_seconds':t['elapsed_seconds']})
    print(json.dumps(summaries,ensure_ascii=False,indent=2))
    return int(any(t['planner_error'] or t['failure_count'] for t in trials))
if __name__=='__main__': raise SystemExit(main())
