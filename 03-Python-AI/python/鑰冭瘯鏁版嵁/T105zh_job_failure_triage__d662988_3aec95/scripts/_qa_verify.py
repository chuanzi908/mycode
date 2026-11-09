import json
import os

base = r'c:\Users\admin\Desktop\PinchBech题集\PinchBench 类已做任务\2026-5-11\工作空间'
task_dir = os.path.join(base, 'T105zh_job_failure_triage__d662988_3aec95')

with open(os.path.join(task_dir, 'environment/resources/fixtures/scheduler/jobs.json'), encoding='utf-8') as f:
    jobs = json.load(f)
with open(os.path.join(task_dir, 'environment/resources/fixtures/helpdesk/tickets.json'), encoding='utf-8') as f:
    tickets = json.load(f)

print('=' * 60)
print('PHASE 3: INDEPENDENT CALCULATION FROM SOURCE DATA')
print('=' * 60)

# --- JOB FAILURE ANALYSIS ---
print('\n--- JOB FAILURE ANALYSIS ---')
for j in jobs:
    failed_runs = [r for r in j['execution_history'] if r['status'] == 'failed']
    print(f"{j['job_id']} ({j['name']}): last_status={j['last_status']}, "
          f"failed_runs={len(failed_runs)}, enabled={j['enabled']}, "
          f"next_run={j['next_run']}")
    if failed_runs:
        first_failure = min(failed_runs, key=lambda r: r['started_at'])
        print(f'  First failure: {first_failure["started_at"]}')
        for fr in failed_runs:
            err_info = fr.get('error') or fr.get('error_message', 'N/A')
            if isinstance(err_info, dict):
                err_info = err_info.get('code', '') + ': ' + err_info.get('message', '')
            print(f'  {fr["run_id"]}: {fr["started_at"]} -> {fr["status"]} '
                  f'| err={str(err_info)[:80]}')

failed_job_ids = {j['job_id'] for j in jobs if j['last_status'] == 'failed'}
print(f'\nFailed jobs (last_status=failed): {sorted(failed_job_ids)} '
      f'-> count={len(failed_job_ids)}')

# --- TICKET ANALYSIS ---
print('\n--- TICKET ANALYSIS ---')
for t in tickets:
    print(f"{t['ticket_id']}: {t['title'][:60]} | "
          f"category={t['category']} | created={t['created_at']}")

# --- CORRELATION ---
print('\n--- CORRELATION (instruction.md rules: error type + timeline + semantic) ---')
# JOB-003: DB_CONN_TIMEOUT data sync. TK-003 (CRM data not updating, after), TK-007 (dashboard depends on data sync, after)
# JOB-005: OOM weekly report. TK-002 (weekly report not received, after same day), TK-006 (report export fails, same system)
# JOB-007: SMTP unreachable. TK-005 (notifications not received, after)

correlations = {
    'JOB-003': ['TK-003', 'TK-007'],
    'JOB-005': ['TK-002', 'TK-006'],
    'JOB-007': ['TK-005'],
}
all_related = set()
for rel_list in correlations.values():
    all_related.update(rel_list)

all_ticket_ids = {t['ticket_id'] for t in tickets}
unrelated = all_ticket_ids - all_related
print(f'Related: {sorted(all_related)} (count={len(all_related)})')
print(f'Unrelated: {sorted(unrelated)} (count={len(unrelated)})')
assert (all_related | unrelated) == all_ticket_ids, 'MISSING!'

# Timeline verification
print('\n--- TIMELINE VERIFICATION (ticket.created_at >= job.first_failure_time) ---')
for job_id, rel_list in correlations.items():
    job = next(j for j in jobs if j['job_id'] == job_id)
    failed_runs = [r for r in job['execution_history'] if r['status'] == 'failed']
    first_failure = min(failed_runs, key=lambda r: r['started_at'])['started_at']
    print(f'{job_id} first_failure: {first_failure}')
    for tk_id in rel_list:
        tk = next(t for t in tickets if t['ticket_id'] == tk_id)
        after = tk['created_at'] >= first_failure
        print(f'  {tk_id} created_at: {tk["created_at"]} -> '
              f'{"AFTER" if after else "BEFORE"} first failure')

