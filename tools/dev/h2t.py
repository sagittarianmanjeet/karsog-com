import re, html, sys, os
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0; s.href=[]; s.pre=''
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in('script','style','svg','noscript'): s.skip+=1; return
        if s.skip: return
        if t in('h1','h2','h3','h4'): s.out.append('\n\n'+'#'*int(t[1])+' ')
        elif t in('p','div','section','header','tr','ul','ol','table','details','figure','nav','footer','main'): s.out.append('\n')
        elif t=='li': s.out.append('\n- ')
        elif t=='summary': s.out.append('\nQ: ')
        elif t in('td','th'): s.out.append(' | ')
        elif t=='br': s.out.append(' / ')
        elif t=='a': s.href.append(a.get('href','')); s.out.append('[')
        elif t=='img': s.out.append(f"[img {a.get('src','')} alt={a.get('alt','')!r}]")
        elif t in('b','strong'): s.out.append('**')
        elif t=='em': s.out.append('_')
    def handle_endtag(s,t):
        if t in('script','style','svg','noscript'): s.skip-=1; return
        if s.skip: return
        if t=='a': h=s.href.pop() if s.href else ''; s.out.append(f']({h})')
        elif t in('b','strong'): s.out.append('**')
        elif t=='em': s.out.append('_')
        elif t in('p','h1','h2','h3','h4','li','summary'): s.out.append('\n')
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
def conv(path):
    x=open(path,encoding='utf-8').read()
    head=x[:x.find('<body')]
    t=re.search(r'<title>(.*?)</title>',head,re.S); d=re.search(r'<meta name="description" content="([^"]*)',head)
    b=x[x.find('<body'):]
    # drop nav/menus
    b=re.sub(r'<nav class="top.*?</nav>','',b,flags=re.S)
    b=re.sub(r'<div class="ksub">.*?</div></div>','',b,flags=re.S)
    p=P(); p.feed(b)
    s=''.join(p.out)
    s=re.sub(r'[ \t]+',' ',s); s=re.sub(r' *\n *','\n',s); s=re.sub(r'\n{3,}','\n\n',s)
    return f"TITLE: {html.unescape(t.group(1)) if t else ''}\nDESC: {html.unescape(d.group(1)) if d else ''}\n{s.strip()}\n"
if __name__=='__main__':
    out=sys.argv[1]
    for f in sys.argv[2:]:
        name=f.replace('public/','').replace('/index.html','').replace('/','_') or 'home'
        if name=='index.html': name='home'
        open(os.path.join(out,name+'.txt'),'w').write(conv(f))
