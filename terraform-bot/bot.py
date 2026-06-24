import json
import os
import sys

sys.path.append(os.path.dirname(__file__))

import labeler
import commands
import duplicates
import stale_prs
import pr_bot
import dashboard


def main():
    mode=os.environ.get('TERRAFORM_BOT_MODE','')
    if mode=='dashboard':
        dashboard.run(); return
    if os.environ.get('GITHUB_EVENT_NAME')=='schedule' or mode=='stale-prs':
        # Refresh the dashboard first so it is guaranteed to carry the no-stale
        # label before the stale scan runs over the open-issue list.
        dashboard.run(); stale_prs.run(); return

    with open(os.environ['GITHUB_EVENT_PATH'],'r',encoding='utf-8') as f:
        e=json.load(f)

    if 'pull_request' in e:
        pr_bot.run(e['pull_request'],e.get('action',''))
        return

    if 'issue' not in e:
        return

    issue=e['issue']
    if 'comment' in e:
        commands.run(issue,e['comment'])
    else:
        labeler.run(issue)


if __name__=='__main__':
    main()
