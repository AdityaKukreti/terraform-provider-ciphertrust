import subprocess as s
ALLOWED={'OWNER','MEMBER','COLLABORATOR'}
HELP='''Terraform bot commands:\n- /bot help\n- /bot label <label>\n- /bot needs-repro\n- /bot duplicate #123\n'''

def comment(n,msg):s.run(['gh','issue','comment',str(n),'--body',msg],check=False)

def run(issue,c):
    body=c.get('body','').strip()
    if not body.startswith('/bot'):return
    n=issue['number'];p=body.split()
    if c.get('author_association') not in ALLOWED:
        return comment(n,'Only repo collaborators can run bot commands.')
    if len(p)<2 or p[1]=='help':return comment(n,HELP)
    if p[1]=='label' and len(p)>2:
        s.run(['gh','issue','edit',str(n),'--add-label',p[2]],check=False);return comment(n,'Added label: '+p[2])
    if p[1]=='needs-repro':
        s.run(['gh','issue','edit',str(n),'--add-label','needs-repro'],check=False);return comment(n,'Please add reproduction steps, expected/actual behavior, and provider/Terraform versions.')
    if p[1]=='duplicate' and len(p)>2:
        s.run(['gh','issue','edit',str(n),'--add-label','duplicate'],check=False);return comment(n,'Possible duplicate of '+p[2])
