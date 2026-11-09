#!/usr/bin/env python3
"""Run real TUN/socket integration in a temporary Linux network namespace.

Requires root and permission to create network namespaces and TUN devices.
Only the uniquely named namespace created by this process is removed.
"""
import argparse, json, os, pathlib, signal, subprocess, sys, time, uuid

def cmd(*args, check=True):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check, timeout=15)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',default='integration-output'); a=ap.parse_args()
    if sys.platform != 'linux' or os.geteuid()!=0: ap.error('requires Linux and root (sudo)')
    here=pathlib.Path(__file__).resolve().parent; out=pathlib.Path(a.output_dir).resolve(); out.mkdir(parents=True,exist_ok=True)
    ns='tcplab-'+uuid.uuid4().hex[:10]; created=False; server=None; checks=[]
    logpath=out/'server.log'; pcap=out/'traffic.pcap'; result=out/'integration.json'
    try:
        cmd('ip','netns','add',ns); created=True
        cmd('ip','-n',ns,'link','set','lo','up')
        with open(logpath,'w',encoding='utf-8') as log:
            server=subprocess.Popen(['ip','netns','exec',ns,sys.executable,str(here/'stack.py'),'--pcap',str(pcap)],stdout=log,stderr=subprocess.STDOUT)
            ready=False
            for _ in range(100):
                if server.poll() is not None: raise RuntimeError('server exited; inspect server.log')
                if cmd('ip','-n',ns,'link','show','tunlab0',check=False).returncode==0: ready=True; break
                time.sleep(.05)
            if not ready: raise RuntimeError('TUN interface not ready; inspect server.log')
            cmd('ip','-n',ns,'addr','add','10.0.0.1/24','dev','tunlab0')
            cmd('ip','-n',ns,'link','set','tunlab0','up')
            for message in ('hello tcp', 'second connection', 'network test 123'):
                completed=cmd('ip','netns','exec',ns,sys.executable,str(here/'client.py'),'--message',message)
                ok='Result:   PASS' in completed.stdout
                checks.append({'message':message,'stdout':completed.stdout,'passed':ok})
                if not ok: raise RuntimeError('client output did not report PASS')
            completed=cmd('ip','netns','exec',ns,sys.executable,str(here/'client.py'),'--message','x'*900,'--repeat','3')
            ok='Result:   PASS' in completed.stdout
            checks.append({'message':'2700-byte stream (900 bytes repeated 3 times)','stdout':completed.stdout,'passed':ok})
            if not ok: raise RuntimeError('multi-segment stream did not report PASS')
            print('PASS: 4 real TCP echo connections, including a 2700-byte stream')
    except Exception as exc:
        detail = str(exc) + ('\n' + exc.stdout if isinstance(exc,subprocess.CalledProcessError) and exc.stdout else '')
        checks.append({'error':detail,'passed':False}); print('FAIL:',detail, file=sys.stderr)
    finally:
        if server and server.poll() is None:
            server.send_signal(signal.SIGINT)
            try: server.wait(timeout=5)
            except subprocess.TimeoutExpired: server.kill(); server.wait()
        cleanup=None
        if created:
            deleted=cmd('ip','netns','delete',ns,check=False); cleanup={'success':deleted.returncode==0,'output':deleted.stdout}
        summary={'environment':{'platform':sys.platform,'python':sys.version.split()[0]},'namespace':ns,'checks':checks,'cleanup':cleanup,'server_log':str(logpath),'pcap':str(pcap)}
        with open(result,'w',encoding='utf-8') as f: json.dump(summary,f,ensure_ascii=False,indent=2)
        print('Evidence:',result)
    if len(checks)!=4 or not all(x.get('passed') for x in checks) or not cleanup or not cleanup['success']: return 1
    return 0
if __name__=='__main__': sys.exit(main())
