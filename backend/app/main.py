import json
import os
import shutil
import threading
import time
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / '.env')
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from pydantic import BaseModel, Field
from . import store, auth, engines, reports

store.initialize()
reports.signing_key()
app = FastAPI(title='Re-Trace SIH26149 API',version='0.1.0')
app.add_middleware(CORSMiddleware,allow_origins=os.getenv('ALLOWED_ORIGINS','http://localhost:5173,http://127.0.0.1:5173').split(','),allow_methods=['GET','POST'],allow_headers=['Authorization','Content-Type'])
worker_lock = threading.Lock()

@app.middleware('http')
async def headers(request, call_next):
    length = request.headers.get('content-length')
    if length:
        try:
            if int(length) > engines.MAX_BYTES + 1024 * 1024:
                return Response('Request too large',status_code=413)
        except ValueError:
            return Response('Invalid content length',status_code=400)
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response

def case_access(case_id, actor, write=False):
    with store.connection() as db:
        row = db.execute('SELECT * FROM cases WHERE id=?',(case_id,)).fetchone()
        member = db.execute('SELECT 1 FROM members WHERE case_id=? AND user_id=?',(case_id,actor['id'])).fetchone()
    if not row or not (actor['role']=='ADMIN' or row['owner']==actor['id'] or member):
        raise HTTPException(404,'Case not found')
    if write and actor['role'] not in ('ADMIN','INVESTIGATOR'):
        raise HTTPException(403,'Read-only role')
    return dict(row)

def admin(actor):
    if actor['role'] != 'ADMIN':
        raise HTTPException(403,'Administrator required')

def source_path(source_id):
    # IDs come only from already-authorized database records.
    return store.ROOT / 'sources' / source_id

def source_record(source_id, case_id):
    with store.connection() as db:
        row = db.execute('SELECT * FROM sources WHERE id=? AND case_id=?',(source_id,case_id)).fetchone()
    if not row:
        raise HTTPException(404,'Source not found in this case')
    return dict(row)

def save_source(case_id, actor, data, name, media, kind):
    folder = store.ROOT / 'sources'
    folder.mkdir(exist_ok=True)
    if sum(p.stat().st_size for p in folder.iterdir() if p.is_file()) + len(data) > 256 * 1024 * 1024:
        raise HTTPException(413,'Local evidence quota of 256 MiB reached')
    sid = store.uid()
    source_path(sid).write_bytes(data)
    record = {'id':sid,'case_id':case_id,'name':name[:200], 'media':media,'kind':kind,'size':len(data),'hash':engines.sha(data),'created':store.now()}
    with store.connection() as db:
        db.execute('INSERT INTO sources VALUES(:id,:case_id,:name,:media,:kind,:size,:hash,:created)',record)
    store.record(actor,'SOURCE_INSPECTED',case_id,{**record,'media_detection':'Operator-declared; physical controller not available','filesystem':'Not interpreted: raw byte access'})
    return record

@app.get('/api/health')
def health():
    return {'status':'ok','version':'0.1.0','mode':'sandbox','auth_mode':auth.AUTH_MODE}

@app.post('/api/auth/register')
def register(data:auth.Credentials, request:Request):
    return auth.signup(data,request)

@app.post('/api/auth/login')
def login(data:auth.Credentials,request:Request):
    return auth.login(data,request)

@app.post('/api/auth/supabase')
def cloud_login(data:auth.CloudToken,request:Request):
    return auth.cloud_exchange(data,request)

@app.get('/api/auth/me')
def me(actor=Depends(auth.authenticate)):
    return {k:actor[k] for k in ('id','email','role','session_id')}

@app.post('/api/auth/logout')
def logout(actor=Depends(auth.authenticate)):
    with store.connection() as db:
        db.execute('UPDATE sessions SET revoked=1 WHERE id=?',(actor['session_id'],))
    store.record(actor,'SESSION_ENDED')
    return {'revoked':True}

@app.post('/api/auth/revoke-all')
def revoke_all(actor=Depends(auth.authenticate)):
    with store.connection() as db:
        db.execute('UPDATE sessions SET revoked=1 WHERE user_id=?',(actor['id'],))
    store.record(actor,'ALL_SESSIONS_REVOKED')
    return {'revoked':True}

@app.get('/api/users')
def users(actor=Depends(auth.authenticate)):
    admin(actor)
    with store.connection() as db:
        return [dict(r) for r in db.execute('SELECT id,email,role,created FROM users')]

class RoleUpdate(BaseModel):
    role:Literal['ADMIN','INVESTIGATOR','VIEWER']

