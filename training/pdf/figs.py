# 그림 생성기: 흐름도·화면 개략도(SVG)를 만들어 원고 section 안에 끼워 넣는다.
# 사용: python3 training/pdf/figs.py  (원고 part-*.html 원본은 건드리지 않고 build 단계에서 합침)
import html, json, os
D = os.path.dirname(os.path.abspath(__file__))
INK, ACC, SOFT, MARK, PAPER, LINE, MUTED, WARN = '#1D2321', '#1F5F57', '#E2EEEA', '#F3D34A', '#F3F5F0', '#C9D0C9', '#5B6661', '#9A3B1D'
FONT = "font-family=\"'IBM Plex Sans KR','Gothic A1',sans-serif\""

def esc(t): return html.escape(str(t))

def text(x, y, t, size=13, w='500', fill=INK, anchor='middle'):
    size = round(size*1.12, 1); lines = str(t).split('\n'); out = ''
    for i, l in enumerate(lines):
        out += f'<text x="{x}" y="{y + i*size*1.3}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {FONT}>{esc(l)}</text>'
    return out

def box(x, y, w, h, fill='#fff', stroke=LINE, r=8, sw=1.2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def arrow(x1, y1, x2, y2, c=ACC):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="2" marker-end="url(#ah)"/>'

def svg(w, h, body, label=''):
    defs = f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ACC}"/></marker></defs>'
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}">{defs}{body}</svg>'

def fig(svgcode, cap, kind='diagram'):
    tag = '개략도' if kind == 'mock' else '그림'
    return f'<figure class="fig {kind}">{svgcode}<figcaption><b>{tag}</b> {esc(cap)}</figcaption></figure>'

def flow(steps, hi=None, w=680):
    """steps: [(제목, 설명)] 가로 흐름. hi: 강조할 단계 번호 목록"""
    hi = hi or []; n = len(steps); gap = 26; bw = (w - 20 - gap*(n-1)) / n; bh = 92; y = 14; body = ''
    for i, (t, s) in enumerate(steps):
        x = 10 + i*(bw+gap); on = i in hi
        body += box(x, y, bw, bh, MARK if on else '#fff', INK if on else LINE, 10, 1.6 if on else 1.2)
        body += f'<circle cx="{x+16}" cy="{y+16}" r="10" fill="{ACC}"/>' + text(x+16, y+20.5, i+1, 11, '700', '#fff')
        body += text(x+bw/2, y+44, t, 14, '700')
        body += text(x+bw/2, y+64, s, 10.5, '400', MUTED)
        if i < n-1: body += arrow(x+bw+3, y+bh/2, x+bw+gap-3, y+bh/2)
    return svg(w, bh+28, body, ' → '.join(t for t, _ in steps))

def window(w, h, title, inner):
    b = box(2, 2, w-4, h-4, '#fff', INK, 10, 1.6)
    b += f'<path d="M2,12 a10,10 0 0 1 10,-10 h{w-24} a10,10 0 0 1 10,10 v18 h-{w-4} z" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
    for i, c in enumerate(['#E0857A', '#E8C76B', '#8FC48A']): b += f'<circle cx="{18+i*14}" cy="16" r="4.5" fill="{c}"/>'
    b += text(w/2, 20, title, 11.5, '600', MUTED)
    return svg(w, h, b + inner, title)

def callout(n, x, y):
    return f'<circle cx="{x}" cy="{y}" r="11" fill="{WARN}"/>' + text(x, y+4.5, n, 12, '700', '#fff')

F = {}
# ---------- 도구 고르기 ----------
def tools():
    cols = [('채팅', '묻고 답 받기', '짧은 질문·문장 다듬기', '복사해서 붙여 넣기'),
            ('Cowork', '폴더를 맡기기', '가정통신문·엑셀·공문·상장', '결과 파일이 폴더에'),
            ('클로드 코드', '앱을 만들고 고치기', '시간표·인정점·사이트·3D', '저장 지점·검사·배포')]
    b = ''
    for i, (t, a, c, d) in enumerate(cols):
        x = 10 + i*226; on = i == 1
        b += box(x, 10, 210, 170, MARK if i == 1 else ('#fff' if i == 0 else SOFT), INK, 12, 1.5)
        b += text(x+105, 44, t, 19, '800') + text(x+105, 70, a, 12.5, '600', ACC)
        b += f'<line x1="{x+20}" y1="86" x2="{x+190}" y2="86" stroke="{LINE}"/>'
        b += text(x+105, 112, '잘 맞는 일', 10.5, '600', MUTED) + text(x+105, 132, c, 12) + text(x+105, 160, d, 11.5, '500', MUTED)
    b += text(340, 208, '결과가 문서면 Cowork · 계속 고쳐 쓸 앱·사이트면 클로드 코드 · 짧은 질문은 채팅', 12.5, '700', ACC)
    return svg(690, 220, b, '세 도구 비교')
F['tools'] = [('after_intro', fig(tools(), '같은 클로드, 세 가지 쓰임. 하고 싶은 일의 결과물로 고릅니다.'))]

