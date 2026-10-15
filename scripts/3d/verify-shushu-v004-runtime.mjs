// Immutable source/candidate invariants and bounded evidence gates.
import fs from 'node:fs';
import crypto from 'node:crypto';
const out='docs/production/shushu/evidence/production-rig-v004-runtime/';
const read=n=>JSON.parse(fs.readFileSync(out+n));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const costs=read('asset-costs.json');
function glb(p){const b=fs.readFileSync(p),n=b.readUInt32LE(12);return {b,j:JSON.parse(b.subarray(20,20+n)),bin:b.subarray(28+n)};}
const a=glb(costs.source),b=glb(costs.candidate),allowed=new Set();
for(const m of a.j.meshes)for(const p of m.primitives){if(p.attributes.WEIGHTS_1===undefined)continue;const ac=a.j.accessors[p.attributes.WEIGHTS_0],v=a.j.bufferViews[ac.bufferView],start=(v.byteOffset||0)+(ac.byteOffset||0);for(let i=start;i<start+ac.count*16;i++)allowed.add(i);}
let changedBytes=0,unexpectedBytes=0;for(let i=0;i<a.bin.length;i++)if(a.bin[i]!==b.bin[i]){changedBytes++;if(!allowed.has(i))unexpectedBytes++;}
const expected=structuredClone(a.j);for(const m of expected.meshes)for(const p of m.primitives){delete p.attributes.JOINTS_1;delete p.attributes.WEIGHTS_1;}
const structureEqual=JSON.stringify(expected)===JSON.stringify(b.j);
const protection=[];for(const r of read('protected-inputs.json')){const exists=fs.existsSync(r.path),now=exists?sha(fs.readFileSync(r.path)):null;if(now!==r.sha256)protection.push({path:r.path,exists,before:r.sha256,now,authorized:['docs/production/Handoff.md','docs/production/shushu/evidence/production-rig-v004/REVIEW.md'].includes(r.path)});}
const inter=read('interpolation-comparison.json'),stock=read('stock-runtime.json'),four=read('four-runtime.json');
const report={sourceSha256:sha(a.b),sourceMatchesManifest:sha(a.b)===costs.sourceSha256,candidateSha256:sha(b.b),structureEqual,changedBytes,unexpectedBytes,binLengthEqual:a.bin.length===b.bin.length,protectedInputs:read('protected-inputs.json').length,protectionChanges:protection,schemaErrors:read('candidate-validation.json').issues.numErrors,engineReference:{samples:inter.engine.length,maxMatrix:Math.max(...inter.engine.map(c=>c.maxMatrix)),maxAnchor:Math.max(...inter.engine.map(c=>c.maxAnchor)),maxMorph:Math.max(...inter.engine.map(c=>c.maxMorph)),missing:[...new Set(inter.engine.flatMap(c=>c.missing))]},stockVsSpecMaxMatrix:Math.max(...stock.checks.map(c=>c.maxMatrix)),skinRasterPeak:Math.max(...stock.checks.flatMap(c=>c.skin.map(s=>s.maxFour))),normalAnglePeak:Math.max(...stock.checks.flatMap(c=>c.skin.map(s=>s.maxNormalAngleDeg))),browserErrors:[...stock.errors,...four.errors],motionAdvance:[...stock.advance,...four.advance],candidateDecision:'REJECTED: no restored extra influences, no material size/performance improvement; not adopted',mobile:'UNKNOWN: adb devices -l returned no connected devices on 2026-10-15'};
report.invariantsPass=report.sourceMatchesManifest&&structureEqual&&unexpectedBytes===0&&report.binLengthEqual&&protection.every(r=>r.authorized)&&report.schemaErrors===0&&report.browserErrors.length===0;
report.boundedBindingPass=report.engineReference.missing.length===0&&report.engineReference.maxMatrix<2e-6&&report.engineReference.maxAnchor<2e-6&&report.engineReference.maxMorph<1e-5&&report.motionAdvance.every(r=>r.afterTime>r.beforeTime&&r.matrixDelta>1e-5);
report.productionGate='HOLD: full skin/morph/normal render equivalence, phone performance, real items and production motion contracts';
fs.writeFileSync(out+'verification.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));if(!report.invariantsPass||!report.boundedBindingPass)process.exitCode=1;
