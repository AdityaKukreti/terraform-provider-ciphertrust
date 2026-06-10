import os
import yaml

DEFAULTS={
    'bot':{
        'dashboard_issue_title':'CipherTrust Bot Dashboard',
        'idempotent_comments':True,
    },
    'labels':{'managed_extra':[]},
    'owners':{'fallback':{}},
    'auto_merge':{
        'enabled':False,
        'label':'automerge',
        'method':'squash',
        'trusted_author_associations':['OWNER','MEMBER','COLLABORATOR'],
    },
    'merge_queue':{
        'enabled':True,
        'label':'merge-queue',
        'ready_label':'automerge',
    },
    'commands':{
        'natural_language':True,
        'min_intent_confidence':0.75,
    },
}

_CACHE=None

def deep_merge(base,override):
    if not isinstance(base,dict) or not isinstance(override,dict):
        return override
    out=dict(base)
    for k,v in override.items():
        out[k]=deep_merge(out.get(k),v) if k in out else v
    return out

def load():
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    cfg=DEFAULTS
    path=os.getenv('CIPHERTRUST_BOT_CONFIG','.ciphertrust-bot.yml')
    try:
        if os.path.exists(path):
            with open(path,'r',encoding='utf-8') as f:
                loaded=yaml.safe_load(f) or {}
            cfg=deep_merge(DEFAULTS,loaded)
    except Exception as e:
        print('[terraform-bot][config] failed loading '+path+': '+type(e).__name__+': '+str(e)[:300],flush=True)
    _CACHE=cfg
    return cfg

def get(path,default=None):
    cur=load()
    for part in path.split('.'):
        if not isinstance(cur,dict) or part not in cur:
            return default
        cur=cur[part]
    return cur

def enabled(path,default=False):
    return bool(get(path,default))