# --- NUMERICAL VALUES ---
print('\n' + '=' * 60)
print('NUMERICAL VALUE VERIFICATION')
print('=' * 60)

job003 = next(j for j in jobs if j['job_id'] == 'JOB-003')
job005 = next(j for j in jobs if j['job_id'] == 'JOB-005')
job007 = next(j for j in jobs if j['job_id'] == 'JOB-007')

def count_failed(job):
    return len([r for r in job['execution_history'] if r['status'] == 'failed'])

def first_failure_time(job):
    failed = [r for r in job['execution_history'] if r['status'] == 'failed']
    return min(failed, key=lambda r: r['started_at'])['started_at']

j003_cnt = count_failed(job003)
j005_cnt = count_failed(job005)
j007_cnt = count_failed(job007)
j003_ff = first_failure_time(job003)
j005_ff = first_failure_time(job005)
j007_ff = first_failure_time(job007)

results = [
    ('JOB-003.failure_count', j003_cnt, '== 3', j003_cnt == 3),
    ('JOB-005.failure_count', j005_cnt, '== 1', j005_cnt == 1),
    ('JOB-007.failure_count', j007_cnt, '== 3', j007_cnt == 3),
    ('JOB-003.first_failure_time', j003_ff,
     "== '2026-05-10T01:30:01Z'", j003_ff == '2026-05-10T01:30:01Z'),
    ('JOB-005.first_failure_time', j005_ff,
     "== '2026-05-05T08:00:00Z'", j005_ff == '2026-05-05T08:00:00Z'),
    ('JOB-007.first_failure_time', j007_ff,
     "== '2026-05-09T18:00:00Z'", j007_ff == '2026-05-09T18:00:00Z'),
    ('total_failed_jobs', len(failed_job_ids), '== 3', len(failed_job_ids) == 3),
    ('total_related_tickets', len(all_related), '== 5', len(all_related) == 5),
    ('total_unrelated_tickets', len(unrelated), '== 5', len(unrelated) == 5),
    ('unrelated_tickets set', sorted(unrelated),
     "== ['TK-001','TK-004','TK-008','TK-009','TK-010']",
     unrelated == {'TK-001', 'TK-004', 'TK-008', 'TK-009', 'TK-010'}),
]

for name, computed, expected, match in results:
    status = 'CORRECT' if match else 'WRONG'
    print(f'{status}: {name} = {computed} ({expected})')

all_correct = all(r[3] for r in results)
print(f'\nAll values correct: {all_correct}')

# Error format check
print('\n--- ERROR FORMAT INCONSISTENCY CHECK ---')
for j in [job003, job005, job007]:
    for fr in [r for r in j['execution_history'] if r['status'] == 'failed']:
        has_obj = 'error' in fr
        has_str = 'error_message' in fr
        print(f"{j['job_id']} {fr['run_id']}: error_object={has_obj}, "
              f"error_message_string={has_str}")

# JOB-010
job010 = next(j for j in jobs if j['job_id'] == 'JOB-010')
print(f"\nJOB-010: enabled={job010['enabled']}, next_run={job010['next_run']}, "
      f"last_status={job010['last_status']}")

# All 10 tickets count
print(f'\nTotal tickets in fixtures: {len(tickets)}')

# instruction.md schema fields count
print(f'Output schema fields per failed_job entry: 9 '
      f'(job_id, job_name, error_summary, first_failure_time, '
      f'failure_count, related_tickets, impact_scope, '
      f'suggested_priority, priority_reason)')
print(f'Output top-level fields: 5 '
      f'(failed_jobs, unrelated_tickets, total_failed_jobs, '
      f'total_related_tickets, total_unrelated_tickets)')

print('\n=== ALL INDEPENDENT CALCULATIONS COMPLETE ===')