# ---------- Pro 사용량 ----------
def usage():
    b = text(10, 22, '사용량은 한 통을 같이 씁니다', 14, '700', INK, 'start')
    segs = [('채팅', 0.22, '#fff'), ('Cowork', 0.3, MARK), ('클로드 코드', 0.33, SOFT), ('남은 양', 0.15, PAPER)]
    x = 10
    for t, f, c in segs:
        w = 660*f; b += box(x, 36, w, 46, c, INK, 4, 1.2) + text(x+w/2, 64, t, 12.5, '600'); x += w
    b += text(10, 108, '5시간마다 다시 채워짐  +  일주일 한도 따로', 12.5, '600', ACC, 'start')
    for i in range(7):
        b += box(10+i*94, 122, 86, 30, SOFT if i < 4 else '#fff', LINE, 4) + text(53+i*94, 142, ['월', '화', '수', '목', '금', '토', '일'][i], 12)
    b += text(680, 172, '여러 에이전트(팀)는 일꾼마다 따로 써서 몇 배로 늘어납니다', 11.5, '500', WARN, 'end')
    return svg(690, 182, b, '사용량 구조')

# ---------- 메뉴 지도 (개략도: 실제 데스크톱 앱 메뉴 이름 그대로) ----------
DARK, DARK2, DTXT, DMUT, BLUE = '#1E1F1E', '#2A2B2A', '#ECECEA', '#A3A6A2', '#3B82F6'
def dtext(x, y, t, size=12, w='500', fill=None, anchor='start'):
    return text(x, y, t, size, w, fill or DTXT, anchor)
def dwin(w, h, title, inner):
    b = box(2, 2, w-4, h-4, DARK, '#444', 10, 1.4) + dtext(20, 28, title, 14, '700') + dtext(w-24, 28, '✕', 14, '500', DMUT, 'end')
    b += f'<line x1="2" y1="42" x2="{w-2}" y2="42" stroke="#3a3a3a"/>'
    return svg(w, h, b + inner, title)
NAV = [('환경설정', None), ('일반', 0), ('계정', 0), ('개인정보보호', 0), ('사용량', 0), ('기능', 0), ('메모리', 0), ('디자인 시스템', 0), ('Claude Code', 0), ('Cowork', 0),
       ('이 컴퓨터', None), ('시스템', 0), ('확장 프로그램', 0), ('개발자', 0), ('사용자 지정', None), ('Skills', 0), ('커넥터', 0), ('플러그인', 0)]
def settings_nav(sel, h):
    b = box(12, 52, 170, h-62, DARK, '#333', 6) + box(22, 60, 150, 24, DARK2, '#3a3a3a', 6) + dtext(34, 77, '검색', 11, '500', DMUT)
    y = 104
    for t, k in NAV:
        if k is None: b += dtext(26, y, t, 10.5, '600', DMUT); y += 20; continue
        if t == sel: b += box(20, y-15, 156, 22, '#33363a', BLUE, 6, 1.4)
        b += dtext(34, y, t, 11.5, '600' if t == sel else '500'); y += 21
    return b
def settings_usage():
    w, h = 690, 470; b = settings_nav('사용량', h)
    b += dtext(200, 76, '사용 한도', 15, '800')
    def bar(y, t, s, pct):
        r = dtext(200, y, t, 12.5, '600') + dtext(200, y+18, s, 10.5, '500', DMUT)
        r += box(410, y-4, 200, 6, '#3a3a3a', '#3a3a3a', 3) + box(410, y-4, max(6, 200*pct/100), 6, BLUE, BLUE, 3) + dtext(676, y+2, f'{pct}% 사용됨', 11, '500', DMUT, 'end')
        return r
    b += bar(112, '현재 세션', '오후 ○시에 초기화 (5시간 단위)', 11)
    b += dtext(200, 170, '주간 한도', 15, '800') + dtext(200, 192, '사용량 제한에 대해 더 알아보기', 11, '500', '#6EA8FE')
    b += bar(226, '모든 모델', '(요일) 오후 ○시에 초기화', 2)
    b += bar(276, 'Fable', '(요일) 오후 ○시에 초기화', 25)
    b += dtext(200, 330, '제한 초기화', 15, '800') + dtext(200, 354, '현재 초기화 없음', 12, '600') + dtext(200, 372, '받으시면 만료일과 함께 여기에 표시됩니다.', 10.5, '500', DMUT)
    b += callout(1, 186, 104) + callout(2, 186, 162) + callout(3, 400, 268)
    return dwin(w, h, '설정', b)
def settings_connectors():
    w, h = 690, 470; b = settings_nav('커넥터', h)
    b += dtext(200, 80, '커넥터', 17, '800') + box(272, 62, 112, 26, DARK2, '#444', 6) + dtext(282, 80, '내 항목', 11.5, '700') + dtext(336, 80, '탐색', 11.5, '500', DMUT)
    b += box(600, 62, 76, 26, '#F4F4F2', '#F4F4F2', 6) + text(638, 80, '+ 추가 ▾', 11.5, '700', '#1E1F1E')
    for i, c in enumerate(['커넥터', '유형', '인증', '상태']): b += dtext([200, 400, 490, 600][i], 112, c, 10.5, '600', DMUT)
    rows = [('Canva', '웹', '개인별', '✓'), ('Claude in Chrome', '데스크톱', '—', '✓'), ('GitHub 통합', '웹', '개인별', '✓'), ('Gmail', '웹', '개인별', '✓'), ('Google Calendar', '웹', '개인별', '✓'), ('Notion', '웹', '개인별', '✓'), ('Adobe', '웹', '—', '연결'), ('Microsoft 365', '웹', '—', '연결')]
    for i, r in enumerate(rows):
        y = 140+i*36
        if i == 0: b += box(194, y-20, 486, 32, '#2f3a2f', '#F3D34A', 6, 1.4)
        b += f'<line x1="194" y1="{y+14}" x2="680" y2="{y+14}" stroke="#333"/>'
        for j, v in enumerate(r):
            if j == 3 and v == '연결': b += box(596, y-14, 46, 22, '#3a3a3a', '#3a3a3a', 5) + dtext(619, y+1, v, 11, '600', DTXT, 'middle')
            else: b += dtext([200, 400, 490, 606][j], y, v, 12 if j == 0 else 11, '600' if j == 0 else '500', DTXT if j == 0 else DMUT)
    b += callout(1, 184, 401) + callout(2, 266, 52) + callout(3, 588, 52) + callout(4, 186, 128)
    return dwin(w, h, '설정', b)
