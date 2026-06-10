import github_api as gh
import bot_config
import pr_bot


def labels(pr):
    return [x.get('name') for x in pr.get('labels',[]) if x.get('name')]


def queue_label():
    return bot_config.get('merge_queue.label','merge-queue')


def ready_label():
    return bot_config.get('merge_queue.ready_label','automerge')


def maybe_enqueue(pr,files,risk):
    if not bot_config.enabled('merge_queue.enabled',True):
        return
    num=pr['number']
    current=labels(pr)
    if queue_label() in current:
        return
    high_risk=risk.get('level')=='high'
    if high_risk:
        gh.log('merge-queue','not enqueueing PR #'+str(num)+': high risk')
        return
    gh.ensure_label(queue_label(),description='Eligible for lightweight bot merge queue')
    try:
        gh.add_labels(num,[queue_label()])
        gh.add_comment(num,'## Merge Queue\n\nAdded '+('`'+queue_label()+'`')+' for lightweight queue tracking.\n\n> This is not a full GitHub Merge Queue. Maintainers still control approval and merge policy.\n\n_Handled by ciphertrust-bot._')
    except Exception as e:
        gh.log('merge-queue','failed enqueueing PR #'+str(num)+': '+type(e).__name__+': '+str(e)[:300])


def run():
    if not bot_config.enabled('merge_queue.enabled',True):
        return
    q=queue_label(); ready=ready_label()
    prs=[]
    for pr in gh.list_open_prs():
        labs=labels(pr)
        if q in labs or ready in labs:
            prs.append(pr)
    if not prs:
        gh.log('merge-queue','no queued PRs')
        return
    prs=sorted(prs,key=lambda p:p.get('created_at',''))
    for pr in prs:
        num=pr['number']
        files=gh.pr_files(num)
        ok,reason=pr_bot.auto_merge_decision(pr,files)
        if ok:
            gh.log('merge-queue','PR #'+str(num)+' is merge-eligible: '+reason)
            pr_bot.try_auto_merge(pr,files)
            return
        gh.log('merge-queue','PR #'+str(num)+' blocked: '+reason)
