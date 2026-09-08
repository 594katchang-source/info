import fs from 'node:fs';
import path from 'node:path';

const [sourcePath, generatedPath] = process.argv.slice(2);

if (!sourcePath || !generatedPath) {
  console.error('Usage: node validate-tfda-data.mjs <20_5.json> <nutrition_data.js>');
  process.exit(2);
}

const nutrientMap = new Map([
  ['熱量', 'calories'], ['水分', 'water'], ['粗蛋白', 'protein'], ['粗脂肪', 'fat'],
  ['總碳水化合物', 'carbs'], ['膳食纖維', 'fiber'], ['糖質總量', 'sugar'],
  ['鈉', 'sodium'], ['鉀', 'potassium'], ['鈣', 'calcium'], ['鎂', 'magnesium'],
  ['鐵', 'iron'], ['鋅', 'zinc'], ['磷', 'phosphorus'],
  ['維生素A總量(IU)', 'vitA'], ['維生素B1', 'vitB1'], ['維生素B2', 'vitB2'],
  ['維生素B6', 'vitB6'], ['維生素B12', 'vitB12'], ['維生素C', 'vitC'],
  ['維生素D總量(ug)', 'vitD'], ['維生素E總量', 'vitE'], ['葉酸', 'folate'],
  ['膽固醇', 'cholesterol'],
]);

function parseValue(value) {
  if (value === null || value === undefined) return null;
  const text = String(value).trim();
  if (!text || text === '-' || text === 'N.A.' || text === 'NA' || text === 'Tr' || text.includes('微量')) return null;
  const exact = Number(text);
  if (Number.isFinite(exact)) return exact;
  const firstNumber = text.match(/[+-]?(?:\d+(?:\.\d*)?|\.\d+)/)?.[0];
  if (!firstNumber) return null;
  const parsed = Number(firstNumber);
  return Number.isFinite(parsed) ? parsed : null;
}

const sourceText = fs.readFileSync(sourcePath, 'utf8').replace(/^\uFEFF/, '');
const generatedText = fs.readFileSync(generatedPath, 'utf8').replace(/^\uFEFF/, '');

if (sourceText.includes('\uFFFD') || generatedText.includes('\uFFFD')) {
  throw new Error('Replacement character U+FFFD was found in source or generated data.');
}

const rows = JSON.parse(sourceText);
const arrayStart = generatedText.indexOf('[');
const arrayEnd = generatedText.lastIndexOf(']');
if (arrayStart < 0 || arrayEnd < arrayStart) throw new Error('Generated JavaScript array was not found.');
const generated = JSON.parse(generatedText.slice(arrayStart, arrayEnd + 1));

const expected = new Map();
for (const row of rows) {
  const id = String(row['整合編號'] ?? '').trim();
  if (!id) continue;

  let food = expected.get(id);
  if (!food) {
    food = {
      id,
      name: String(row['樣品名稱'] ?? '').trim(),
      commonName: String(row['俗名'] ?? '').trim(),
      englishName: String(row['樣品英文名稱'] ?? '').trim(),
      category: String(row['食品分類'] ?? '').trim(),
      nutrients: {},
    };
    expected.set(id, food);
  }

  const nutrientName = String(row['分析項'] ?? '').trim();
  const value = parseValue(row['每100克含量']);
  if (!nutrientName || value === null || value === 0) continue;
  food.nutrients[nutrientMap.get(nutrientName) ?? nutrientName] = Math.round(value * 100) / 100;
}

const expectedArray = [...expected.values()];
if (generated.length !== expectedArray.length) {
  throw new Error(`Food count mismatch: generated=${generated.length}, expected=${expectedArray.length}`);
}

const generatedIds = new Set(generated.map((food) => food.id));
if (generatedIds.size !== generated.length) throw new Error('Duplicate food IDs were found in generated data.');

let mismatchCount = 0;
const mismatchExamples = [];
for (let index = 0; index < expectedArray.length; index += 1) {
  const expectedFood = expectedArray[index];
  const generatedFood = generated[index];
  if (JSON.stringify(expectedFood) !== JSON.stringify(generatedFood)) {
    mismatchCount += 1;
    if (mismatchExamples.length < 5) {
      mismatchExamples.push({ index, expected: expectedFood.id, generated: generatedFood?.id ?? null });
    }
  }
}

if (mismatchCount > 0) {
  throw new Error(`Generated data mismatches official source in ${mismatchCount} food records: ${JSON.stringify(mismatchExamples)}`);
}

const sampleIndexes = [0, Math.floor(generated.length / 2), generated.length - 1];
const samples = sampleIndexes.map((index) => {
  const food = generated[index];
  return {
    position: index === 0 ? 'first' : index === generated.length - 1 ? 'last' : 'middle',
    index,
    id: food.id,
    name: food.name,
    category: food.category,
    nutrientCount: Object.keys(food.nutrients).length,
    matchedOfficialSource: true,
  };
});

console.log(JSON.stringify({
  source: path.resolve(sourcePath),
  generated: path.resolve(generatedPath),
  sourceRows: rows.length,
  foodCount: generated.length,
  uniqueFoodIds: generatedIds.size,
  fullRecordMismatches: mismatchCount,
  containsReplacementCharacter: false,
  zincKeyMapped: generated.some((food) => Object.hasOwn(food.nutrients, 'zinc')),
  obsoleteChineseZincKeyPresent: generated.some((food) => Object.hasOwn(food.nutrients, '鋅')),
  samples,
}, null, 2));
