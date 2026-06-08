import subprocess as s

HELP='''Terraform bot commands:\n- /bot help\n- /bot label <label>\n- /bot needs-repro\n'''

def comment(n,msg):
    s.run(['gh','issue','comment',str(n),'--body',msg],check=False)

def run(issue,body):
    if not body.startswith('/bot'):return
    n=issue['number'];p=body.split()
    if len(p)<2 or p[1]=='help':comment(n,HELP)
    elif p[1]=='label' and len(p)>2:
        s.run(['gh','issue','edit',str(n),'--add-label',p[2]],check=False)
        comment(n,'Added label: '+p[2])
    elif p[1]=='needs-repro':
        s.run(['gh','issue','edit',str(n),'--add-label','needs-repro'],check=False)
        comment(n,'Please add reproduction steps, expected behavior, actual behavior, and provider/Terraform versions.')