def main_window():
    w, h = 690, 400; b = box(2, 2, w-4, h-4, DARK, '#444', 10, 1.4)
    b += box(2, 2, 150, h-4, '#191a19', '#333', 10)
    b += dtext(14, 28, '☰  ◧', 12, '500', DMUT) + box(84, 10, 62, 26, '#33363a', BLUE, 6) + dtext(115, 28, 'Code', 12, '700', DTXT, 'middle')
    for i in range(8): b += box(14, 48+i*26, 124, 16, '#262726', '#262726', 4)
    b += dtext(14, 268, '(세션 목록)', 10, '500', DMUT)
    b += box(8, 288, 138, 104, '#262726', '#3a3a3a', 8)
    for i, t in enumerate(['⚙ 설정   Ctrl+,', '◎ 언어', '? 도움 받기', '… 더 알아보기']): b += dtext(18, 308+i*22, t, 11, '600' if i == 0 else '500')
    b += dtext(164, 28, '세션 제목 ▾', 12, '700')
    b += box(164, 46, 330, 270, DARK, DARK, 6) + dtext(180, 80, '대화·작업 내용', 12, '500', DMUT)
    b += box(164, 330, 330, 34, '#262726', '#444', 10) + dtext(178, 351, '+   Enter 키로 보내기', 11, '500', DMUT)
    b += dtext(494, 384, '모델 ▾ · 노력 · 권한 모드', 10.5, '600', DMUT, 'end')
    b += box(506, 46, 172, 340, '#191a19', '#333', 8)
    for i, t in enumerate(['환경 (작업 폴더·저장소)', '컨텍스트 (사용량 %)', '커넥터', '결과물', '변경 사항']): b += dtext(516, 74+i*58, t, 11.5, '700') + box(516, 82+i*58, 150, 20, '#262726', '#262726', 4)
    b += callout(1, 124, 48) + callout(2, 146, 300) + callout(3, 494, 340) + callout(4, 500, 70)
    return svg(w, h, b, 'Claude 데스크톱 앱 Code 화면')
F['menus'] = [('after_intro', fig(main_window(), '데스크톱 앱 Code 화면의 개략도. ① 모드 전환(왼쪽 위 아이콘 묶음: 채팅·Cowork·Code, 지금은 Code 선택) ② 왼쪽 아래 계정 메뉴 → 설정(Ctrl+,) ③ 입력창 아래 모델·권한 모드 ④ 오른쪽 패널: 작업 폴더, 컨텍스트, 커넥터, 결과물, 변경 사항.', 'mock')),
              ('before:h3:설정 창', fig(settings_connectors(), '설정 창 개략도(실제 메뉴 이름). ① 사용자 지정 › 커넥터 ② 내 항목/탐색 ③ + 추가 ④ Canva가 "개인별·✓"면 연결된 것.', 'mock')),
              ('before:h3:사용량', fig(settings_usage(), '설정 › 사용량 개략도. ① 현재 세션(5시간마다 초기화) ② 주간 한도 ③ Fable 같은 모델별 막대. 팀 요금제 화면을 바탕으로 그린 개략도라, 요금제·앱 버전에 따라 항목이 다를 수 있습니다.', 'mock'))]
# ---------- 세팅 ----------
def mcp():
    b = box(255, 80, 180, 70, MARK, INK, 14, 1.6) + text(345, 112, '클로드', 18, '800') + text(345, 134, '(채팅·Cowork·코드)', 11, '500', MUTED)
    tools_ = [('Canva', '디자인 만들기·내보내기', 40, 20), ('한글(HWPX)', '문서 편집·자동화', 40, 160), ('Google 드라이브 등', '파일 읽기', 500, 20), ('내 PC 프로그램', '플러그인으로 설치', 500, 160)]
    for t, s, x, y in tools_:
        b += box(x, y, 150, 56, '#fff', INK, 10) + text(x+75, y+24, t, 13, '700') + text(x+75, y+43, s, 10.5, '400', MUTED)
        cx = x+150 if x < 300 else x; cy = y+28
        b += f'<line x1="{cx}" y1="{cy}" x2="{255 if x<300 else 435}" y2="{115}" stroke="{ACC}" stroke-width="2" stroke-dasharray="5 4"/>'
        b += f'<rect x="{(cx+(255 if x<300 else 435))/2-14}" y="{(cy+115)/2-8}" width="28" height="16" rx="3" fill="{ACC}"/>' + text((cx+(255 if x<300 else 435))/2, (cy+115)/2+4, 'MCP', 9, '700', '#fff')
    b += text(345, 236, 'MCP = 클로드와 다른 도구를 잇는 공통 플러그(공개 표준)', 12.5, '700', ACC)
    return svg(690, 248, b, 'MCP 개념')

