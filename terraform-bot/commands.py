import subprocess as s
import llm
import labeler
ALLOWED={'OWNER','MEMBER','COLLABORATOR'}
HELP='''Terraform bot commands:\n- `/bot help`\n- `/bot label` auto-detect labels\n- `/bot label bug` add one label manually\n- `/bot needs-repro`\n- `/bot duplicate #123`\n- `/bot summarize`\n- `/bot groq-check`\n'''

def comment(n,msg):s.run(['gh','issue','comment',str(n),'--body',msg],check=False)

def label_result(n,labels):
    added,failed=labeler.add_labels(n,labels)
    parts=[]
    if added:parts.append('Added labels: '+', '.join(added))
    if failed:parts.append('Failed labels: '+', '.join(failed))
    return comment(n,'\n'.join(parts) if parts else 'No labels changed.')

def run(issue,c):
    body=c.get('body','').strip()
    if not body.startswith('/bot'):return
    n=issue['number'];p=body.split()
    if c.get('author_association') not in ALLOWED:
        return comment(n,'Only repo collaborators can run bot commands.')
    if len(p)<2 or p[1]=='help':return comment(n,HELP)
    if p[1]=='groq-check':return comment(n,llm.status())
    if p[1]=='summarize':
        msg=llm.summarize(issue) or ('LLM summary unavailable. '+llm.LAST_ERROR)
        return comment(n,msg)
    if p[1]=='label':
        if len(p)>2:return label_result(n,[' '.join(p[2:])])
        labels=labeler.suggest(issue)
        if not labels:return comment(n,'No matching labels detected for this issue.')
        return label_result(n,labels)
    if p[1]=='needs-repro':
        msg=llm.summarize(issue) or 'Please add reproduction steps, expected/actual behavior, and provider/Terraform versions.'
        labeler.add_labels(n,['needs-repro']);return comment(n,msg)
    if p[1]=='duplicate' and len(p)>2:
        labeler.add_labels(n,['duplicate']);return comment(n,'Possible duplicate of '+p[2])
