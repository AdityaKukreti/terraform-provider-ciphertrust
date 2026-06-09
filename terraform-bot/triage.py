import fnmatch

PROVIDER_TEXT_RULES={
    'auth':['auth','authentication','authorize','unauthorized','forbidden','credential','credentials','token','login','api key','apikey'],
    'provider-config':['provider configuration','provider config','configure provider','provider block'],
    'ciphertrust-manager':['ciphertrust manager','ctm','ciphertrust'],
    'key-management':['key','keys','kms','key management','rotation','encrypt','decrypt','crypto'],
    'resource':['resource','terraform resource'],
    'data-source':['data source','datasource','data-source'],
    'regression':['regression','worked before','previous version','after upgrade'],
    'acceptance-test':['acceptance test','acctest','tf_acc']
}

PROVIDER_FILE_RULES={
    'auth':['**/*auth*','**/*credential*','**/*token*','**/*login*'],
    'provider-config':['provider/**','**/*provider*'],
    'key-management':['**/*key*','**/*kms*','**/*crypto*'],
    'resource':['**/resource_*.go','**/*resource*'],
    'data-source':['**/data_source_*.go','**/*data_source*','**/*datasource*'],
    'acceptance-test':['**/*_test.go','**/*acctest*'],
    'ci':['.github/**'],
    'dependencies':['go.mod','go.sum']
}

HIGH_RISK_PATTERNS=[
    '.github/workflows/**',
    'terraform-bot/**',
    'go.mod',
    'go.sum',
    '**/*auth*',
    '**/*credential*',
    '**/*token*',
    '**/*secret*',
    '**/*tls*',
]

PROVIDER_CODE_PATTERNS=['provider/**/*.go','internal/**/*.go','**/resource_*.go','**/data_source_*.go']
TEST_PATTERNS=['**/*_test.go','**/test/**','**/*acctest*']
DOC_PATTERNS=['docs/**','examples/**','*.md','**/*.md']
USER_FACING_PATTERNS=['provider/**','**/resource_*.go','**/data_source_*.go','examples/**']

ISSUE_REQUIRED_SIGNALS={
    'terraform version':['terraform version','terraform v','tf version'],
    'provider version':['provider version','ciphertrust provider version'],
    'steps to reproduce':['steps to reproduce','repro','reproduction','how to reproduce'],
    'expected behavior':['expected behavior','expected'],
    'actual behavior':['actual behavior','actual','error','fails','failure'],
}


def matches_any(path,patterns):
    return any(fnmatch.fnmatch(path,p) for p in patterns)


def text_blob(item):
    return (str(item.get('title',''))+' '+str(item.get('body') or '')).lower()


def provider_labels_from_text(item):
    text=text_blob(item)
    labels=[]
    for label,needles in PROVIDER_TEXT_RULES.items():
        if any(n in text for n in needles):
            labels.append(label)
    return sorted(set(labels))


def provider_labels_from_files(files):
    labels=[]
    for f in files:
        low=f.lower()
        for label,patterns in PROVIDER_FILE_RULES.items():
            if matches_any(low,patterns):
                labels.append(label)
    return sorted(set(labels))


def missing_tests_docs(files):
    labels=[]; reasons=[]
    changed_provider_code=any(matches_any(f,PROVIDER_CODE_PATTERNS) for f in files)
    changed_user_facing=any(matches_any(f,USER_FACING_PATTERNS) for f in files)
    has_tests=any(matches_any(f,TEST_PATTERNS) for f in files)
    has_docs=any(matches_any(f,DOC_PATTERNS) for f in files)
    if changed_provider_code and not has_tests:
        labels.append('needs-tests')
        reasons.append('provider/internal Go code changed but no test files were changed')
    if changed_user_facing and not has_docs:
        labels.append('needs-docs')
        reasons.append('user-facing provider/resource behavior may have changed but docs/examples were not updated')
    return sorted(set(labels)),reasons


def risk_report(item,files=None):
    files=files or []
    reasons=[]
    labels=[]
    risky=[f for f in files if matches_any(f,HIGH_RISK_PATTERNS)]
    provider_code=[f for f in files if matches_any(f,PROVIDER_CODE_PATTERNS)]
    if risky:
        labels.append('risk/high')
        reasons.append('high-risk files changed: '+', '.join(risky[:5]))
    if provider_code:
        labels.append('risk/medium')
        reasons.append('provider/internal code changed: '+', '.join(provider_code[:5]))
    if files and all(matches_any(f,DOC_PATTERNS) for f in files):
        labels.append('risk/low')
        reasons.append('docs/examples/markdown-only change')
    text=text_blob(item)
    if any(x in text for x in ['breaking','deprecate','remove','rename','migration','force new','schema change']):
        labels.append('breaking-change')
        labels.append('risk/high')
        reasons.append('breaking-change language detected in title/body')
    if any(x in text for x in ['auth','authentication','token','credential','secret','tls']):
        labels.append('security-review-required')
        reasons.append('security/auth-sensitive language detected')
    labels=sorted(set(labels))
    if 'risk/high' in labels:
        level='high'
    elif 'risk/medium' in labels:
        level='medium'
    elif 'risk/low' in labels:
        level='low'
    else:
        level='unknown'
        reasons.append('not enough signal to classify risk')
    return {'level':level,'labels':labels,'reasons':reasons}


def issue_quality(issue):
    text=text_blob(issue)
    missing=[name for name,needles in ISSUE_REQUIRED_SIGNALS.items() if not any(n in text for n in needles)]
    labels=[]
    if 'steps to reproduce' in missing:
        labels.append('needs-repro')
    if len(missing)>=2:
        labels.append('needs-info')
    return sorted(set(labels)),missing


def issue_quality_comment(missing):
    if not missing:return None
    lines=['Thanks for opening this issue. To help maintainers reproduce and triage it, please add the missing details below:','']
    for m in missing:
        lines.append('- '+m)
    lines.append('')
    lines.append('_Handled by ciphertrust-bot._')
    return '\n'.join(lines)


def pr_quality_comment(test_doc_reasons,risk):
    lines=[]
    if test_doc_reasons:
        lines.append('PR quality checks found follow-up items:')
        for r in test_doc_reasons:
            lines.append('- '+r)
    if risk.get('level') in ('medium','high'):
        lines.append('Risk: '+risk.get('level'))
        for r in risk.get('reasons',[])[:5]:
            lines.append('- '+r)
    if not lines:return None
    lines.append('')
    lines.append('_Handled by ciphertrust-bot._')
    return '\n'.join(lines)


def risk_markdown(item,files=None):
    risk=risk_report(item,files or [])
    lines=['Risk assessment: **'+risk['level']+'**','']
    lines.append('Reasons:')
    for r in risk['reasons']:
        lines.append('- '+r)
    if risk['labels']:
        lines.append('')
        lines.append('Suggested labels: '+', '.join(risk['labels']))
    return '\n'.join(lines)