def connectors_mock():
    w, h = 690, 230; b = ''
    b += text(20, 56, '사용자 지정 › 커넥터', 14, '700', INK, 'start') + box(540, 38, 130, 28, ACC, ACC, 14) + text(605, 57, '+ 커넥터 찾기', 12, '700', '#fff')
    for i, (t, s, st) in enumerate([('Canva', '디자인 검색·만들기·자동 채우기·내보내기', '연결'), ('Google Drive', '파일 찾기·읽기', '연결됨'), ('Gmail', '메일 찾기·초안', '연결 안 함')]):
        y = 80+i*46; b += box(20, y, 650, 38, MARK if i == 0 else '#fff', LINE, 6)
        b += text(36, y+24, t, 13, '700', INK, 'start') + text(160, y+24, s, 11.5, '400', MUTED, 'start')
        b += box(578, y+7, 80, 24, ACC if i == 0 else '#fff', ACC, 12) + text(618, y+24, st, 11.5, '700', '#fff' if i == 0 else ACC)
    b += callout(1, 532, 52) + callout(2, 570, 92)
    return window(w, h, 'Claude 앱 › 사용자 지정 (개략도)', b)

def terminal():
    rows = [('① uv 설치 (한 번만, Windows)', 'winget install --id=astral-sh.uv -e'),
            ('② 한글 플러그인 목록 추가', 'claude plugin marketplace add airmang/hwpx-plugins'),
            ('③ 한글 플러그인 설치', 'claude plugin install hwpx-plugin@hwpx')]
    b = ''
    for i, (t, c) in enumerate(rows):
        y = 8+i*62
        b += text(6, y+16, t, 12.5, '700', INK, 'start')
        b += box(2, y+24, 686, 30, '#1F2624', INK, 6) + f'<text x="16" y="{y+44}" font-size="12.5" fill="{MARK}" font-family="\'IBM Plex Mono\',monospace">{esc(c)}</text>'
    b += text(6, 204, '한 상자에 한 줄씩, 순서대로 붙여 넣고 Enter. 다 끝나면 클로드 코드를 새로 시작합니다.', 12, '600', ACC, 'start')
    return svg(690, 214, b, '한글 플러그인 설치 순서')

def git_line():
    pts = [('월', '첫 화면'), ('화', '주차 이동'), ('수', '당겨오기'), ('목', '충돌 검사'), ('오늘', '망가짐?')]
    b = f'<line x1="40" y1="70" x2="650" y2="70" stroke="{INK}" stroke-width="3"/>'
    for i, (d, t) in enumerate(pts):
        x = 60+i*145; last = i == 4
        b += f'<circle cx="{x}" cy="70" r="14" fill="{WARN if last else ACC}"/>' + text(x, 75, '✕' if last else '✓', 13, '700', '#fff')
        b += text(x, 42, d, 12, '700') + text(x, 104, t, 12, '500', MUTED)
    b += f'<path d="M640,118 C610,170 520,170 497,120" fill="none" stroke="{WARN}" stroke-width="2" marker-end="url(#ah)"/>' + text(568, 190, '"어제 잘 되던 때로 되돌려 줘"', 12.5, '700', WARN)
    b += text(14, 222, 'Git = 저장 지점(커밋)을 남기는 도구  ·  GitHub = 그 기록을 인터넷(비공개 저장소)에 보관', 12, '600', ACC, 'start')
    return svg(690, 232, b, 'Git 저장 지점')

def firebase():
    return flow([('내 작업 폴더', 'index.html 등'), ('올리기 전 검사', '개인정보·파일 종류'), ('올리기 명령', 'firebase deploy'), ('웹 주소', '이름.web.app'), ('학생·동료', '링크로 열기')], [2])
F['setup'] = [('after_intro', fig(mcp(), 'MCP는 클로드에 다른 도구를 꽂는 플러그입니다. 커넥터와 플러그인이 이 방식으로 연결됩니다.')),
              ('after:h3:2. 캔바', fig(settings_connectors(), '설정 › 사용자 지정 › 커넥터. 탐색에서 Canva를 찾아 연결하고 캔바에 로그인하면 내 항목에 "개인별 ✓"로 보입니다.', 'mock')),
              ('before:h3:한글', fig(terminal(), '한글 플러그인 설치 순서(보기용 그림). 실제로 복사할 때는 본문의 명령 상자를 쓰세요. 클로드 코드 대화창에 이 명령을 실행해 달라고 맡겨도 됩니다. 캔바 연결 명령은 캔바 절에 따로 있습니다.')),
              ('before:h3:Git', fig(git_line(), '저장 지점이 있으면 망가져도 잘 되던 때로 돌아갈 수 있습니다.')),
              ('after:h3:5. Firebase', fig(firebase(), '웹을 Firebase에 올리는 흐름. 올린 주소는 누구나 열 수 있습니다.'))]

# ---------- EP0 Cowork 개략도 ----------
def cowork_mock():
    w, h = 690, 290; b = ''
    b += box(14, 40, 300, 236, PAPER, LINE, 6) + text(28, 64, '작업 폴더', 12.5, '700', INK, 'start')
    for i, t in enumerate(['📁 클로드작업', '   📁 가정통신문_11월', '      📄 양식.hwpx', '      📄 메모.txt', '      📄 가정통신문_공개수업.hwpx  ← 새로 생김']):
        b += text(28, 92+i*24, t.replace('📁', '▸').replace('📄', '·'), 12, '700' if '새로' in t else '500', ACC if '새로' in t else INK, 'start')
    b += box(326, 40, 350, 236, '#fff', LINE, 6) + text(340, 64, '진행 상황', 12.5, '700', INK, 'start')
    for i, (t, d) in enumerate([('양식 읽기', 1), ('메모에서 날짜·장소 찾기', 1), ('빈칸 [  ] 표시', 1), ('새 파일로 저장', 1), ('확인할 곳 목록 만들기', 0)]):
        y = 92+i*28; b += box(340, y-14, 18, 18, ACC if d else '#fff', ACC, 4) + (text(349, y, '✓', 12, '700', '#fff') if d else '')
        b += text(368, y, t, 12, '500', INK if d else MUTED, 'start')
    b += box(340, 236, 322, 30, MARK, INK, 15) + text(501, 256, '지우기 전에 허락을 묻습니다. 그래도 복사본부터', 11.5, '700')
    b += callout(1, 300, 52) + callout(2, 662, 52)
    return window(w, h, 'Cowork (개략도)', b)
