import json,os,sys
sys.path.append(os.path.dirname(__file__))
import labeler,commands,duplicates,stale_prs

if os.environ.get('GITHUB_EVENT_NAME')=='schedule' or os.environ.get('TERRAFORM_BOT_MODE')=='stale-prs':
    stale_prs.run()
    raise SystemExit(0)

e=json.load(open(os.environ['GITHUB_EVENT_PATH']))
if 'issue' not in e:raise SystemExit(0)
issue=e['issue']
if 'comment' in e:
    commands.run(issue,e['comment'])
else:
    labeler.run(issue)
    if e.get('action')=='opened':duplicates.run(issue)
