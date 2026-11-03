# 차례 쪽 번호 채우기: 빌드 → 쪽 찾기 → pages.json → 다시 빌드
import subprocess, re, json, os
D = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(D, '..', '클로드코드_실무연수.pdf')
def build(): subprocess.run(['node', os.path.join(D, 'build.js')], check=True, capture_output=True)
def scan():
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', P], capture_output=True, text=True).stdout).group(1))
    m = {'시작 전': 'tools', '시작 전 · 2': 'menus', '시작 전 · 3': 'setup', '시작 전 · 4': 'pro'}; out = {}
    for p in range(3, n+1):
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), P, '-'], capture_output=True, text=True).stdout
        first = [l.strip() for l in t.split('\n') if l.strip()][:2]
        for l in first:
            g = re.match(r'^(EP \d+|시작 전(?: · \d)?)\s+·\s+이런 일이 됩니다', l)
            if g:
                k = m.get(g.group(1)) or 'ep' + g.group(1)[3:]; out.setdefault(k, str(p))
        if first and first[0].startswith('30분 실습'): out.setdefault('wrap', str(p))
        if first and '이 자료는 이렇게 만들었습니다' in first[0]: out.setdefault('colophon', str(p))
    return out
build(); pg = scan(); json.dump(pg, open(os.path.join(D, 'pages.json'), 'w')); build()
pg2 = scan(); print('stable' if pg == pg2 else 'shifted', len(pg), pg.get('wrap'), pg.get('colophon'))