F['ep0'] = [('after_intro', fig(cowork_mock(), '① 맡긴 폴더 안에 결과 파일이 생깁니다 ② 클로드가 하는 일을 단계별로 보여 줍니다.', 'mock'))]

# ---------- 문서 업무 ----------
F['ep1'] = [('after_intro', fig(flow([('양식 + 메모', '.hwpx · .txt'), ('Cowork에 맡기기', '한 문단 요청'), ('새 가정통신문', '원본은 그대로'), ('사람이 확인', '날짜·숫자·담당자')], [1]), '가정통신문 흐름'))]
F['ep2'] = [('after_intro', fig(flow([('반별 엑셀 7개', '가명 처리본'), ('합치기', '열 맞추기'), ('이상한 줄 표시', '중복·빈칸·오타'), ('통합 + 합계', '확인필요 시트'), ('줄 수 대조', '사람이 확인')], [2]), '엑셀 합치기 흐름'))]
F['ep3'] = [('after_intro', fig(flow([('공문 PDF', '여러 개도 됨'), ('내 일만 뽑기', '담임 기준'), ('할 일 표', '마감일 순 · 근거 쪽수'), ('쪽수 열어 확인', '두세 개만')], [2]), '공문 정리 흐름'))]
F['ep4'] = [('after_intro', fig(flow([('양식 + 명단', '가명으로 연습'), ('먼저 두 장', '모양 확인'), ('고칠 점 말하기', '자리·글꼴'), ('나머지 전부', '한 파일, 쪽 나눔')], [1]), '대량 작업은 먼저 두 장만'))]
F['ep5'] = [('after_intro', fig(flow([('정리 계획만', '종류·개수·용량 표'), ('규칙 확정', '사람이 정함'), ('20개만 옮겨 보기', '확인'), ('전부 옮기기', '지우지 말고 모으기'), ('정리 보고서', '되돌리기 쉽게')], [1]), '다운로드·음악 폴더 정리 흐름. 지우지 않고 모으기만 하는 것이 원칙입니다.')), ('after:h3:PC 설정', fig(flow([('반복하던 설정', '손으로 매번'), ('조건 말하기', '권한 없이·건너뛰기'), ('스크립트 파일', '사용법 주석'), ('오른쪽 클릭 → 실행', '다른 PC에서도')], [2]), 'PC 설정 자동화 흐름'))]

# ---------- 시간표 ----------
def merge():
    b = ''
    for i, (t, s, c) in enumerate([('기본 시간표', '교사 × 요일 × 교시', '#fff'), ('학사일정', '휴업일·시험·행사', SOFT), ('변경 기록', '당겨오기 등', MARK)]):
        y = 14+i*70; b += box(10, y, 200, 56, c, INK, 10) + text(110, y+25, t, 14, '700') + text(110, y+44, s, 11, '400', MUTED)
        b += arrow(212, y+28, 300, 112)
    b += box(304, 64, 150, 96, ACC, ACC, 12) + text(379, 104, '합치기', 17, '800', '#fff') + text(379, 128, '순서: 기본 → 일정 → 변경', 10.5, '500', '#fff')
    b += arrow(456, 112, 500, 112)
    b += box(504, 40, 176, 144, '#fff', INK, 10) + text(592, 64, '이번 주 진짜 시간표', 12.5, '700')
    cells = [['창경', '공강', '시험'], ['공학', '행사', '시험'], ['당겨옴', '창경', '시험']]
    for r in range(3):
        for c in range(3):
            v = cells[r][c]; col = {'시험': SOFT, '행사': PAPER, '당겨옴': MARK}.get(v, '#fff')
            b += box(516+c*54, 76+r*34, 50, 30, col, LINE, 4) + text(541+c*54, 96+r*34, v, 11, '600')
    return svg(690, 226, b, '시간표 합치기')
F['ep6'] = [('after_intro', fig(merge(), '세 가지 데이터를 정해진 순서로 합쳐 주차별 시간표를 만듭니다.')),
            ('end', '<figure class="shot"><img src="img/submon-week.png" alt="발표자 시간표 화면"><figcaption><b>실제 화면</b> 발표자 앱의 주간 시간표. 정기고사 주간이라 시험이 크게 표시되고, "수업 · 당겨오기" 칸이 보입니다(교사 이름은 가렸습니다).</figcaption></figure>')]

def dangyeo():
    def grid(x, title, marks):
        b = text(x+150, 22, title, 14, '800')
        days = ['월', '화', '수', '목', '금']
        for c, d in enumerate(days): b += text(x+52+c*52, 46, d, 12, '700', MUTED)
        for r in range(4):
            b += text(x+12, 72+r*36, f'{r+4}교시', 10.5, '600', MUTED, 'start')
            for c in range(5):
                v = marks.get((r, c), ''); col = {'당겨옴': MARK, '당겨 감': PAPER, '축제': SOFT, '3반': '#fff'}.get(v, '#fff')
                b += box(x+28+c*52, 54+r*36, 48, 30, col, INK if v in ('당겨옴', '당겨 감') else LINE, 4, 1.4 if v else 1) + text(x+52+c*52, 74+r*36, v, 10.5, '700' if v else '400')
        return b
    b = grid(0, '당기기 전', {(1, 4): '축제', (1, 1): '', (2, 3): '3반', (0, 0): '3반', (3, 4): '3반'})
    b += grid(360, '당긴 뒤', {(1, 4): '축제', (1, 1): '당겨옴', (2, 3): '3반', (0, 0): '3반', (3, 4): '당겨 감'})
    b += arrow(312, 130, 352, 130)
    b += text(345, 214, '금요일 축제로 빠질 3반 수업을 화요일 5교시(내 공강·3반 빈 시간)로 미리 당겨 옵니다 (예시)', 11.5, '600', ACC)
    return svg(690, 224, b, '수업 당겨오기 전후')
