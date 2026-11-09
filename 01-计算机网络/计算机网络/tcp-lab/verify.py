#!/usr/bin/env python3
"""One offline command: tests, fuzzing, comparison, logs and source hashes."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',default='validation-output')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True,exist_ok=True)
    tasks = [
        ('unit-tests',['-m','unittest','discover','-s','tests','-v']),
        ('single-packet',['fuzz.py','--seed','42','--cases','10000','--output',str(out/'fuzz-results.json')]),
        ('stateful',['agent_fuzz.py','--seed','2026','--rounds','5','--episodes','200','--output',str(out/'agent-results.json')]),
        ('comparison',['experiment.py','--output',str(out/'comparison.json'),'--csv',str(out/'comparison.csv')]),
    ]
    environment = dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
    results = []
    for name, arguments in tasks:
        command = [sys.executable]+arguments
        try:
            completed = subprocess.run(command,cwd=root,env=environment,stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,encoding='utf-8',errors='replace',timeout=120)
            code, log = completed.returncode, completed.stdout
        except subprocess.TimeoutExpired:
            code, log = 124, 'Validation step exceeded 120 seconds.\n'
        (out/(name+'.log')).write_text(log,encoding='utf-8')
        results.append({'name':name,'command':command,'exit_code':code,'log':name+'.log'})
        print(('PASS' if code==0 else 'FAIL')+': '+name)
    sources = list(root.glob('*.py'))+list((root/'tests').glob('*.py'))
    summary = {'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'platform':platform.platform(),'python':sys.version,'checks':results,
               'passed':all(x['exit_code']==0 for x in results),
               'scope':'Offline only. No live Linux TUN or real model calls performed.',
               'sha256':{str(path.relative_to(root)).replace('\\','/'):hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Evidence: '+str(out/'summary.json'))
    return 0 if summary['passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
