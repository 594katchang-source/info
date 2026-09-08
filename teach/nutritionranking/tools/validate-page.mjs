import fs from 'node:fs';
import path from 'node:path';

const [htmlPath] = process.argv.slice(2);
if (!htmlPath) {
  console.error('Usage: node validate-page.mjs <index.html>');
  process.exit(2);
}

const html = fs.readFileSync(htmlPath, 'utf8');
const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]);
const duplicateIds = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
const jsonLdBlocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)]
  .map((match) => JSON.parse(match[1]));
const expectedText = [
  'nutrition_data.js?v=20260908-data',
  'app.js?v=20260908-data',
  'style.css?v=20260908-data',
  '2026 年 8 月 27 日 14:08',
  '2026 年 9 月 8 日',
  'https://data.gov.tw/dataset/8543',
];
const missingExpectedText = expectedText.filter((text) => !html.includes(text));

const result = {
  html: path.resolve(htmlPath),
  duplicateIds,
  jsonLdBlocks: jsonLdBlocks.length,
  dateModified: jsonLdBlocks[0]?.dateModified ?? null,
  missingExpectedText,
};

console.log(JSON.stringify(result, null, 2));

if (duplicateIds.length || missingExpectedText.length || result.dateModified !== '2026-09-08') {
  process.exit(1);
}