F['ep7'] = [('after_intro', fig(dangyeo(), '당겨 온 칸은 "당겨옴", 원래 칸은 "당겨 감"으로 표시하고 언제든 되돌릴 수 있게 만듭니다.'))]
F['ep8'] = [('after_intro', fig(flow([('일정 붙여 넣기', '다시 계산'), ('저장·불러오기', '변경 기록 파일'), ('학교 안 나누기', '파일로 공유'), ('(선택) 웹에 올리기', 'Firebase + 입장 코드'), ('다른 앱으로', '넓히기')], [3]), '학교 일정과 함께 쓰는 흐름. 웹에 올리는 것은 학교가 허용한 경우에만 입장 코드와 함께.')),
            ('end', '<figure class="shot"><img src="img/submon-hub.png" alt="SUB모니터 화면"><figcaption><b>실제 화면</b> 발표자의 SUB모니터. 시간표 사이트의 계산 결과를 가져와 시계·날씨·시간표·학교 일정·쪽지를 한 줄에 띄웁니다(교사 이름·쪽지·일정 내용은 가렸습니다).</figcaption></figure>')]

# ---------- 인정점 ----------
F['ep9'] = [('after_intro', fig(flow([('학업성적관리규정', 'PDF · hwpx'), ('계산 규칙표', '근거 조항 달기'), ('확인필요 항목', '클로드가 정하지 않음'), ('사람이 확정', '담당자·위원회')], [1]), '규정을 규칙표로'))]
F['ep10'] = [('after_intro', fig(flow([('확정된 규칙표', ''), ('가짜 학생 20명', '학생01~20'), ('인정점.html', '브라우저 안에서만'), ('계산 근거 열', '점수 × 비율'), ('실제 점수', '내 PC에서만')], [2]), '인정점 프로그램 흐름'))]
def check():
    rows = [('학생02', '24.0', '24.0'), ('학생04', '25.1', '25.1'), ('학생07', '42.0', '42.0'), ('학생11', '36.8', '36.7')]
    b = text(20, 24, '정답표(손계산) ↔ 프로그램 결과 자동 비교 (예시)', 13.5, '700', INK, 'start')
    for i, h in enumerate(['학생', '손계산', '프로그램', '결과']): b += text(80+i*170, 54, h, 12, '700', MUTED)
    for r, (n, a, p) in enumerate(rows):
        ok = a == p; y = 64+r*34
        b += box(10, y, 670, 30, '#fff' if ok else '#FBEAE2', LINE, 4)
        for i, v in enumerate([n, a, p, '통과' if ok else '다름 → 고치기']): b += text(80+i*170, y+20, v, 12.5, '700' if not ok else '500', WARN if (not ok and i >= 2) else INK)
    return svg(690, 206, b, '검산')
F['ep11'] = [('after_intro', fig(check(), '사람이 계산한 정답과 프로그램 결과가 하나라도 다르면 실패로 알려 줍니다. 학생11의 36.7은 반올림 대신 버림을 쓴 버그를 가정한 예시입니다(EP 11 정답표와 같은 숫자).'))]

# ---------- 사이트·캔바·3D ----------
def sitemap():
    b = box(225, 8, 240, 50, MARK, INK, 10) + text(345, 32, '단원 첫 화면', 15, '800') + text(345, 50, 'index.html', 10.5, '500', MUTED)
    for k in range(4):
        x = 30+k*162; b += f'<line x1="345" y1="58" x2="{x+70}" y2="92" stroke="{ACC}" stroke-width="2"/>'
        b += box(x, 92, 140, 92, '#fff', INK, 8) + text(x+70, 114, f'{k+1}차시 페이지', 13, '700')
        for r, t in enumerate(['학습 목표·핵심 개념', '활동 안내·확인 퀴즈', '활동지 내려받기']): b += text(x+70, 136+r*16, t, 10, '500', MUTED)
    b += box(60, 200, 570, 30, PAPER, LINE, 6) + text(345, 220, '실습은 여기까지(단원 하나). 익숙해지면 단원·교과서를 늘려 입구 페이지로 묶습니다.', 11.5, '600', ACC)
    return svg(690, 238, b, '사이트 지도')
F['ep12'] = [('after_intro', fig(sitemap(), '실습 결과의 모양: 단원 첫 화면 하나와 차시 페이지 여러 개. 발표자처럼 교과서별 입구로 넓히는 것은 익숙해진 다음입니다.'))]
F['ep13'] = [('after_intro', fig(flow([('차시 핵심 개념', 'EP 12 사이트'), ('캔바 커넥터', '세팅 장에서 연결'), ('캔바 슬라이드', '클로드가 초안'), ('사람이 다듬기', '캔바에서'), ('내보내기', 'PNG·PDF → 사이트')], [2]), '캔바 활용 흐름'))]
def three_d():
    b = flow([('말로 설명', '모양 + 치수(mm)'), ('OpenSCAD 코드', '치수는 숫자로'), ('미리보기·STL', 'OpenSCAD'), ('슬라이서', 'Bambu Studio·Cura'), ('출력 → 재기', '치수 고쳐 다시')], [1])
    return b
