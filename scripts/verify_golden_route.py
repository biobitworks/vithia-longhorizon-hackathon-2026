#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from vithia.integrity import verify_breakpoint, MMRAccumulator
from vithia.canonical import canonical_sha256
GR=ROOT/'evidence/golden_route'; OBJ=GR/'objects'; BPD=GR/'breakpoints'
entries=[]
for p in BPD.glob('GR*.json'):
    try:d=json.loads(p.read_text())
    except Exception:continue
    seq=d.get('breakpoint',{}).get('payload',{}).get('sequence')
    if isinstance(seq,int):entries.append((seq,p,d))
entries.sort(key=lambda x:x[0]); ok=True; mmr=MMRAccumulator(); routes=[]; ids=[]; roots=[]; checks=[]
for seq,p,d in entries:
    q=d['breakpoint']['payload']; fcos=[]; missing=[]
    for oid in q['state_object_ids']:
        op=OBJ/(oid.split(':',1)[1]+'.json')
        if not op.exists():missing.append(str(op));continue
        fcos.append(json.loads(op.read_text()))
    v=verify_breakpoint(d['breakpoint'],fcos) if not missing else {'passed':False,'recomputed_merkle_root_sha256':'MISSING'}
    merkle_ok=v['passed'] and v['recomputed_merkle_root_sha256']==q['merkle_root_sha256']
    mmr.append(seq,d['breakpoint']['object_id'].split(':',1)[1],q['state_version_id']); mmr_ok=mmr.root()==d['mmr']['root_sha256']
    passed=merkle_ok and mmr_ok and not missing; ok &= passed
    routes.append(q['stage']);ids.append(d['breakpoint']['object_id']);roots.append(q['merkle_root_sha256'])
    checks.append({'stage':q['stage'],'passed':passed,'recomputed_merkle_root_sha256':v['recomputed_merkle_root_sha256'],'mmr_root_sha256':mmr.root()})
    print(f"{p.name}: {'PASS' if passed else 'FAIL'} merkle={v['recomputed_merkle_root_sha256']} mmr={mmr.root()}")
manifests=[]
for p in GR.glob('GOLDEN_ROUTE_MANIFEST_V*.json'):
    m=re.search(r'_V(\d+)\.json$',p.name)
    if m:manifests.append((int(m.group(1)),p))
if not manifests:raise SystemExit('no golden-route manifest')
_,latest=max(manifests); manifest=json.loads(latest.read_text())
manifest_hash=canonical_sha256({k:v for k,v in manifest.items() if k!='manifest_sha256'})
manifest_ok=(manifest_hash==manifest['manifest_sha256'] and manifest['route']==routes and manifest['breakpoint_ids']==ids and manifest['merkle_roots']==roots and manifest['mmr_root']==mmr.root() and manifest.get('independent_recompute_pass') is True)
print('LATEST_MANIFEST:',latest.name);print('MANIFEST_MATCH:',manifest_ok,manifest['manifest_sha256']);ok &= manifest_ok
media=ROOT/'assets/BFL_FLUX2_KLEIN4B_OUTPUT_V2.png'; receipt=ROOT/'evidence/sponsors/BFL_USAGE_RECEIPT_V2.json'
if media.exists() and receipt.exists():
    r=json.loads(receipt.read_text()); h=hashlib.sha256(media.read_bytes()).hexdigest(); media_ok=h==r.get('media_sha256');print('BFL_MEDIA_HASH_MATCH:',media_ok,h);ok &= media_ok
print('BREAKPOINT_COUNT:',len(entries));print('FINAL_MMR:',mmr.root());print('OVERALL:','PASS' if ok else 'FAIL')
raise SystemExit(0 if ok else 1)
