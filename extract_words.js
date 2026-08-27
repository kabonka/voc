const fs = require('fs');
const html = fs.readFileSync('voc.html', 'utf8');
const start = html.indexOf('const wordList = ');
if (start < 0) { console.error('wordList not found'); process.exit(1); }
const arrStart = html.indexOf('[', start);
let depth = 0, i = arrStart, end = -1;
for (; i < html.length; i++) {
  const c = html[i];
  if (c === '[') depth++;
  else if (c === ']') { depth--; if (depth === 0) { end = i; break; } }
}
const arrText = html.slice(arrStart, end + 1);
const wordList = JSON.parse(arrText);
const out = wordList.map(w => ({ word: w.word, def: w.def, sent: w.sent }));
fs.writeFileSync('words.json', JSON.stringify(out));
console.log('extracted count =', wordList.length);