def scad_sample():
    code = ['// 책상 명패 (예시) — 숫자만 바꾸면 크기가 바뀝니다', '가로 = 90;  세로 = 30;  두께 = 3;', '글자 = "김하늘";  글자크기 = 10;  글자돌출 = 1.5;', '', 'cube([가로, 세로, 두께]);                 // 바탕판', 'translate([8, 14, 두께])', '  linear_extrude(글자돌출) text(글자, size = 글자크기);']
    b = box(2, 2, 336, 186, '#1F2624', INK, 10)
    for i, l in enumerate(code): b += f'<text x="16" y="{30+i*22}" font-size="11.5" fill="{MARK if l.startswith("//") else "#E3EAE6"}" font-family="\'IBM Plex Mono\',monospace">{esc(l)}</text>'
    # 명패 그림 (등각 느낌)
    b += f'<polygon points="380,130 600,130 660,90 440,90" fill="{SOFT}" stroke="{INK}" stroke-width="1.5"/>'
    b += f'<polygon points="380,130 600,130 600,146 380,146" fill="#BFD8D1" stroke="{INK}" stroke-width="1.5"/><polygon points="600,130 660,90 660,106 600,146" fill="#A9CBC2" stroke="{INK}" stroke-width="1.5"/>'
    b += text(520, 116, '김하늘', 15, '800', ACC)
    b += text(520, 176, '바탕판 위에 글자가 1.5mm 솟음', 11.5, '500', MUTED)
    return svg(690, 192, b, 'OpenSCAD 예시')
F['ep14'] = [('after_intro', fig(three_d(), '클로드는 모양을 깎는 대신 치수가 담긴 코드를 씁니다.')),
             ('before:h3:따라', fig(scad_sample(), 'OpenSCAD 코드와 결과 모양(예시 개략도). 숫자를 바꿔 달라고 말하면 크기가 바뀝니다.', 'mock'))]

# ---------- 점검 ----------
def loop():
    pts = [('① 직접 써 보기', '캡처·메모'), ('② 점검 목록 받기', '심각/보통/사소'), ('③ 하나만 고치기', '원인부터'), ('④ 확인하기', '무엇을 눌러?'), ('⑤ 저장 지점', '커밋')]
    import math; b = ''
    cx, cy, R = 345, 128, 96
    for i, (t, s) in enumerate(pts):
        a = -math.pi/2 + i*2*math.pi/5; x = cx+R*1.9*math.cos(a); y = cy+R*math.sin(a)
        b += box(x-74, y-26, 148, 52, MARK if i == 2 else '#fff', INK, 10) + text(x, y-2, t, 13, '700') + text(x, y+16, s, 10.5, '400', MUTED)
    b += text(cx, cy-4, '한 바퀴씩', 15, '800', ACC) + text(cx, cy+18, '①→②→③→④→⑤→①', 12, '700', ACC)
    return svg(690, 256, b, '점검 순환')
F['ep15'] = [('after_intro', fig(loop(), '한 번에 하나씩 고치고, 잘 되면 저장 지점을 남기는 순서를 반복합니다.'))]
F['ep16'] = [('after_intro', '<figure class="shot"><img src="img/sim.png" alt="손목 컨트롤러 시뮬레이터"><figcaption><b>실제 화면</b> 발표자의 손목 컨트롤러 웹 시뮬레이터. 시계가 없어도 시계 화면·가상 PC·보낸 키 기록을 볼 수 있게 먼저 만들었습니다.</figcaption></figure>')]


# ---------- 1차 검토 그림 요청(개략도) ----------
def win_light(w, h, title, inner):
    return window(w, h, title, inner)
def permission_mock():
    w, h = 690, 230; b = ''
    b += text(24, 62, '클로드: 진짜시간표.html 파일을 새로 만들겠습니다.', 13, '500', INK, 'start')
    b += box(20, 78, 650, 132, SOFT, ACC, 10, 1.6)
    b += text(36, 104, '이 작업을 해도 될까요?', 14, '800', INK, 'start')
    b += text(36, 128, '파일 만들기: 바탕 화면 › 클로드작업 › 시간표 › 진짜시간표.html', 12, '500', MUTED, 'start')
    for i, (t, c) in enumerate([('허락', ACC), ('항상 허락', '#fff'), ('거절', '#fff')]):
        b += box(36+i*150, 148, 136, 36, c, ACC, 18, 1.4) + text(104+i*150, 171, t, 13, '700', '#fff' if i == 0 else ACC)
    b += text(500, 171, '← 잘 모르면 "거절" 후 질문', 11.5, '600', WARN, 'start')
    b += callout(1, 36, 104) + callout(2, 104, 144)
    return window(w, h, '허락 질문 (개략도)', b)
def saveas_mock():
    w, h = 690, 250; b = ''
    b += text(24, 60, '한글 › 파일 › 다른 이름으로 저장하기', 13, '700', INK, 'start')
    b += box(24, 74, 640, 34, '#fff', LINE, 6) + text(36, 96, '파일 이름:  양식', 12.5, '500', INK, 'start')
    b += box(24, 116, 640, 34, MARK, INK, 6, 1.6) + text(36, 138, '파일 형식:  HWPX 문서 (*.hwpx)', 12.5, '700', INK, 'start') + box(600, 120, 58, 26, '#fff', INK, 4) + text(629, 138, '▼', 13, '700') + text(596, 106, '여기를 눌러 고르세요 →', 11, '700', WARN, 'end')
    b += box(560, 160, 104, 30, ACC, ACC, 15) + text(612, 180, '저장', 12.5, '700', '#fff')
    b += text(24, 222, '탐색기 › 보기 › 표시 › "파일 확장명" 켜기 → 양식.hwpx 처럼 끝의 확장자가 보입니다', 12, '600', ACC, 'start')
    b += callout(1, 680, 132) + callout(2, 14, 216)
    return window(w, h, '파일 형식 바꾸기 (개략도)', b)
