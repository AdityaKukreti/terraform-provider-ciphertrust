import json,os,sys
sys.path.append(os.path.dirname(__file__))
import labeler,commands,duplicates,stale_prs,pr_bot,dashboard,merge_queue

mode=os.environ.get('TERRAFORM_BOT_MODE','')
if mode=='dashboard':
    dashboard.run()
    raise SystemExit(0)
if mode=='merge-queue':
    merge_queue.run()
    raise SystemExit(0)
if os.environ.get('GITHUB_EVENT_NAME')=='schedule' or mode=='stale-prs':
    stale_prs.run()
    merge_queue.run()
    dashboard.run()
    raise SystemExit(0)

e=json.load(open(os.environ['GITHUB_EVENT_PATH']))
if 'pull_request' in e:
    pr_bot.run(e['pull_request'],e.get('action',''))
    raise SystemExit(0)
if 'issue' not in e:raise SystemExit(0)
issue=e['issue']
if 'comment' in e:
    commands.run(issue,e['comment'])
else:
    labeler.run(issue)
    if e.get('action')=='opened':duplicates.run(issue)
