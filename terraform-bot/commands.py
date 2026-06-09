import subprocess as s
import llm
ALLOWED={'OWNER','MEMBER','COLLABORATOR'}
HELP='''Terraform bot commands:\n- /bot help\n- /bot label <label>\n- /bot needs-repro\n- /bot duplicate #123\n- /bot summarize\n- /bot groq-check\n'''

def comment(n,msg):s.run(['gh','issue','comment',str(n),'--body',msg],check=False)

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
    if p[1]=='label' and len(p)>2:
        s.run(['gh','issue','edit',str(n),'--add-label',p[2]],check=False);return comment(n,'Added label: '+p[2])
    if p[1]=='needs-repro':
        msg=llm.summarize(issue) or 'Please add reproduction steps, expected/actual behavior, and provider/Terraform versions.'
        s.run(['gh','issue','edit',str(n),'--add-label','needs-repro'],check=False);return comment(n,msg)
    if p[1]=='duplicate' and len(p)>2:
        s.run(['gh','issue','edit',str(n),'--add-label','duplicate'],check=False);return comment(n,'Possible duplicate of '+p[2])
