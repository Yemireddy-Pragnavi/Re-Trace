import { PNG } from 'npm:pngjs@7.0.0';
import jpeg from 'npm:jpeg-js@0.4.4';
import { PDFDocument, StandardFonts } from 'npm:pdf-lib@1.17.1';
import { unzipSync, zipSync, strToU8 } from 'npm:fflate@0.8.2';
import { Buffer } from 'node:buffer';
export const MAX=8*1024*1024;
export const signatures:Record<string,number[]>={png:[137,80,78,71,13,10,26,10],jpeg:[255,216,255],pdf:[37,80,68,70,45],zip:[80,75,3,4]};
export const canonical=(v:any):string=>v===null||typeof v!=='object'?JSON.stringify(v):Array.isArray(v)?'['+v.map(canonical).join(',')+']':'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
export async function sha(data:Uint8Array|string){const bytes=typeof data==='string'?new TextEncoder().encode(data):data;return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(n=>n.toString(16).padStart(2,'0')).join('')}
export function find(data:Uint8Array, pattern:number[],start=0){outer:for(let i=start;i<=data.length-pattern.length;i++){for(let j=0;j<pattern.length;j++)if(data[i+j]!==pattern[j])continue outer;return i}return -1}
const u32=(b:Uint8Array,i:number,le=false)=>new DataView(b.buffer,b.byteOffset,b.byteLength).getUint32(i,le);
const u16=(b:Uint8Array,i:number)=>new DataView(b.buffer,b.byteOffset,b.byteLength).getUint16(i,true);
function crc(b:Uint8Array){let n=0xffffffff;for(const v of b){n^=v;for(let k=0;k<8;k++)n=(n>>>1)^((n&1)?0xedb88320:0)}return (n^0xffffffff)>>>0}
function endAt(data:Uint8Array,start:number,type:string):[number,string]{
 if(type==='png'){let p=start+8,count=0;while(p+12<=data.length&&count++<10000){const len=u32(data,p),end=p+12+len;if(end>data.length||len>MAX)throw Error('Truncated PNG');const kind=String.fromCharCode(...data.slice(p+4,p+8));if(crc(data.slice(p+4,end-4))!==u32(data,end-4))throw Error('PNG CRC mismatch');if(count===1&&kind!=='IHDR')throw Error('Missing PNG IHDR');if(kind==='IEND')return[end,'PNG chunk lengths and CRCs verified'];p=end}}
 if(type==='jpeg'){const e=find(data,[255,217],start+3);if(e>=0)return[e+2,'JPEG SOI/EOI boundary']}
 if(type==='pdf'){const e=find(data,[37,37,69,79,70],start+5);if(e>=0)return[e+5,'PDF first EOF/revision boundary']}
 if(type==='zip'){const e=find(data,[80,75,5,6],start+4);if(e>=0&&e+22<=data.length){const end=e+22+u16(data,e+20);if(end<=data.length)return[end,'ZIP end-of-central-directory boundary']}}
 throw Error('No complete supported boundary')
}
async function validate(blob:Uint8Array,type:string){
 if(type==='png'){if(blob.length<33||u32(blob,16)*u32(blob,20)>4_000_000)throw Error('Image pixel budget exceeded');PNG.sync.read(Buffer.from(blob));return 'PNG pixel decode succeeded'}
 if(type==='jpeg'){jpeg.decode(blob,{useTArray:true,maxResolutionInMP:4,maxMemoryUsageInMB:64});return 'JPEG pixel decode succeeded'}
 if(type==='pdf'){const pdf=await PDFDocument.load(blob,{ignoreEncryption:false,throwOnInvalidObject:true});if(pdf.getPageCount()>200)throw Error('PDF page budget exceeded');return 'PDF object and page structure parsed'}
 const e=find(blob,[80,75,5,6]);if(e<0)throw Error('ZIP directory absent');const count=u16(blob,e+10);if(count>200)throw Error('ZIP member limit exceeded');let p=u32(blob,e+16,true),total=0;const checks:{name:string,crc:number}[]=[];
 for(let i=0;i<count;i++){if(p+46>blob.length||u32(blob,p,true)!==0x02014b50)throw Error('Invalid ZIP central directory');if(u16(blob,p+8)&1)throw Error('Encrypted ZIP unsupported');total+=u32(blob,p+24,true);if(total>MAX)throw Error('ZIP expansion budget exceeded');const len=u16(blob,p+28);checks.push({name:new TextDecoder().decode(blob.slice(p+46,p+46+len)),crc:u32(blob,p+16,true)});p+=46+len+u16(blob,p+30)+u16(blob,p+32)}
 const files=unzipSync(blob);for(const item of checks)if(!files[item.name]||crc(files[item.name])!==item.crc)throw Error('ZIP member CRC mismatch');return 'ZIP directory and member CRCs validated; never extracted to paths';
}
export async function carve(data:Uint8Array,types=Object.keys(signatures)){
 if(data.length>MAX)throw Error('Cloud source limit is 8 MiB');if(types.some(t=>!signatures[t]))throw Error('Unsupported type');let n=0;const files:any[]=[],rejected:any[]=[];
 for(const type of types){let cursor=0;while(true){const start=find(data,signatures[type],cursor);if(start<0)break;cursor=start+signatures[type].length;if(++n>128)return {files,rejected,complete:false,reason:'Candidate limit exceeded'};
 try{const[end,boundary]=endAt(data,start,type);const blob=data.slice(start,end);const parsed=await validate(blob,type);files.push({type,classification:type==='pdf'?'Document':type==='zip'?'Archive':'Image',offset:start,end_offset:end,size:blob.length,sha256:await sha(blob),confidence:95,reasons:['Known signature (+25)',boundary+' (+30)',parsed+' (+40)'],confidence_note:'Heuristic, not statistical probability',data:blob})}catch(e){rejected.push({type,offset:start,reason:String(e).slice(0,200)})}}}
 return {files:files.sort((a,b)=>a.offset-b.offset),rejected,complete:true}
}
export async function fixture(){
 const payloads:Uint8Array[]=[];
 for(let i=0;i<5;i++){const png=new PNG({width:16+i,height:16+i});for(let j=0;j<png.data.length;j+=4){png.data[j]=35+i*20;png.data[j+1]=170-i*12;png.data[j+2]=190;png.data[j+3]=255}payloads.push(i<2?new Uint8Array(PNG.sync.write(png)):new Uint8Array(jpeg.encode({data:png.data,width:16+i,height:16+i},70).data))}
 for(let i=0;i<2;i++){const pdf=await PDFDocument.create();pdf.setCreationDate(new Date('2026-01-01T00:00:00Z'));pdf.setModificationDate(new Date('2026-01-01T00:00:00Z'));pdf.addPage([200+i*20,200]);let bytes=await pdf.save({useObjectStreams:false});while(bytes.length&&[10,13,32].includes(bytes[bytes.length-1]))bytes=bytes.slice(0,-1);payloads.push(bytes)}
 payloads.push(zipSync({'evidence.txt':strToU8('Re-Trace known ground truth')},{mtime:new Date('2026-01-01T00:00:00Z')}));
 const size=payloads.reduce((n,b)=>n+b.length+1024,1024),data=new Uint8Array(size);let p=1024;for(const b of payloads){data.set(b,p);p+=b.length+1024}return{data,payloads}
}
export async function groundTruth(data:Uint8Array,recovered:any[]){const known=await fixture();if(await sha(data)!==await sha(known.data))return null;const expected=new Set(await Promise.all(known.payloads.map(sha))),actual=new Set(recovered.map(f=>f.sha256));const matched=[...expected].filter(x=>actual.has(x)).length;return{known_artifacts:8,recovered_artifacts:recovered.length,matched_artifacts:matched,missed_count:8-matched,false_positives:[...actual].filter(x=>!expected.has(x)).length,recovery_percentage:matched/8*100}}
export async function pdfReport(payload:any){const doc=await PDFDocument.create();const font=await doc.embedFont(StandardFonts.Courier);let page=doc.addPage(),y=790;for(const line of ['RE-TRACE | FORENSIC CASE REPORT','Sandbox assurance only. Original sources retained.',...JSON.stringify(payload,null,2).split('\n')]){const safe=line.replace(/[^\x20-\x7e]/g,'?');for(let i=0;i<Math.max(1,safe.length);i+=88){if(y<45){page=doc.addPage();y=790}page.drawText(safe.slice(i,i+88),{x:35,y,size:9,font});y-=12}}return new Uint8Array(await doc.save())}
