import os
from datetime import datetime, timezone, timedelta
import github_api as gh


def parse_time(value):
    if not value:return None
    return datetime.fromisoformat(value.replace('Z','+00:00'))


def age(item):
    t=parse_time(item.get('updated_at'))
    if not t:return timedelta(0)
    return datetime.now(timezone.utc)-t


def days(name,default):
    try:return int(os.getenv(name,default))
    except Exception:return int(default)


def minutes(name):
    v=os.getenv(name)
    if not v:return None
    try:return int(v)
    except Exception:return None


def label_names(item):
    return [l.get('name') for l in item.get('labels',[]) if l.get('name')]


def _warn(number,label,grace_period):
    try:
        gh.add_labels(number,[label])
    except Exception as e:
        gh.log('stale','failed adding '+label+' to #'+str(number)+': '+str(e)[:200])
        return
    try:
        gh.add_comment(number,
            'This item has been inactive. It will be closed if there is no activity within '
            +grace_period+'.\n\n'
            'To keep it open: remove the `'+label+'` label. '
            'Add the `no-stale` label to exempt it permanently.'
            '\n\n_Handled by ciphertrust-bot._')
    except Exception as e:
        gh.log('stale','failed warning on #'+str(number)+': '+str(e)[:200])


def _close(number,closer):
    try:
        gh.add_comment(number,'Closing as stale after inactivity.\n\n_Handled by ciphertrust-bot._')
    except Exception as e:
        gh.log('stale','failed commenting on #'+str(number)+': '+str(e)[:200])
    try:
        closer(number)
    except Exception as e:
        gh.log('stale','failed closing #'+str(number)+': '+str(e)[:200])


# Slack to absorb the bot's own warn comment/label events when judging whether a
# human (or a push) touched the item after we warned. The warn label + comment are
# written seconds apart in one run, so anything beyond this margin is real activity.
ACTIVITY_MARGIN=timedelta(minutes=2)


def _label_added_at(item,label):
    """Datetime the stale label was most recently added, or None if we can't tell."""
    try:
        last=None
        for e in gh.issue_events(item['number']):
            if e.get('event')=='labeled' and (e.get('label') or {}).get('name')==label:
                t=parse_time(e.get('created_at'))
                if t and (last is None or t>last):
                    last=t
        return last
    except Exception:
        return None


def _process_stale(item,label,exempt,threshold,grace,grace_period,closer):
    lnames=label_names(item)
    if exempt in lnames:
        return
    if label not in lnames:
        # Phase 1: first time going stale — warn only, never close in the same run.
        if age(item)>=threshold:
            _warn(item['number'],label,grace_period)
        return
    # Phase 2: already warned in a prior run.
    labeled_at=_label_added_at(item,label)
    if labeled_at is None:
        # Can't tell when we warned — be conservative and don't close.
        return
    last_update=parse_time(item.get('updated_at'))
    if last_update and last_update>labeled_at+ACTIVITY_MARGIN:
        # Someone replied, edited, or pushed after the warning — treat as revived
        # and drop the stale label so the cycle restarts instead of closing.
        try:
            gh.remove_label(item['number'],label)
            gh.log('stale','reset stale on #'+str(item['number'])+' — activity after warning')
        except Exception as e:
            gh.log('stale','failed resetting stale on #'+str(item['number'])+': '+str(e)[:200])
        return
    if datetime.now(timezone.utc)-labeled_at>=grace:
        _close(item['number'],closer)


def close_stale_prs():
    m=minutes('STALE_PR_MINUTES')
    threshold=timedelta(minutes=m) if m is not None else timedelta(days=days('STALE_PR_DAYS',30))
    grace_days_val=days('STALE_GRACE_DAYS',7)
    if m is not None:
        gm=minutes('STALE_GRACE_MINUTES')
        grace=timedelta(minutes=gm) if gm is not None else timedelta(days=grace_days_val)
        grace_period=(str(gm)+' minutes') if gm is not None else (str(grace_days_val)+' days')
    else:
        grace=timedelta(days=grace_days_val)
        grace_period=str(grace_days_val)+' days'
    label=os.getenv('STALE_PR_LABEL','stale')
    exempt=os.getenv('STALE_EXEMPT_LABEL','no-stale')
    gh.ensure_label(label)
    for pr in gh.list_open_prs():
        _process_stale(pr,label,exempt,threshold,grace,grace_period,gh.close_pr)


def close_stale_issues():
    threshold=timedelta(days=days('STALE_ISSUE_DAYS',60))
    grace_days_val=days('STALE_GRACE_DAYS',7)
    grace=timedelta(days=grace_days_val)
    label=os.getenv('STALE_ISSUE_LABEL','stale')
    exempt=os.getenv('STALE_EXEMPT_LABEL','no-stale')
    gh.ensure_label(label)
    for issue in gh.list_open_issues():
        _process_stale(issue,label,exempt,threshold,grace,str(grace_days_val)+' days',gh.close_issue)


def run():
    close_stale_prs()
    close_stale_issues()
