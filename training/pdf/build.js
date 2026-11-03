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
    return `<section class="ep" id="${id}">${body}</section>`;
  });
}

const html = shell.replace('<!--PARTS-->', parts.map((f) => inject(fs.readFileSync(path.join(dir, f), 'utf8'))).join('\n'));
const built = path.join(dir, 'book.html');
fs.writeFileSync(built, html);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + built, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const out = path.join(dir, '..', '클로드코드_실무연수.pdf');
  await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log(out);
})();
