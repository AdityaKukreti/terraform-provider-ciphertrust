import copy
import os
import yaml

DEFAULTS={
    'bot':{'dashboard_issue_title':'CipherTrust Bot Dashboard','idempotent_comments':True},
    'labels':{'managed_extra':[]},
    'risk':{
        'high_risk_paths':['.github/workflows/**','terraform-bot/**','go.mod','go.sum','**/*auth*','**/*credential*','**/*token*','**/*secret*','**/*tls*'],
        'low_risk_paths':['docs/**','examples/**','*.md','**/*.md'],
    },
    'commands':{'natural_language':True},
}
_CACHE=None


def deep_merge(a,b):
    out=copy.deepcopy(a)
    for k,v in (b or {}).items():
        if isinstance(v,dict) and isinstance(out.get(k),dict):
            out[k]=deep_merge(out[k],v)
        else:
            out[k]=v
    return out


def load():
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    cfg=copy.deepcopy(DEFAULTS)
    path='.ciphertrust-bot.yml'
    if os.path.exists(path):
        with open(path,'r',encoding='utf-8') as f:
            cfg=deep_merge(cfg,yaml.safe_load(f) or {})
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
