import json,os,sys
sys.path.append(os.path.dirname(__file__))
import labeler,commands

e=json.load(open(os.environ['GITHUB_EVENT_PATH']))
if 'issue' not in e:raise SystemExit(0)
issue=e['issue']
if 'comment' in e:
    commands.run(issue,e['comment'].get('body','').strip())
else:
    labeler.run(issue)
