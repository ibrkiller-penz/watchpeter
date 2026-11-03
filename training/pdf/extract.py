# book.html → 검토용 텍스트(섹션별). 사용: python3 extract.py → review/text/<id>.txt, review/book.txt
import re, html, os
D=os.path.dirname(os.path.abspath(__file__)); s=open(os.path.join(D,'book.html'),encoding='utf8').read()
os.makedirs(os.path.join(D,'review','text'),exist_ok=True)
def clean(t):
    t=re.sub(r'<svg.*?</svg>','[그림]',t,flags=re.S)
    t=re.sub(r'<img [^>]*alt="([^"]*)"[^>]*>',r'[사진: \1]',t)
    t=re.sub(r'</(p|li|h2|h3|h4|tr|dt|dd|pre|figcaption|div)>','\n',t)
    t=re.sub(r'<h2[^>]*>','\n## ',t); t=re.sub(r'<h3[^>]*>','\n### ',t); t=re.sub(r'<h4[^>]*>','\n#### ',t)
    t=re.sub(r'<p class="lbl">','\n[',t); t=re.sub(r'<td[^>]*>',' | ',t)
    t=re.sub(r'<[^>]+>','',t); t=html.unescape(t)
    return re.sub(r'\n\s*\n+','\n',t).strip()
allt=[]
for m in re.finditer(r'<section class="(?:ep|reel|toc|cover)"(?: id="([^"]+)")?[^>]*>(.*?)</section>',s,re.S):
    sid=m.group(1) or 'front'; t=clean(m.group(2))
    if sid!='front': open(os.path.join(D,'review','text',sid+'.txt'),'w',encoding='utf8').write(t)
    allt.append(f'===== [{sid}] =====\n{t}')
open(os.path.join(D,'review','book.txt'),'w',encoding='utf8').write('\n\n'.join(allt))
print(len('\n'.join(allt)),'chars')
