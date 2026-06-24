import fnmatch
import re
import bot_config

PROVIDER_LABEL_RULES={
    'auth':[r'\bauth\b',r'\blogin\b',r'\bunauthorized\b',r'\bforbidden\b',r'\bcertificate\b',r'\btls\b'],
    'provider-config':[r'provider\s+config',r'provider\s+block',r'\bendpoint\b',r'ciphertrust\s+manager'],
    'ciphertrust-manager':[r'ciphertrust\s+manager',r'\bciphertrust\b',r'\bcm\b'],
    'resource':[r'resource_',r'\bresource\b'],
    'data-source':[r'data[\s_]source',r'\bdatasource\b'],
}
HIGH_RISK_PATTERNS=['.github/workflows/**','terraform-bot/**','go.mod','go.sum','**/*auth*','**/*tls*']
CODE_PATTERNS=['provider/**/*.go','internal/**/*.go','**/resource_*.go','**/data_source_*.go']
TEST_PATTERNS=['**/*_test.go','**/test/**','**/*acctest*']
DOC_PATTERNS=['docs/**','examples/**','*.md','**/*.md']

ISSUE_SIGNAL_PATTERNS={
    'terraform version':[
        r'(?im)^\s*(?:terraform\s*(?:cli\s*)?version|tf\s*version)\s*[:=]?\s*`?v?\d+\.\d+',
        r'(?im)^\s*terraform\s+v?\d+\.\d+',
        r'(?i)terraform\s+v\d+\.\d+',
        r'(?i)terraform\s*-v',
    ],
    'provider version':[
        r'(?im)^\s*(?:provider|ciphertrust provider|terraform-provider-ciphertrust)\s*(?:version)?\s*[:=]\s*`?["~>=< ]*v?\d+\.\d+',
        r'(?i)terraform-provider-ciphertrust\s+v?\d+\.\d+',
        r'(?is)required_providers.{0,600}ciphertrust.{0,300}version\s*=',
        r'(?i)thalesgroup[/ ]ciphertrust.{0,120}version\s*=',
        r'(?i)(?:terraform-provider-ciphertrust|thalesgroup[/ ]ciphertrust|provider)\b[^\n]{0,80}version\s*[:=]?\s*["\'`~>=< v]*\d+\.\d+',
    ],
    'steps to reproduce':[
        r'(?im)^\s*(?:steps to reproduce|reproduction steps|steps|repro)\s*[:#-]*\s*$',
        r'(?im)^\s*1[\.)]\s+.+\n\s*2[\.)]\s+',
        r'(?i)(?:run|execute)\s+`?(?:terraform\s+(?:init|plan|apply|import|refresh)|go\s+test)',
    ],
    'expected behavior':[
        r'(?im)^\s*expected(?: behavior| result)?\s*[:#-]*',
        r'(?i)\b(?:expected|should)\b.{0,120}\b(?:create|update|read|delete|succeed|work|return|show|not fail)\b',
    ],
    'actual behavior':[
        r'(?im)^\s*(?:actual(?: behavior| result)?|observed(?: behavior| result)?|error output)\s*[:#-]*',
        r'(?i)\b(?:actual|got|instead)\b.{0,120}\b(?:error|fail|failed|panic|timeout|unauthorized|forbidden)\b',
        r'(?i)\b(?:error|panic|timeout|unauthorized|forbidden|invalid|failed|failure|crash|nil pointer)\b',
        r'(?im)^\s*```',
    ],
}


def text_of(obj):
    return ((obj.get('title') or '')+'\n'+(obj.get('body') or '')).lower()


def raw_text(obj):
    return (obj.get('title') or '')+'\n'+(obj.get('body') or '')


def provider_labels_from_text(obj):
    text=text_of(obj)
    labels=set()
    for label,patterns in PROVIDER_LABEL_RULES.items():
        if any(re.search(p,text) for p in patterns):
            labels.add(label)
    if 'auth' in labels or re.search(r'\bsecurity\b',text):
        labels.add('security')
    return sorted(labels)