@app.post('/api/users/{user_id}/role')
def change_role(user_id:str,data:RoleUpdate,actor=Depends(auth.authenticate)):
    admin(actor)
    if actor['id']==user_id:
        raise HTTPException(400,'Cannot change your own administrative role')
    with store.connection() as db:
        if not db.execute('SELECT 1 FROM users WHERE id=?',(user_id,)).fetchone():
            raise HTTPException(404,'User not found')
        db.execute('UPDATE users SET role=? WHERE id=?',(data.role,user_id))
        db.execute('UPDATE sessions SET revoked=1 WHERE user_id=?',(user_id,))
    store.record(actor,'ROLE_CHANGED',details={'user_id':user_id,'role':data.role})
    return {'updated':True}

class CaseInput(BaseModel):
    title:str=Field(min_length=3,max_length=160)
    description:str=Field(default='',max_length=3000)

@app.get('/api/cases')
def cases(actor=Depends(auth.authenticate)):
    with store.connection() as db:
        return [dict(r) for r in db.execute('SELECT * FROM cases WHERE ?=\'ADMIN\' OR owner=? OR id IN (SELECT case_id FROM members WHERE user_id=?) ORDER BY created DESC',(actor['role'],actor['id'],actor['id']))]

@app.post('/api/cases')
def new_case(data:CaseInput,actor=Depends(auth.authenticate)):
    if actor['role']=='VIEWER':
        raise HTTPException(403,'Read-only role')
    row={'id':store.uid(),'title':data.title,'description':data.description,'owner':actor['id'],'created':store.now()}
    with store.connection() as db:
        db.execute('INSERT INTO cases VALUES(:id,:title,:description,:owner,:created)',row)
    store.record(actor,'CASE_CREATED',row['id'],{'title':data.title})
    return row

class Member(BaseModel):
    user_id:str

@app.post('/api/cases/{case_id}/members')
def add_member(case_id:str,data:Member,actor=Depends(auth.authenticate)):
    admin(actor)
    case_access(case_id,actor,True)
    with store.connection() as db:
        if not db.execute('SELECT 1 FROM users WHERE id=?',(data.user_id,)).fetchone():
            raise HTTPException(404,'User not found')
        db.execute('INSERT OR IGNORE INTO members VALUES(?,?)',(case_id,data.user_id))
    store.record(actor,'CASE_MEMBER_ADDED',case_id,{'user_id':data.user_id})
    return {'added':True}

@app.get('/api/cases/{case_id}')
def case_detail(case_id:str,actor=Depends(auth.authenticate)):
    case=case_access(case_id,actor)
    with store.connection() as db:
        sources=[dict(r) for r in db.execute('SELECT * FROM sources WHERE case_id=?',(case_id,))]
        jobs=[{**dict(r),'result':json.loads(r['result'])} for r in db.execute('SELECT * FROM jobs WHERE case_id=? ORDER BY created DESC',(case_id,))]
        evidence=[{**dict(r),'details':json.loads(r['details'])} for r in db.execute('SELECT * FROM evidence WHERE case_id=?',(case_id,))]
        report_rows=[dict(r) for r in db.execute('SELECT id,created,pdf_hash FROM reports WHERE case_id=? ORDER BY created DESC',(case_id,))]
    return {'case':case,'sources':sources,'jobs':jobs,'evidence':evidence,'reports':report_rows,'events':store.case_timeline(case_id)}

@app.post('/api/cases/{case_id}/open')
def open_case(case_id:str,actor=Depends(auth.authenticate)):
    case_access(case_id,actor)
    store.record(actor,'CASE_OPENED',case_id)
    return {'opened':True}

@app.post('/api/cases/{case_id}/sources')
async def upload_source(case_id:str,file:UploadFile=File(...),media:Literal['HDD','SSD','NVMe','USB','SD','Optical','Image']=Form('Image'),kind:Literal['image','file']=Form('image'),actor=Depends(auth.authenticate)):
    case_access(case_id,actor,True)
    data=await file.read(engines.MAX_BYTES+1)
    await file.close()
    if not data or len(data)>engines.MAX_BYTES:
        raise HTTPException(413,'Upload must contain 1 byte to 32 MiB')
    if kind=='image' and Path(file.filename or '').suffix.lower() not in ('.img','.raw','.dd','.bin'):
        raise HTTPException(400,'Raw images require .img, .raw, .dd or .bin; E01/AFF are not supported')
    return save_source(case_id,actor,data,(file.filename or 'upload').replace('\\','/').split('/')[-1],media,kind)

