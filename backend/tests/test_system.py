import os
import tempfile
os.environ['RETRACE_DATA_DIR']=tempfile.mkdtemp(prefix='retrace-test-')
os.environ['AUTH_MODE']='local'
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import store, engines, reports, auth

client=TestClient(app)

def account(email):
    auth.limits.clear()
    r=client.post('/api/auth/register',json={'email':email,'password':'Test-Only-Password-42!'})
    assert r.status_code==200,r.text
    return r.json(),{'Authorization':'Bearer '+r.json()['token']}

@pytest.fixture(scope='module')
def ctx():
    a,headers=account('admin@example.com')
    case=client.post('/api/cases',headers=headers,json={'title':'Known evidence case'}).json()
    return a,headers,case['id']

def test_carve_true_files_and_integrity():
    data,payloads=engines.fixture()
    before=engines.sha(data)
    scan=engines.carve(data)
    assert scan['complete']
    assert {f['type'] for f in scan['files']}=={'png','jpeg','pdf','zip'}
    assert {f['sha256'] for f in scan['files']}=={engines.sha(b) for b in payloads}
    assert engines.sha(data)==before
    assert all(f['confidence']==95 and len(f['reasons'])==3 for f in scan['files'])

def test_corruption_and_bounded_scan():
    data,_=engines.fixture()
    broken=bytearray(data);broken[data.find(engines.SIGNATURES['png'])+20]^=1
    scan=engines.carve(bytes(broken),['png'])
    assert not scan['files'] and scan['rejected']
    assert not engines.carve(b'%PDF-bad'*300,['pdf'])['complete']
    assert not engines.carve(b'%PDF-1.7 truncated')['files']

def test_auth_required_and_viewer_isolation(ctx):
    _,headers,cid=ctx
    assert client.get('/api/cases').status_code==401
    viewer,vh=account('viewer@example.com')
    assert client.get('/api/cases/'+cid,headers=vh).status_code==404
    assert client.post('/api/cases',headers=vh,json={'title':'Forbidden'}).status_code==403
    assert client.post('/api/cases/'+cid+'/members',headers=headers,json={'user_id':viewer['user']['id']}).status_code==200
    assert client.get('/api/cases/'+cid,headers=vh).status_code==200
    assert client.post('/api/cases/'+cid+'/demo-source',headers=vh).status_code==403
    assert client.post('/api/cases/'+cid+'/reports',headers=vh).status_code==403
    assert client.post('/api/cases/'+cid+'/audit/tamper-demo',headers=vh).status_code==403
    assert client.post('/api/auth/logout',headers=vh).status_code==200
    assert client.get('/api/auth/me',headers=vh).status_code==401

def test_end_to_end_recovery_erase_reports(ctx):
    _,h,cid=ctx
    source=client.post('/api/cases/'+cid+'/demo-source',headers=h).json()
    op={'module':'recovery','source_ids':[source['id']]}
    response=client.post('/api/cases/'+cid+'/jobs',headers=h,json=op)
    assert response.status_code==200,response.text
    assert len(response.json()['result']['items'][0]['files'])==4
    detail=client.get('/api/cases/'+cid,headers=h).json()
    assert len(detail['evidence'])==4
    item=detail['evidence'][0]
    downloaded=client.get('/api/evidence/'+item['id']+'/download',headers=h)
    assert engines.sha(downloaded.content)==item['details']['sha256']
    op['module']='drive'
    assert client.post('/api/cases/'+cid+'/jobs',headers=h,json=op).status_code==400
    op['confirmation']='ERASE SANDBOX COPY'
    erased=client.post('/api/cases/'+cid+'/jobs',headers=h,json=op).json()['result']['items'][0]
    assert erased['readback_verified'] and erased['validation']=='PASS' and erased['source_unchanged']
    assert source['hash']==engines.sha((store.ROOT/'sources'/source['id']).read_bytes())
    assert client.post('/api/cases/'+cid+'/audit/verify',headers=h).json()['status']=='VALID'
    tamper=client.post('/api/cases/'+cid+'/audit/tamper-demo',headers=h).json()
    assert tamper['copy_result']['status']=='BROKEN' and tamper['primary_result']['status']=='VALID'
    report=client.post('/api/cases/'+cid+'/reports',headers=h)
    assert report.status_code==200,report.text
    rid=report.json()['id']
    envelope=client.get('/api/reports/'+rid+'/json',headers=h).json()
    pdf=client.get('/api/reports/'+rid+'/pdf',headers=h).content
    assert reports.verify_envelope(envelope)
    assert envelope['payload']['pdf_sha256']==engines.sha(pdf)
    assert pdf.startswith(b'%PDF-')
    envelope['payload']['scope']='altered'
    assert client.post('/api/reports/verify-signature',headers=h,json=envelope).json()['status']=='BROKEN'
    assert client.post('/api/cases/'+cid+'/benchmark',headers=h).json()['passed']

def test_batch_file_metadata_and_path_traversal(ctx):
    _,h,cid=ctx
    sources=[]
    for name in ('../../outside.txt','folder/nested.txt'):
        r=client.post('/api/cases/'+cid+'/sources',headers=h,files={'file':(name,b'private data')},data={'kind':'file','media':'SSD'})
        assert r.status_code==200,r.text
        assert '/' not in r.json()['name']
        sources.append(r.json()['id'])
    r=client.post('/api/cases/'+cid+'/jobs',headers=h,json={'module':'files','source_ids':sources,'confirmation':'ERASE SANDBOX COPY'})
    assert r.status_code==200,r.text
    for item in r.json()['result']['items']:
        assert item['absence_verified'] and item['metadata']['timestamps_reset'] and item['source_unchanged']
    folder=store.ROOT/'jobs'/r.json()['id']
    assert not list(folder.iterdir())

def test_cross_case_source_injection(ctx):
    _,h,cid=ctx
    second=client.post('/api/cases',headers=h,json={'title':'Other case'}).json()['id']
    source=client.post('/api/cases/'+second+'/demo-source',headers=h).json()
    r=client.post('/api/cases/'+cid+'/jobs',headers=h,json={'module':'recovery','source_ids':[source['id']]})
    assert r.status_code==404

def test_source_tampering_and_append_only(ctx):
    _,h,cid=ctx
    source=client.post('/api/cases/'+cid+'/demo-source',headers=h).json()
    (store.ROOT/'sources'/source['id']).write_bytes(b'altered')
    r=client.post('/api/cases/'+cid+'/jobs',headers=h,json={'module':'recovery','source_ids':[source['id']]})
    assert r.status_code==422
    assert 'integrity mismatch' in r.text
    import sqlite3
    with pytest.raises(sqlite3.IntegrityError):
        with store.connection() as db:db.execute("UPDATE events SET hash='bad'")
    assert store.verify(store.events(cid))['status']=='VALID'

def test_roles_never_from_client(ctx):
    _,h,_=ctx
    outsider,oh=account('outsider@example.com')
    assert outsider['user']['role']=='VIEWER'
    assert client.post('/api/users/'+outsider['user']['id']+'/role',headers=oh,json={'role':'ADMIN'}).status_code==403
    assert client.post('/api/users/'+outsider['user']['id']+'/role',headers=h,json={'role':'INVESTIGATOR'}).status_code==200
    assert client.get('/api/auth/me',headers=oh).status_code==401