def terminal_open_mock():
    w, h = 690, 240; b = ''
    b += box(20, 44, 300, 182, PAPER, LINE, 8) + box(32, 56, 276, 30, '#fff', INK, 15) + text(46, 76, '🔍 터미널'.replace('🔍', '검색:'), 12.5, '600', INK, 'start')
    b += box(32, 96, 276, 52, MARK, INK, 8, 1.4) + text(46, 118, '터미널 (Windows Terminal)', 12.5, '700', INK, 'start') + text(46, 138, '또는 PowerShell', 11, '500', MUTED, 'start')
    b += text(32, 176, '① 키보드의 Windows 키 누르기', 11.5, '500', INK, 'start') + text(32, 198, '② "터미널" 입력 → 맨 위 결과 클릭', 11.5, '500', INK, 'start')
    b += arrow(324, 122, 360, 122)
    b += box(366, 44, 300, 182, '#1F2624', INK, 8)
    b += f'<text x="380" y="78" font-size="12" fill="#9FB0A9" font-family="\'IBM Plex Mono\',monospace">PS C:\\Users\\교사&gt;</text>'
    b += f'<text x="380" y="104" font-size="12" fill="{MARK}" font-family="\'IBM Plex Mono\',monospace">여기에 명령 붙여 넣기</text>'
    b += text(380, 150, '붙여 넣기: 마우스 오른쪽 클릭', 11.5, '600', '#E3EAE6', 'start') + text(380, 172, '실행: Enter', 11.5, '600', '#E3EAE6', 'start') + text(380, 200, '$ 기호는 치지 않습니다', 11.5, '700', '#F0A184', 'start')
    return svg(690, 240, b, '터미널 여는 법')
def rightclick_mock():
    w, h = 690, 210; b = ''
    b += box(20, 20, 220, 40, '#fff', INK, 6) + text(36, 46, '▣ 정리.ps1', 13, '700', INK, 'start')
    b += text(250, 46, '← 파일을 마우스 오른쪽 클릭', 12, '600', WARN, 'start')
    b += box(60, 70, 300, 130, '#fff', INK, 8, 1.4)
    for i, (t, on) in enumerate([('열기', 0), ('PowerShell에서 실행', 1), ('편집', 0), ('더 많은 옵션 표시', 0)]):
        y = 96+i*28
        if on: b += box(66, y-18, 288, 26, MARK, INK, 5)
        b += text(80, y, t, 12.5, '700' if on else '500', INK, 'start')
    b += text(380, 120, 'Windows 11에서 안 보이면', 12, '700', INK, 'start') + text(380, 142, '"더 많은 옵션 표시"를 먼저 누릅니다', 12, '500', MUTED, 'start') + text(380, 172, '학교 PC는 실행이 막혀 있을 수 있음 →', 12, '500', MUTED, 'start') + text(380, 192, '정보 담당 선생님께 문의', 12, '600', WARN, 'start')
    return svg(690, 210, b, 'PowerShell 스크립트 실행')
F['ep0'] = F.get('ep0', []) + [('after:h3:허락 질문 읽는 법', fig(permission_mock(), '① 클로드가 무엇을 하려는지 읽고 ② 허락·항상 허락·거절 중 고릅니다. 파일을 지우거나 보내는 일이면 꼭 다시 읽습니다. 버튼 이름은 버전마다 조금 다릅니다.', 'mock')),
                               ('before:h3:확장자', fig(saveas_mock(), '① 한글에서 파일 형식을 HWPX로 골라 저장 ② 탐색기에서 확장명을 켜면 파일 이름 끝(.hwpx, .txt)이 보입니다.', 'mock'))]
F['setup'] = F.get('setup', []) + [('after:h3:터미널이란', fig(terminal_open_mock(), '터미널(검은 명령 창) 여는 법과 명령 붙여 넣는 법. 학교 PC는 설치가 막혀 있을 수 있습니다.', 'mock'))]
F['ep5'] = F.get('ep5', []) + [('after:h3:PC 설정', fig(rightclick_mock(), '.ps1 스크립트 실행하기. 메뉴 이름은 Windows 버전에 따라 다릅니다.', 'mock'))]

F['pro'] = [('after_intro', fig(usage(), '채팅·Cowork·클로드 코드가 같은 사용량을 나눠 씁니다. 그림의 비율은 예시입니다.')), ('before:h3:사용량을 아끼는', fig(settings_usage(), '설정 › 사용량 개략도(팀 요금제 화면을 바탕으로 그림). ① 현재 세션 막대가 가장 중요합니다 ② 주간 한도 ③ 모델별 막대. 화면 표시는 요금제·앱 버전마다 다릅니다. Fable은 Claude 모델 이름 중 하나입니다. 요금 안내 기준으로 Pro에서는 사용 크레딧으로 씁니다(2026년 11월 기준). 성능 차이는 이 책에서 다루지 않으며, Pro 화면에는 이 막대가 없을 수 있습니다.', 'mock'))]
json.dump(F, open(os.path.join(D, 'figs.json'), 'w', encoding='utf8'), ensure_ascii=False)
print(len(F), 'sections,', sum(len(v) for v in F.values()), 'figures')