@app.post('/api/cases/{case_id}/demo-source')
def demo_source(case_id:str,actor=Depends(auth.authenticate)):
    case_access(case_id,actor,True)
    image,_=engines.fixture()
    return save_source(case_id,actor,image,'four-format-forensic-fixture.img','USB','image')

class Operation(BaseModel):
    module:Literal['drive','files','recovery','validation']
    source_ids:list[str]=Field(min_length=1,max_length=50)
    types:list[Literal['png','jpeg','pdf','zip']]=Field(default_factory=lambda:list(engines.SIGNATURES),min_length=1)
    confirmation:str=''
    purpose:Literal['Internal reuse','External transfer','Disposal']='Internal reuse'
    sensitivity:Literal['Normal','Sensitive','Highly sensitive']='Normal'

def policy_for(source,data):
    native = {'SSD':'ATA sanitize / controller-supported crypto erase','NVMe':'NVMe sanitize / crypto erase','HDD':'Media overwrite with verified device capabilities'}.get(source['media'],'Native media-specific capability inspection required')
    return {'media':source['media'],'media_basis':'Operator-declared profile','scope':data.module,'purpose':data.purpose,'sensitivity':data.sensitivity,
            'sandbox_method':'Single zero overwrite and full read-back of a disposable working copy',
            'native_recommendation':native,'native_available':False,
            'decision': 'Escalate to native purge/destroy assessment' if data.purpose!='Internal reuse' or data.sensitivity=='Highly sensitive' else 'Logical clear demonstration on sandbox copy',
            'standards':['NIST SP 800-88 Rev.2: guidance mapping requires media-specific validation','IEEE 2883: future native method assessment','DoD 5220.22-M: legacy reference only'],
            'limitations':'No certification. Cannot address SSD wear leveling, snapshots, journals or remapped sectors. Original uploaded evidence is retained.'}

@app.post('/api/cases/{case_id}/policy')
def policy(case_id:str,data:Operation,actor=Depends(auth.authenticate)):
    case_access(case_id,actor,True)
    result=[policy_for(source_record(sid,case_id),data) for sid in data.source_ids]
    store.record(actor,'POLICY_GENERATED',case_id,{'policies':result})
    return result

@app.post('/api/cases/{case_id}/jobs')
def run_job(case_id:str,data:Operation,actor=Depends(auth.authenticate)):
    case_access(case_id,actor,True)
    sources=[source_record(sid,case_id) for sid in dict.fromkeys(data.source_ids)]
    if data.module in ('drive','files') and data.confirmation!='ERASE SANDBOX COPY':
        raise HTTPException(400,'Type ERASE SANDBOX COPY to authorize the working-copy operation')
    if data.module=='drive' and (len(sources)!=1 or sources[0]['kind']!='image'):
        raise HTTPException(400,'Drive erasure requires one raw image')
    if data.module=='files' and any(s['kind']!='file' for s in sources):
        raise HTTPException(400,'File/folder erasure requires uploaded file targets')
    if not worker_lock.acquire(blocking=False):
        raise HTTPException(409,'Another operation is running. Retry after it completes.')
    jid=store.uid()
    folder=store.ROOT/'jobs'/jid
    folder.mkdir(parents=True)
    start=time.perf_counter()
    with store.connection() as db:
        db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?)',(jid,case_id,data.module,'RUNNING',store.now(),'{}'))
    store.record(actor,'JOB_STARTED',case_id,{'job_id':jid,'module':data.module,'sources':[s['id'] for s in sources]})
    result={'items':[],'scope':'Sandbox copies only; original source evidence retained','bytes_processed':0}
    try:
        for source in sources:
            original=source_path(source['id']).read_bytes()
            if engines.sha(original)!=source['hash']:
                raise ValueError('Source integrity mismatch; operation stopped')
            result['bytes_processed']+=len(original)
            if data.module in ('drive','files'):
                target=folder/source['id']
                target.write_bytes(original)
                item=engines.sanitize(target,unlink=data.module=='files')
                item['policy']=policy_for(source,data)
                # Drive work copies are retained for post-operation inspection; no raw physical writes.
            else:
                scan=engines.carve(original,data.types)
                recovered=[]
                for hit in scan.pop('files'):
                    blob=hit.pop('data')
                    eid=store.uid()
                    hit['id']=eid
                    if data.module=='recovery':
                        (folder/eid).write_bytes(blob)
                        with store.connection() as db:
                            db.execute('INSERT INTO evidence VALUES(?,?,?,?)',(eid,case_id,jid,store.canonical(hit)))
                        store.record(actor,'FILE_RECOVERED',case_id,{'job_id':jid,'source_id':source['id'],**hit})
                    recovered.append(hit)
                item={**scan,'ground_truth':engines.ground_truth(original,recovered),'files':recovered,'validation':'WARNING' if recovered else ('PASS' if scan['complete'] else 'INCONCLUSIVE'),
                      'validation_scope':'Supported contiguous formats only; absence of results is not proof of complete erasure'}
            item['source_id']=source['id']
            item['source_unchanged']=engines.sha(source_path(source['id']).read_bytes())==source['hash']
            if not item['source_unchanged']:
                raise ValueError('Original source changed during operation')
            result['items'].append(item)
        result['duration_seconds']=time.perf_counter()-start
        result['throughput_mib_s']=result['bytes_processed']/1048576/max(result['duration_seconds'],1e-9)
        with store.connection() as db:
            db.execute('UPDATE jobs SET status=?,result=? WHERE id=?',('COMPLETED',store.canonical(result),jid))
        store.record(actor,'JOB_COMPLETED',case_id,{'job_id':jid,'module':data.module,**result})
        return {'id':jid,'status':'COMPLETED','result':result}
    except Exception as exc:
        result['error']=str(exc)[:300]
        with store.connection() as db:
            db.execute('UPDATE jobs SET status=?,result=? WHERE id=?',('FAILED',store.canonical(result),jid))
        store.record(actor,'JOB_FAILED',case_id,{'job_id':jid,'error':result['error']})
        raise HTTPException(422,result['error'])
    finally:
        worker_lock.release()

