import json
import os
import re

LABEL_ENUM=['bug','documentation','enhancement','auth','security','ciphertrust-manager','provider-config','resource','data-source']
INTENTS={'help','features','summarize','explain','duplicate','check-labels','clean-labels','label','unknown'}
# Section names must match the keys of triage.ISSUE_SIGNAL_PATTERNS exactly so
# the LLM and regex paths share one vocabulary and one threshold rule.
QUALITY_SECTIONS=['terraform version','provider version','steps to reproduce','expected behavior','actual behavior']


def _log(msg):
    try:
        import github_api as gh
        gh.log('llm',msg)
    except Exception:
        pass


def _client():
    key=os.getenv('GROQ_API_KEY')
    if not key:
        return None
    try:
        from groq import Groq
        return Groq(api_key=key)
    except Exception:
        return None


def _strip_fences(text):
    text=re.sub(r'^```(?:json)?\s*','',text.strip(),flags=re.MULTILINE)
    return re.sub(r'```\s*$','',text.strip(),flags=re.MULTILINE).strip()


def ask(system_prompt,user_content='',max_tokens=700,json_mode=False,temperature=0.1):
    c=_client()
    if not c:
        # A missing key is an expected config state; a key that is set but yields
        # no client means groq failed to import/init — surface that, don't hide it.
        if os.getenv('GROQ_API_KEY'):
            _log('GROQ_API_KEY is set but the LLM client is unavailable (groq package missing or failed to init)')
        return ''
    try:
        messages=[{'role':'system','content':system_prompt}]
        if user_content:
            messages.append({'role':'user','content':user_content})
        kwargs=dict(
            model=os.getenv('GROQ_MODEL','llama-3.3-70b-versatile'),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if json_mode:
            kwargs['response_format']={'type':'json_object'}
        res=c.chat.completions.create(**kwargs)
        return res.choices[0].message.content.strip()
    except Exception as e:
        _log('call failed: '+str(e)[:200])
        return ''


def classify_labels(title,body,files=None,patch=None,context='issue'):
    """LLM-primary label classifier over the fixed content-label enum.

    Reads the issue/PR content (and, for PRs, the changed files + diff) and
    returns the applicable labels as a subset of LABEL_ENUM. Returns None when
    the LLM is unavailable or the reply can't be parsed, so callers fall back to
    the deterministic rules. An empty list means "no content labels apply".
    """
    guide=(
        '- bug: a defect, crash, panic, error, or broken/regressed behavior\n'
        '- enhancement: a feature request or an improvement to existing behavior\n'
        '- documentation: a change or request primarily about docs, README, or examples\n'
        '- auth: authentication/authorization — login, tokens, credentials, certificates, TLS\n'
        '- security: security-sensitive (credentials/secrets, TLS, auth, vulnerabilities). Always include when auth applies\n'
        '- ciphertrust-manager: about CipherTrust Manager (CM) itself — domains, connections, users, licensing, configuration\n'
        '- provider-config: the Terraform provider block / endpoint / provider authentication configuration\n'
        '- resource: a Terraform resource (ciphertrust_* resource, resource_*.go)\n'
        '- data-source: a Terraform data source (data sources, data_source_*.go)')
    system=('You label a GitHub '+context+' for the CipherTrust Terraform provider. '
            'Read the content and decide which of these labels genuinely apply:\n'+guide+'\n\n'
            'Decide from what the '+context+' is actually about, not incidental wording '
            '(e.g. the phrase "for example" is not documentation). '
            'Apply only labels that clearly fit; returning few or none is fine. '
            'Return JSON only: {"labels": [...]} using ONLY the exact label names listed above.')
    user='Title: '+str(title)+'\nBody: '+str(body or '')[:5000]
    if files:
        user+='\n\nChanged files:\n'+'\n'.join('- '+str(f) for f in files[:50])
    if patch:
        user+='\n\nDiff:\n'+str(patch)[:5000]
    out=ask(system,user,max_tokens=200,json_mode=True,temperature=0)
    if not out:
        return None
    try:
        data=json.loads(_strip_fences(out))
        labels=data.get('labels')
        if not isinstance(labels,list):
            return None
        return [x for x in labels if x in LABEL_ENUM]
    except Exception:
        _log('classify_labels: could not parse response')
        return None


def assess_quality(title,body):
    """Semantically judge which required sections are missing from an issue.

    Returns a list of missing section names (a subset of QUALITY_SECTIONS;
    possibly empty when nothing is missing) when the LLM answered, or None when
    the LLM was unavailable / failed — the caller treats None as "fall back to
    the regex check". Empty-list and None are deliberately distinct.
    """
    system=('You are triaging a GitHub issue for the CipherTrust Terraform provider. '
            'Decide which of these required sections are MISSING from the issue:\n'
            '- terraform version\n- provider version\n- steps to reproduce\n- expected behavior\n- actual behavior\n\n'
            'A section is PRESENT if the information appears anywhere in the issue in any form — '
            'a heading, prose, a numbered list, a code block, or pasted CLI output — even if it is '
            'not under an exact heading and even if interleaved with other content. For example, '
            'pasted `terraform version` output that lists the provider satisfies "provider version"; '
            'numbered steps with code fences between them satisfy "steps to reproduce". '
            'Be lenient: only report a section as missing if the information genuinely is not present. '
            'Return JSON only: {"missing": [...]} using only the exact section names listed above.')
    user='Title: '+str(title)+'\nBody: '+str(body or '')[:5000]
    out=ask(system,user,max_tokens=200,json_mode=True)
    if not out:
        return None
    try:
        data=json.loads(_strip_fences(out))
        return [x for x in data.get('missing',[]) if x in QUALITY_SECTIONS]
    except Exception:
        _log('assess_quality: could not parse response')
        return None


def summarize(title,body,patch=None,comments=None):
    if patch:
        system=('Summarize this pull request for maintainers in concise Markdown. '
                'You have the description AND the actual diff. '
                'Cover: what changed and why, which files/areas are affected, and the suggested next action.')
        user='Title: '+str(title)+'\nDescription: '+str(body or '')[:1000]+'\nDiff:\n'+str(patch)[:4000]
    else:
        system='Summarize the GitHub issue/PR provided by the user for maintainers in concise Markdown. Include problem, likely area, and next action.'
        user='Title: '+str(title)+'\nBody: '+str(body or '')[:5000]
        if comments:
            user+='\n\nComments:\n'+str(comments)[:3000]
    return ask(system,user,max_tokens=120)


def explain_pr(title,body,patch):
    system='Explain the code changes in this pull request for a Terraform provider. Describe what changed, how it works, and any notable side effects or risks. Be concise and technical.'
    user='Title: '+str(title)+'\nDescription: '+str(body or '')[:1000]+'\nDiff:\n'+str(patch or '')[:5000]
    return ask(system,user,max_tokens=600)


def intent(text):
    system=('Map the user\'s bot mention to a safe intent. Return JSON only: {"intent": "<value>", "args": {}}.\n'
            'Allowed intents: help, features, summarize, explain, duplicate, check-labels, clean-labels, label, unknown.\n'
            'Use explain for requests to explain code changes or the PR diff. Use summarize for high-level issue/PR summaries.\n'
            'Use unknown for any destructive, unclear, or unrecognised requests.')
    user=str(text or '')[:2000]
    out=ask(system,user,max_tokens=150,json_mode=True)
    try:
        data=json.loads(_strip_fences(out))
        if data.get('intent') not in INTENTS:
            data['intent']='unknown'
        data['args']=data.get('args') or {}
        return data
    except Exception:
        return {'intent':'unknown','args':{}}