def provider_labels_from_files(files):
    labels=set()
    for f in files:
        low=f.lower()
        if 'auth' in low or 'tls' in low:
            labels.update(['auth','security'])
        if 'resource_' in low: labels.add('resource')
        if 'data_source' in low: labels.add('data-source')
        if 'provider' in low: labels.add('provider-config')
    return sorted(labels)


def matches_any(path,patterns):
    return any(fnmatch.fnmatch(path,p) for p in patterns)


def risk_report(obj,files=None):
    files=files or []
    reasons=[]; labels=set(); level='low' if files else 'unknown'
    text=text_of(obj)
    high_risk_paths=bot_config.get('risk.high_risk_paths',HIGH_RISK_PATTERNS)
    low_risk_paths=bot_config.get('risk.low_risk_paths',DOC_PATTERNS)
    # 'level' is computed to gate the PR triage risk section.
    # The only label this produces is 'security' on security/auth-sensitive wording.
    risky=[f for f in files if matches_any(f,high_risk_paths)]
    if risky:
        level='high'; reasons.append('high-risk files changed: '+', '.join(risky[:5]))
    elif files:
        code=[f for f in files if matches_any(f,CODE_PATTERNS)]
        if code:
            level='medium'; reasons.append('provider/internal Go code changed')
        elif all(matches_any(f,low_risk_paths) for f in files):
            level='low'; reasons.append('docs/examples-only change')
        else:
            level='medium'; reasons.append('non-doc files changed')
    if any(re.search(p,text) for p in [r'\btls\b',r'\bcertificate\b',r'\bsecurity\b',r'\bauth\b']):
        level='high'; labels.add('security'); reasons.append('security/auth-sensitive wording detected')
    if any(re.search(p,text) for p in [r'\bbreaking\b',r'migration\s+required',r'\bincompatible\b']):
        level='high'; reasons.append('breaking-change wording detected')
    return {'level':level,'labels':sorted(labels),'reasons':reasons or ['no major risk signals detected']}


def missing_tests_docs(files):
    # A *_test.go file matches CODE_PATTERNS too; exclude tests so a test-only
    # change isn't treated as code that needs tests/docs.
    code_changed=any(matches_any(f,CODE_PATTERNS) and not matches_any(f,TEST_PATTERNS) for f in files)
    tests_changed=any(matches_any(f,TEST_PATTERNS) for f in files)
    docs_changed=any(matches_any(f,DOC_PATTERNS) for f in files)
    labels=[]; reasons=[]
    if code_changed and not tests_changed:
        labels.append('needs-tests'); reasons.append('provider/internal Go code changed but no test files were changed')
    if code_changed and not docs_changed:
        labels.append('needs-docs'); reasons.append('user-facing provider/resource behavior may have changed but docs/examples were not updated')
    return labels,reasons


def has_signal(obj,name):
    blob=raw_text(obj)
    return any(re.search(pattern,blob) for pattern in ISSUE_SIGNAL_PATTERNS[name])


def quality_labels_from_missing(body,missing):
    # Shared rule turning the list of missing sections into quality labels.
    # Used by both the regex path (issue_quality) and the LLM path so the two
    # judges apply identical thresholds. Note: 'steps to reproduce' still counts
    # toward the missing total (and the "more info needed" comment) but no longer
    # emits its own label.
    labels=[]
    if len((body or '').strip())<80 or len(missing)>=1:
        labels.append('needs-info')
    return sorted(set(labels))


def issue_quality(obj):
    body=obj.get('body') or ''
    missing=[name for name in ISSUE_SIGNAL_PATTERNS if not has_signal(obj,name)]
    return quality_labels_from_missing(body,missing),missing


def issue_quality_comment(missing):
    if not missing:return ''
    return '## More information needed\n\nPlease add only the missing details below:\n\n'+'\n'.join('- '+m for m in missing)+'\n\n_Handled by ciphertrust-bot._'


def pr_quality_comment(missing_reasons,risk):
    if not missing_reasons and risk.get('level')!='high': return ''
    parts=['## PR Quality / Risk Notes','']
    if missing_reasons:
        parts.append('### Missing checks')
        parts.extend('- '+r for r in missing_reasons)
        parts.append('')
    if risk.get('level')=='high':
        parts.append('### Risk')
        parts.extend('- '+r for r in risk.get('reasons',[]))
    return '\n'.join(parts)