@app.post('/api/cases/{case_id}/benchmark')
def benchmark(case_id:str,actor=Depends(auth.authenticate)):
    case_access(case_id,actor,True)
    if not worker_lock.acquire(blocking=False):
        raise HTTPException(409,'Another operation is running')
    jid=store.uid()
    folder=store.ROOT/'jobs'/jid
    folder.mkdir(parents=True)
    try:
        start=time.perf_counter()
        data,payloads=engines.fixture()
        scan=engines.carve(data)
        hashes={f['sha256'] for f in scan['files']}
        expected={engines.sha(b.rstrip()) if b.startswith(b'%PDF-') else engines.sha(b) for b in payloads}
        target=folder/'benchmark.img'
        target.write_bytes(data)
        cleared=engines.sanitize(target,True)
        corrupted=bytearray(data)
        png_start=data.find(engines.SIGNATURES['png'])
        corrupted[png_start+20]^=1
        invalid=engines.carve(bytes(corrupted),['png'])
        result={'fixture':'Generated raw image: 8 known files, no filesystem metadata','bytes_processed':len(data),
                'checks':{'eight_artifacts_recovered':len(hashes)==8,'hashes_match_ground_truth':hashes==expected,
                'malformed_png_rejected':len(invalid['files'])==1 and any(r['offset']==png_start for r in invalid['rejected']),'readback_zeroed':cleared['readback_verified'],
                'post_erase_no_supported_artifacts':cleared['validation']=='PASS','working_copy_removed':cleared['absence_verified']},
                'duration_seconds':time.perf_counter()-start,'limits':'Small synthetic contiguous-file fixture; not independent certification or physical-media validation'}
        result['throughput_mib_s']=len(data)/1048576/max(result['duration_seconds'],1e-9)
        result['ground_truth']=engines.ground_truth(data,scan['files'])
        result['passed']=all(result['checks'].values())
        with store.connection() as db:
            db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?)',(jid,case_id,'benchmark','COMPLETED',store.now(),store.canonical(result)))
        store.record(actor,'VALIDATION_BENCHMARK_COMPLETED',case_id,{'job_id':jid,**result})
        return result
    finally:
        shutil.rmtree(folder,ignore_errors=True)
        worker_lock.release()

@app.get('/api/cases/{case_id}/timeline')
def timeline(case_id:str,user:str='',action:str='',source:str='',start:str='',end:str='',actor=Depends(auth.authenticate)):
    case_access(case_id,actor)
    rows=store.case_timeline(case_id)
    return [r for r in rows if (not user or user.lower() in r['user'].lower()) and (not action or action in r['action']) and (not source or source in store.canonical(r['details'])) and (not start or r['timestamp']>=start) and (not end or r['timestamp']<=end)]

@app.post('/api/cases/{case_id}/audit/verify')
def audit(case_id:str,actor=Depends(auth.authenticate)):
    case_access(case_id,actor)
    result=store.verify(store.events(case_id))
    store.record(actor,'AUDIT_VERIFIED',case_id,result)
    return result

