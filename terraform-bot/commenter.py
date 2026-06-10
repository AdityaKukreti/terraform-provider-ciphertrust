import re
import github_api as gh
import bot_config

BOT_MARKER_PREFIX='<!-- ciphertrust-bot:'

def marker(key):
    return BOT_MARKER_PREFIX+str(key)+' -->'

def strip_code_and_quotes(body):
    lines=[];in_fence=False
    for line in (body or '').splitlines():
        if line.strip().startswith('```'):
            in_fence=not in_fence
            continue
        if in_fence:continue
        if line.lstrip().startswith('>'):continue
        lines.append(line)
    return '\n'.join(lines)

def find_existing_comment(issue_number,key):
    m=marker(key)
    comments=gh.issue_comments(issue_number)
    for c in comments:
        body=c.get('body') or ''
        user=(c.get('user') or {}).get('login','')
        if m in body and ('bot' in user.lower() or user):
            return c
    return None

def upsert(issue_number,key,body):
    full=marker(key)+'\n'+body
    if not bot_config.enabled('bot.idempotent_comments',True):
        return gh.add_comment(issue_number,full)
    existing=find_existing_comment(issue_number,key)
    if existing:
        return gh.update_comment(existing['id'],full)
    return gh.add_comment(issue_number,full)

def add(issue_number,body):
    return gh.add_comment(issue_number,body)
