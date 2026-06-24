import re
import github_api as gh
import bot_config

BOT_MARKER_PREFIX='<!-- ciphertrust-bot:'
_comment_cache={}


def marker(key):
    return BOT_MARKER_PREFIX+str(key)+' -->'


def _get_comments(issue_number):
    if issue_number not in _comment_cache:
        _comment_cache[issue_number]=gh.issue_comments(issue_number)
    return _comment_cache[issue_number]


def strip_code_and_quotes(body):
    body=body or ''
    body=re.sub(r'```[^\n]*\n.*?```','',body,flags=re.S)
    # Drop inline `code` spans too, so example commands shown in the bot's own
    # help/label-check output (and in tables) are never parsed as real commands.
    body=re.sub(r'`[^`\n]*`','',body)
    lines=[]
    for line in body.splitlines():
        if line.lstrip().startswith('>'):
            continue
        lines.append(line)
    return '\n'.join(lines)


def find_existing_comment(issue_number,key):
    m=marker(key)
    for c in _get_comments(issue_number):
        if m in (c.get('body') or ''):
            return c
    return None


def upsert(issue_number,key,body):
    full=marker(key)+'\n'+body
    return gh.add_comment(issue_number,full)


def repost(issue_number,key,body):
    """Delete any existing comment(s) for this key, then post a fresh one.

    Used for on-demand informational commands (help/features) so each invocation
    surfaces a visible reply at the bottom of the thread rather than an invisible
    in-place edit of an older comment. Other comment types keep upsert's
    idempotency.
    """
    full=marker(key)+'\n'+body
    m=marker(key)
    for c in _get_comments(issue_number):
        if m in (c.get('body') or ''):
            try:
                gh.delete_comment(c['id'])
            except Exception as e:
                gh.log('comments','could not delete old '+str(key)+' on #'+str(issue_number)+': '+type(e).__name__+': '+str(e)[:200])
    return gh.add_comment(issue_number,full)


def add(issue_number,body):
    return gh.add_comment(issue_number,body)
