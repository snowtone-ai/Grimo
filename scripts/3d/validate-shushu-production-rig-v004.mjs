// Validate only the separately named v004 delivery, after image-byte restoration.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import validator from 'gltf-validator';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const directory = path.join(root, 'assets/grimo/production/shushu/tripo/geometry-v003/rigging');
const results = [];
for (const suffix of ['', '-proof']) {
  const name = `shushu-v006-production-rig-v004${suffix}.glb`;
  const result = await validator.validateBytes(new Uint8Array(fs.readFileSync(path.join(directory, name))), { uri: name, maxIssues: 10000 });
  results.push({ name, ...result });
}
fs.writeFileSync(path.join(root, 'docs/production/shushu/evidence/production-rig-v004/schema-validation.json'), JSON.stringify(results, null, 2) + '\n');
for (const result of results) console.log(result.name, JSON.stringify({ errors: result.issues.numErrors, warnings: result.issues.numWarnings }));
if (results.some(result => result.issues.numErrors > 0)) process.exitCode = 1;
