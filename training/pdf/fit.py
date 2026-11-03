# 장 끝 꼬리 쪽 없애기: 마지막 쪽이 40% 미만이면 그 장을 한 단계씩 촘촘하게(최대 3단계)
import subprocess, json, os, re, glob, tempfile
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(D, '..', '클로드코드_실무연수.pdf')
ORDER = ['tools','menus','setup','pro'] + [f'ep{i}' for i in range(17)] + ['wrap','colophon']
def fills():
    t = tempfile.mkdtemp(); subprocess.run(['pdftoppm','-r','30','-gray',P,t+'/p'],check=True)
    out = {}
    for f in glob.glob(t+'/p-*.pgm'):
        n = int(re.search(r'p-0*(\d+)', f).group(1)); im = Image.open(f); w,h = im.size; px = im.load()
        top, bot = int(h*.06), int(h*.93); last = top
        for y in range(top, bot):
            if any(px[x,y] < 200 for x in range(int(w*.08), int(w*.92), 2)): last = y
        out[n] = (last-top)/(bot-top)
    return out
tight = {}
for it in range(4):
    json.dump(tight, open(os.path.join(D,'tight.json'),'w'))
    subprocess.run(['python3', os.path.join(D,'paginate.py')], check=True, capture_output=True)
    pg = json.load(open(os.path.join(D,'pages.json'))); fl = fills(); total = max(fl)
    starts = sorted((int(pg[k]), k) for k in ORDER if k in pg)
    changed = False; tails = []
    for i, (s, k) in enumerate(starts):
        end = (starts[i+1][0] - 1) if i+1 < len(starts) else total
        if k in ('wrap',): continue  # wrap 다음은 colophon(같은 섹션 아님)
        if end > s and fl.get(end, 1) < 0.40:
            tails.append((k, end, round(fl[end],2)))
            if tight.get(k, 0) < 3 and k != 'colophon': tight[k] = tight.get(k, 0) + 1; changed = True
    print('iter', it, 'pages', total, 'tails', tails)
    if not changed: break
json.dump(tight, open(os.path.join(D,'tight.json'),'w')); print('tight', tight)
