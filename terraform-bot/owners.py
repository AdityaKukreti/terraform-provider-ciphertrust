import fnmatch
import os
import bot_config


def parse_codeowners(path='CODEOWNERS'):
    owners=[]
    if not os.path.exists(path):
        return owners
    try:
        for raw in open(path,'r',encoding='utf-8').read().splitlines():
            line=raw.strip()
            if not line or line.startswith('#'):
                continue
            parts=line.split()
            if len(parts)<2:
                continue
            pattern=parts[0]
            names=[p.lstrip('@') for p in parts[1:] if p.startswith('@')]
            if names:
                owners.append((normalize_pattern(pattern),names))
    except Exception as e:
        print('[terraform-bot][owners] failed reading CODEOWNERS: '+type(e).__name__+': '+str(e)[:300],flush=True)
    return owners


def normalize_pattern(pattern):
    pattern=pattern.strip()
    if pattern.startswith('/'):
        pattern=pattern[1:]
    if pattern.endswith('/'):
        pattern=pattern+'**'
    if '/' not in pattern and not pattern.startswith('**'):
        pattern='**/'+pattern
    return pattern


def fallback_owners():
    fallback=bot_config.get('owners.fallback',{}) or {}
    return [(p,[x.lstrip('@') for x in names]) for p,names in fallback.items() if names]


def reviewers_for_files(files):
    rules=parse_codeowners()+fallback_owners()
    reviewers=set()
    for f in files:
        for pattern,names in rules:
            if fnmatch.fnmatch(f,pattern) or fnmatch.fnmatch('/'+f,pattern):
                reviewers.update(names)
    return sorted(reviewers)
