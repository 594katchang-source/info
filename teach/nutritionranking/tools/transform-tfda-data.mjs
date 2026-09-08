import fs from 'node:fs';
import path from 'node:path';

const [inputPath, outputPath, metadataUpdatedAt = ''] = process.argv.slice(2);

if (!inputPath || !outputPath) {
  console.error('Usage: node transform-tfda-data.mjs <20_5.json> <nutrition_data.js> [metadataUpdatedAt]');
  process.exit(2);
}

const nutrientMap = new Map([
  ['熱量', 'calories'],
  ['水分', 'water'],
  ['粗蛋白', 'protein'],
  ['粗脂肪', 'fat'],
  ['總碳水化合物', 'carbs'],
  ['膳食纖維', 'fiber'],
  ['糖質總量', 'sugar'],
  ['鈉', 'sodium'],
  ['鉀', 'potassium'],
  ['鈣', 'calcium'],
  ['鎂', 'magnesium'],
  ['鐵', 'iron'],
  ['鋅', 'zinc'],
  ['磷', 'phosphorus'],
  ['維生素A總量(IU)', 'vitA'],
  ['維生素B1', 'vitB1'],
  ['維生素B2', 'vitB2'],
  ['維生素B6', 'vitB6'],
  ['維生素B12', 'vitB12'],
  ['維生素C', 'vitC'],
  ['維生素D總量(ug)', 'vitD'],
  ['維生素E總量', 'vitE'],
  ['葉酸', 'folate'],
  ['膽固醇', 'cholesterol'],
]);

function parseLegacyCompatibleNumber(value) {
  if (value === null || value === undefined) return null;

  const text = String(value).trim();
  if (!text || text === '-' || text === 'N.A.' || text === 'NA' || text === 'Tr' || text.includes('微量')) {
    return null;
  }

  const exact = Number(text);
  if (Number.isFinite(exact)) return exact;

  // The former PowerShell transformer kept the first numeric component of a
  // compound value such as P/M/S. Retain that behavior so existing rankings do
  // not silently change semantics during a source-data refresh.
  const firstNumber = text.match(/[+-]?(?:\d+(?:\.\d*)?|\.\d+)/)?.[0];
  if (!firstNumber) return null;

  const parsed = Number(firstNumber);
  return Number.isFinite(parsed) ? parsed : null;
}

const sourceText = fs.readFileSync(inputPath, 'utf8').replace(/^\uFEFF/, '');
const rows = JSON.parse(sourceText);

if (!Array.isArray(rows) || rows.length === 0) {
  throw new Error('TFDA source JSON is empty or is not an array.');
}

const foods = new Map();
let skippedMissingId = 0;
let skippedMissingNutrient = 0;
let skippedNonNumericOrZero = 0;
let compoundValueCount = 0;

for (const row of rows) {
  const id = String(row['整合編號'] ?? '').trim();
  if (!id) {
    skippedMissingId += 1;
    continue;
  }

  let food = foods.get(id);
  if (!food) {
    food = {
      id,
      name: String(row['樣品名稱'] ?? '').trim(),
      commonName: String(row['俗名'] ?? '').trim(),
      englishName: String(row['樣品英文名稱'] ?? '').trim(),
      category: String(row['食品分類'] ?? '').trim(),
      nutrients: {},
    };
    foods.set(id, food);
  } else {
    if (!food.name && row['樣品名稱']) food.name = String(row['樣品名稱']).trim();
    if (!food.commonName && row['俗名']) food.commonName = String(row['俗名']).trim();
    if (!food.englishName && row['樣品英文名稱']) food.englishName = String(row['樣品英文名稱']).trim();
    if (!food.category && row['食品分類']) food.category = String(row['食品分類']).trim();
  }

  const sourceNutrientName = String(row['分析項'] ?? '').trim();
  if (!sourceNutrientName) {
    skippedMissingNutrient += 1;
    continue;
  }

  const rawValue = row['每100克含量'];
  const rawText = rawValue === null || rawValue === undefined ? '' : String(rawValue).trim();
  if (rawText.includes('/')) compoundValueCount += 1;

  const numericValue = parseLegacyCompatibleNumber(rawValue);
  if (numericValue === null || numericValue === 0) {
    skippedNonNumericOrZero += 1;
    continue;
  }

  const key = nutrientMap.get(sourceNutrientName) ?? sourceNutrientName;
  food.nutrients[key] = Math.round(numericValue * 100) / 100;
}

const database = [...foods.values()];
const nutrientKeys = new Set(database.flatMap((food) => Object.keys(food.nutrients)));
const categories = [...new Set(database.map((food) => food.category))].sort((a, b) => a.localeCompare(b, 'zh-Hant'));

if (database.length < 2000) {
  throw new Error(`Unexpected food count: ${database.length}. Expected at least 2000.`);
}

for (const food of database) {
  if (!food.id || !food.name || !food.category || typeof food.nutrients !== 'object') {
    throw new Error(`Invalid transformed food record: ${food.id || '(missing id)'}`);
  }
}

const header = [
  '// Generated from the Taiwan FDA Food Nutrition Composition Dataset (Dataset ID: 8543).',
  '// Source: https://data.gov.tw/dataset/8543',
  metadataUpdatedAt ? `// Dataset metadata updated: ${metadataUpdatedAt}` : null,
  '// Values are per 100 g edible portion unless the source nutrient definition says otherwise.',
].filter(Boolean).join('\n');

const serialized = database.map((food) => `  ${JSON.stringify(food)}`).join(',\n');
const output = `${header}\nconst NUTRITION_DATABASE = [\n${serialized}\n];\n`;

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, output, 'utf8');

console.log(JSON.stringify({
  inputPath: path.resolve(inputPath),
  outputPath: path.resolve(outputPath),
  sourceRows: rows.length,
  foods: database.length,
  nutrientKeys: nutrientKeys.size,
  categories,
  skippedMissingId,
  skippedMissingNutrient,
  skippedNonNumericOrZero,
  compoundValueCount,
  first: { id: database[0].id, name: database[0].name },
  middle: { id: database[Math.floor(database.length / 2)].id, name: database[Math.floor(database.length / 2)].name },
  last: { id: database.at(-1).id, name: database.at(-1).name },
}, null, 2));