@app.post('/api/cases/{case_id}/audit/tamper-demo')
def tamper_demo(case_id:str,actor=Depends(auth.authenticate)):
    admin(actor)
    case_access(case_id,actor)
    rows=store.events(case_id)
    if rows:
        rows[0]['action']='MODIFIED_COPY_ONLY'
    result=store.verify(rows)
    store.record(actor,'TAMPER_DEMO_ON_COPY',case_id,result)
    return {'copy_result':result,'primary_result':store.verify(store.events(case_id))}

@app.get('/api/security-events')
def security_events(actor=Depends(auth.authenticate)):
    admin(actor)
    return store.events(None)

@app.get('/api/evidence/{evidence_id}/download')
def download_evidence(evidence_id:str,actor=Depends(auth.authenticate)):
    with store.connection() as db:
        row=db.execute('SELECT * FROM evidence WHERE id=?',(evidence_id,)).fetchone()
    if not row:
        raise HTTPException(404,'Evidence not found')
    case_access(row['case_id'],actor)
    details=json.loads(row['details'])
    path=store.ROOT/'jobs'/row['job_id']/row['id']
    if not path.exists() or engines.sha(path.read_bytes())!=details['sha256']:
        raise HTTPException(409,'Evidence integrity check failed')
    store.record(actor,'EVIDENCE_DOWNLOADED',row['case_id'],{'evidence_id':evidence_id,'sha256':details['sha256']})
    return FileResponse(path,filename='recovered-'+evidence_id+'.'+details['type'],media_type='application/octet-stream')

@app.post('/api/cases/{case_id}/reports')
def generate_report(case_id:str,actor=Depends(auth.authenticate)):
    case_access(case_id,actor,True)
    detail=case_detail(case_id,actor)
    rid=store.uid()
    payload={'id':rid,'case':detail['case'],'operator':{k:actor[k] for k in ('id','email','role','session_id')},'created':store.now(),
             'scope':'SIH sandbox demonstrator. Not a certified sanitization certificate. Original sources retained.',
             'sources':detail['sources'],'jobs':detail['jobs'],'evidence':detail['evidence'],'timeline':detail['events'],
             'audit':store.verify(store.events(case_id))}
    blob=reports.pdf(payload)
    payload['pdf_sha256']=engines.sha(blob)
    envelope=reports.sign(payload)
    folder=store.ROOT/'reports'
    folder.mkdir(exist_ok=True)
    (folder/(rid+'.pdf')).write_bytes(blob)
    with store.connection() as db:
        db.execute('INSERT INTO reports VALUES(?,?,?,?,?)',(rid,case_id,payload['created'],store.canonical(envelope),payload['pdf_sha256']))
    store.record(actor,'REPORT_GENERATED',case_id,{'report_id':rid,'pdf_sha256':payload['pdf_sha256'],'key_fingerprint':envelope['key_fingerprint']})
    return {'id':rid,'key_fingerprint':envelope['key_fingerprint']}

@app.get('/api/reports/{report_id}/{format}')
def download_report(report_id:str,format:Literal['json','pdf'],actor=Depends(auth.authenticate)):
    with store.connection() as db:
        row=db.execute('SELECT * FROM reports WHERE id=?',(report_id,)).fetchone()
    if not row:
        raise HTTPException(404,'Report not found')
    case_access(row['case_id'],actor)
    envelope=json.loads(row['envelope'])
    try:
        reports.verify_envelope(envelope)
    except Exception:
        raise HTTPException(409,'Report signature invalid')
    store.record(actor,'REPORT_DOWNLOADED',row['case_id'],{'report_id':report_id,'format':format})
    if format=='json':
        return Response(store.canonical(envelope),media_type='application/json',headers={'Content-Disposition':f'attachment; filename="retrace-{report_id}.json"'})
    path=store.ROOT/'reports'/(report_id+'.pdf')
    if not path.exists() or engines.sha(path.read_bytes())!=envelope['payload']['pdf_sha256']:
        raise HTTPException(409,'PDF hash mismatch')
    return FileResponse(path,filename=f'retrace-{report_id}.pdf',media_type='application/pdf')

class ReportEnvelope(BaseModel):
    payload:dict
    signature:str
    public_key:str

@app.post('/api/reports/verify-signature')
def verify_report(data:ReportEnvelope,actor=Depends(auth.authenticate)):
    try:
        reports.verify_envelope(data.model_dump())
        return {'status':'VALID','trust':'Verify the public-key fingerprint against an independently saved value'}
    except Exception:
        return {'status':'BROKEN'}
