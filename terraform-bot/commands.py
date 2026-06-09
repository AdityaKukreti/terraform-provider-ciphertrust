import subprocess as s
import llm
import labeler
ALLOWED={'OWNER','MEMBER','COLLABORATOR'}
TRIGGERS=('/bot','@cipherbot')
HELP='''Terraform bot commands:\n- `/bot help` or `@cipherbot help`\n- `/bot label` or `@cipherbot label` auto-detect labels\n- `/bot label bug` or `@cipherbot label bug` add one label manually\n- `/bot needs-repro` or `@cipherbot needs-repro`\n- `/bot duplicate #123` or `@cipherbot duplicate #123`\n- `/bot summarize` or `@cipherbot summarize`\n- `/bot groq-check` or `@cipherbot groq-check`\n'''

def comment(n,msg):s.run(['gh','issue','comment',str(n),'--body',msg],check=False)

def parse_command(body):
    body=body.strip()
    low=body.lower()
    for t in TRIGGERS:
        if low.startswith(t):
            rest=body[len(t):].strip()
            return rest.split()
    return None

def label_result(n,labels):
    added,failed=labeler.add_labels(n,labels)
    parts=[]
    if added:parts.append('Added labels: '+', '.join(added))
    if failed:parts.append('Failed labels: '+', '.join(failed))
    return comment(n,'\n'.join(parts) if parts else 'No labels changed.')

def run(issue,c):
    p=parse_command(c.get('body',''))
    if p is None:return
    n=issue['number']
    if c.get('author_association') not in ALLOWED:
        return comment(n,'Only repo collaborators can run bot commands.')
    if len(p)<1 or p[0]=='help':return comment(n,HELP)
    cmd=p[0]
    if cmd=='groq-check':return comment(n,llm.status())
    if cmd=='summarize':
        msg=llm.summarize(issue) or ('LLM summary unavailable. '+llm.LAST_ERROR)
        return comment(n,msg)
    if cmd=='label':
        if len(p)>1:return label_result(n,[' '.join(p[1:])])
        labels=labeler.suggest(issue)
        if not labels:return comment(n,'No matching labels detected for this issue.')
        return label_result(n,labels)
    if cmd=='needs-repro':
        msg=llm.summarize(issue) or 'Please add reproduction steps, expected/actual behavior, and provider/Terraform versions.'
        labeler.add_labels(n,['needs-repro']);return comment(n,msg)
    if cmd=='duplicate' and len(p)>1:
        labeler.add_labels(n,['duplicate']);return comment(n,'Possible duplicate of '+p[1])
