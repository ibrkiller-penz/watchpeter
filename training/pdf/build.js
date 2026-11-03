// 사용: python3 training/pdf/figs.py && node training/pdf/build.js  → training/클로드코드_실무연수.pdf
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const dir = __dirname;
const shell = fs.readFileSync(path.join(dir, 'shell.html'), 'utf8');
const figs = JSON.parse(fs.readFileSync(path.join(dir, 'figs.json'), 'utf8'));
const parts = ['part-0.html', 'part-m.html', 'part-s.html', 'part-p.html', 'part-a.html', 'part-b.html', 'part-d.html', 'part-e.html', 'part-f.html', 'part-c.html'];

// 그림 끼워 넣기: section id 별로 after_intro / before:h3:<글자> / end
function inject(html) {
  return html.replace(/<section class="ep" id="([^"]+)">([\s\S]*?)<\/section>/g, (all, id, body) => {
    for (const [where, code] of figs[id] || []) {
      if (where === 'after_intro') {
        const m = body.match(/<p class="intro">[\s\S]*?<\/p>/);
        if (m) body = body.replace(m[0], m[0] + '\n' + code);
        else { const h = body.indexOf('</h2>'); body = body.slice(0, h + 5) + code + body.slice(h + 5); }
      } else if (where.startsWith('before:h3:')) {
        const key = where.slice(10);
        const re = new RegExp('<h[34]>[^<]*' + key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
        const m = body.match(re);
        if (m) body = body.replace(m[0], code + '\n' + m[0]);
        else { console.warn('anchor not found', id, where); body += code; }
      } else if (where.startsWith('after:h3:')) {
        const key = where.slice(9);
        const re = new RegExp('<h[34]>[^<]*' + key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '[^<]*</h[34]>');
        const m = body.match(re);
        if (m) body = body.replace(m[0], m[0] + '\n' + code);
        else { console.warn('anchor not found', id, where); body += code; }
      } else if (where === 'end') {
        const t = body.lastIndexOf('<p class="takeaway">');
        body = t >= 0 ? body.slice(0, t) + code + '\n' + body.slice(t) : body + code;
      }
    }
    const lv = tight[id] ? ' tight' + Math.min(tight[id], 3) + (tight[id] >= 2 ? ' tight1' : '') + (tight[id] >= 3 ? ' tight2' : '') : '';
    return `<section class="ep${lv}" id="${id}">${body}</section>`;
  });
}

let tight = {}; try { tight = JSON.parse(fs.readFileSync(path.join(dir, 'tight.json'), 'utf8')); } catch (e) {}
let pages = {}; try { pages = JSON.parse(fs.readFileSync(path.join(dir, 'pages.json'), 'utf8')); } catch (e) {}
const html = shell.replace(/\{\{pg:([a-z0-9]+)\}\}/g, (m, k) => pages[k] || '00').replace('<!--PARTS-->', parts.map((f) => inject(fs.readFileSync(path.join(dir, f), 'utf8'))).join('\n'));
const built = path.join(dir, 'book.html');
fs.writeFileSync(built, html);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + built, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  // 제목 + 이어지는 짧은 문단 + 첫 덩어리(표·그림·상자)를 한 묶음으로: 쪽 끝에 제목만 남지 않게
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => {
    const PAGE = 990; // A4 본문 높이(px, 대략)
    document.querySelectorAll('section.ep h3, section.ep > h4').forEach((h) => {
      if (h.closest('li') || h.parentElement.classList.contains('keep')) return;
      const group = [h]; let n = h.nextElementSibling; let ps = 0;
      while (n && n.tagName === 'P' && !n.classList.contains('takeaway') && ps < 2) { group.push(n); ps++; n = n.nextElementSibling; }
      if (n && !/^H[234]$/.test(n.tagName) && !n.classList.contains('takeaway')) {
        const hgt = group.reduce((a, e) => a + e.offsetHeight, 0) + n.offsetHeight;
        if (hgt < PAGE * 0.55) group.push(n);
      }
      const w = document.createElement('div'); w.className = 'keep';
      if (group.length && group[group.length - 1] !== n) w.style.breakAfter = 'avoid';
      h.parentElement.insertBefore(w, h); group.forEach((e) => w.appendChild(e));
    });
    document.querySelectorAll('section.ep table.tbl').forEach((t) => { if (t.offsetHeight < PAGE * 0.6) t.style.breakInside = 'avoid'; });
  });
  const out = path.join(dir, '..', '클로드코드_실무연수.pdf');
  await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log(out);
})();
