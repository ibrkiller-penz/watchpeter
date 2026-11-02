// 사용: node training/pdf/build.js  → training/클로드코드_실무연수.pdf
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const dir = __dirname;
const shell = fs.readFileSync(path.join(dir, 'shell.html'), 'utf8');
const parts = ['part-a.html', 'part-b.html', 'part-c.html']
  .map((f) => fs.readFileSync(path.join(dir, f), 'utf8'))
  .join('\n');
const html = shell.replace('<!--PARTS-->', parts);
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
