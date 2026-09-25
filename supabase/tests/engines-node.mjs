// Test the deployed TypeScript source using local npm modules when Deno registry access is unavailable.
import fs from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import ts from 'typescript';
const source=new URL('../functions/retrace-api/engines.ts',import.meta.url);
const compiled=new URL('../functions/retrace-api/.engines-test.mjs',import.meta.url);
const content=(await fs.readFile(source,'utf8')).replace(/npm:([^'@]+(?:\/[^'@]+)?)@[0-9.]+/g,'$1');
try{
await fs.writeFile(compiled,ts.transpileModule(content,{compilerOptions:{module:ts.ModuleKind.ESNext,target:ts.ScriptTarget.ES2022}}).outputText);
const {fixture,carve,sha,pdfReport,groundTruth}=await import(compiled.href);
const {data,payloads}=await fixture();if(await sha(data)!==await sha((await fixture()).data))throw Error('Fixture is not deterministic');const before=await sha(data);const recovered=await carve(data);
const actual=recovered.files.map(f=>f.sha256).sort();const expected=(await Promise.all(payloads.map(sha))).sort();
if(JSON.stringify(actual)!==JSON.stringify(expected))throw Error('Ground-truth recovery failed: '+JSON.stringify({actual,expected,rejected:recovered.rejected}));
if(recovered.files.length!==8||!recovered.complete||await sha(data)!==before)throw Error('Source preservation/recovery failure');
const bad=data.slice();bad[1024+20]^=1;const scan=await carve(bad,['png']);if(scan.files.length!==1||!scan.rejected.some(r=>r.offset===1024))throw Error('Corrupted PNG not rejected');
const flood=await carve(new TextEncoder().encode('%PDF-truncated'.repeat(150)),['pdf']);if(flood.complete)throw Error('Budget not enforced');
const zeros=await carve(new Uint8Array(data.length));if(zeros.files.length)throw Error('Artifact reported in zeroed data');
const metrics=await groundTruth(data,recovered.files);if(metrics.recovery_percentage!==100||metrics.false_positives||metrics.missed_count)throw Error('Invalid truth metrics');
const report=await pdfReport({case:'Synthetic validation',scope:'Not certified'});if(new TextDecoder().decode(report.slice(0,5))!=='%PDF-')throw Error('PDF output invalid');
console.log('PASS: deterministic 8-artifact ground truth and measured recovery statistics, source unchanged, PNG corruption rejection, candidate cap, zero-buffer scan, PDF report');
}finally{await fs.rm(compiled,{force:true})}
