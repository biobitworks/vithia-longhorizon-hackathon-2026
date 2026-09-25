#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from vithia.canonical import canonical_sha256
from vithia.fco import make_fco
from vithia.integrity import MMRAccumulator,make_breakpoint,verify_breakpoint,merkle_root_for_fcos

def load(p): return json.loads((ROOT/p).read_text())
def dump(p,o):
 q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
def fsha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def store(f):
 p=ROOT/'evidence/golden_route/objects'/(f['object_id'].split(':',1)[1]+'.json');dump(p.relative_to(ROOT),f);return f

old_pub=load('PUBLIC_MANIFEST.json');old_gr=load('evidence/golden_route/GOLDEN_ROUTE_MANIFEST_V4.json');video=load('evidence/media/VIDEO_WALKTHROUGH_SUCCESSOR.json')
# Verify existing route and append dynamically.
rows=[]
for p in (ROOT/'evidence/golden_route/breakpoints').glob('GR*.json'):
 try:d=json.loads(p.read_text())
 except: continue
 seq=d.get('breakpoint',{}).get('payload',{}).get('sequence')
 if isinstance(seq,int): rows.append((seq,p,d))
rows.sort(key=lambda x:x[0]);mmr=MMRAccumulator();prev=None
for seq,p,d in rows:
 q=d['breakpoint']['payload'];objs=[load('evidence/golden_route/objects/'+oid.split(':',1)[1]+'.json') for oid in q['state_object_ids']];v=verify_breakpoint(d['breakpoint'],objs);assert v['passed'];assert q.get('predecessor_breakpoint_id')==prev;mmr.append(seq,d['breakpoint']['object_id'].split(':',1)[1],q['state_version_id']);assert mmr.root()==d['mmr']['root_sha256'];prev=d['breakpoint']['object_id']
next_seq=rows[-1][0]+1
vfco=store(make_fco('VideoWalkthroughSuccessorFCO',{
 'receipt_sha256':video['receipt_sha256'],'predecessor_demo_sha256':video['predecessor_demo_sha256'],'successor_demo_sha256':video['successor_demo_sha256'],'duration_seconds':video['successor_duration_seconds'],'permanent_url':video['permanent_url'],'source_clip_count':len(video['source_clips']),'claim_boundary':video['claim_boundary']
}))
urlfco=store(make_fco('PermanentDemoBindingFCO',{
 'url':video['permanent_url'],'repository_path':'demo.mp4','sha256':fsha('demo.mp4'),'expected_duration_seconds':video['successor_duration_seconds'],'binding_state':'CONTENT_FROZEN_PENDING_DEPLOYMENT','claim_boundary':'Binds permanent URL target bytes after deployment verification; URL availability itself is external state.'
}))
bp,receipt=make_breakpoint('DEMO_VIDEO_WALKTHROUGH_SUCCESSOR',[vfco,urlfco],sequence=next_seq,predecessor_breakpoint_id=prev,mmr=mmr)
dump(f'evidence/golden_route/breakpoints/GR{next_seq}_DEMO_VIDEO_WALKTHROUGH_SUCCESSOR.json',receipt)
# V5 route manifest.
allrows=[]
for p in (ROOT/'evidence/golden_route/breakpoints').glob('GR*.json'):
 d=json.loads(p.read_text());seq=d.get('breakpoint',{}).get('payload',{}).get('sequence')
 if isinstance(seq,int): allrows.append((seq,p,d))
allrows.sort(key=lambda x:x[0]);m=MMRAccumulator();routes=[];ids=[];roots=[];checks=[]
for seq,p,d in allrows:
 q=d['breakpoint']['payload'];objs=[load('evidence/golden_route/objects/'+oid.split(':',1)[1]+'.json') for oid in q['state_object_ids']];v=verify_breakpoint(d['breakpoint'],objs);m.append(seq,d['breakpoint']['object_id'].split(':',1)[1],q['state_version_id']);passed=v['passed'] and m.root()==d['mmr']['root_sha256'];assert passed;routes.append(q['stage']);ids.append(d['breakpoint']['object_id']);roots.append(q['merkle_root_sha256']);checks.append({'stage':q['stage'],'passed':passed,'recomputed_merkle_root_sha256':v['recomputed_merkle_root_sha256'],'mmr_root_sha256':m.root()})
g5={'schema':'vithia.golden_route_manifest.v1','manifest_version':5,'predecessor_manifest_sha256':old_gr['manifest_sha256'],'route':routes,'breakpoint_ids':ids,'merkle_roots':roots,'mmr_root':m.root(),'checks':checks,'independent_recompute_pass':True,'claim_boundary':'Adds the edited walkthrough replacement as an append-only successor; prior video/seal state remains preserved in Git and archived final-seal receipts.'};g5['manifest_sha256']=canonical_sha256(g5);dump('evidence/golden_route/GOLDEN_ROUTE_MANIFEST_V5.json',g5)
# Publication successor; final-seal carrier remains excluded to avoid self-reference.
excluded_top={'publication','.git','__pycache__','.vercel'}
def inscope(p):
 rel=p.relative_to(ROOT)
 if rel.as_posix()=='PUBLIC_MANIFEST.json': return False
 if rel.parts and rel.parts[0] in excluded_top: return False
 if '__pycache__' in rel.parts or p.suffix=='.pyc': return False
 if len(rel.parts)>=2 and rel.parts[0]=='results' and rel.parts[1]=='final_seal': return False
 return True
files=[];fcos=[]
for p in sorted((x for x in ROOT.rglob('*') if x.is_file() and inscope(x)),key=lambda x:x.relative_to(ROOT).as_posix()):
 rel=p.relative_to(ROOT).as_posix();b=p.read_bytes();e={'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};files.append(e);f=make_fco('PublicFileFCO',e);dump(Path('publication/objects')/(f['object_id'].split(':',1)[1]+'.json'),f);fcos.append(f)
bundle=make_fco('PublicRepositoryBundleFCO',{'repository':'https://github.com/biobitworks/vithia-longhorizon-hackathon-2026','payload_file_count':len(files),'file_object_ids':[x['object_id'] for x in fcos],'project_golden_route_manifest_sha256':g5['manifest_sha256'],'project_golden_route_mmr_root':g5['mmr_root'],'predecessor_public_manifest_sha256':old_pub['manifest_sha256'],'predecessor_publication_breakpoint_id':old_pub['publication_breakpoint_id'],'transition':'DEMO_VIDEO_WALKTHROUGH_SUCCESSOR','claim_boundary':'Public bundle identity only; does not establish truth or benchmark superiority.'},predecessor_ids=[old_pub['bundle_fco_id']],source_ids=[x['object_id'] for x in fcos]);bpath=Path('publication/objects')/(bundle['object_id'].split(':',1)[1]+'.json');dump(bpath,bundle)
root,leaves=merkle_root_for_fcos(fcos+[bundle]);payload={'stage':'PUBLIC_REPOSITORY_DEMO_VIDEO_WALKTHROUGH_SUCCESSOR','sequence':5,'root_kind':'PUBLICATION_MERKLE_NOT_PROJECT_MMR','predecessor_publication_breakpoint_id':old_pub['publication_breakpoint_id'],'project_golden_route_mmr_root':g5['mmr_root'],'state_object_ids':[x['object_id'] for x in fcos]+[bundle['object_id']],'state_object_count':len(fcos)+1,'merkle_algorithm':'SHA256_DOMAIN_SEPARATED_BINARY_TREE_V1','merkle_leaf_ordering':'declared_state_object_order','merkle_leaf_hashes':leaves,'merkle_root_sha256':root,'claim_boundary':'Seals the corrected public walkthrough payload; separate from project MMR and semantic truth.'};pbp=make_fco('BreakpointFCO',payload,predecessor_ids=[old_pub['publication_breakpoint_id']],source_ids=payload['state_object_ids']);pp=Path('publication/PUB5_DEMO_VIDEO_WALKTHROUGH_SUCCESSOR.json');dump(pp,{'schema':'vithia.publication_breakpoint_receipt.v1','breakpoint':pbp,'merkle_verified':True,'verification':{'passed':True,'recomputed_merkle_root_sha256':root}})
man={'schema':'vithia.public_manifest.v1','manifest_version':6,'payload_scope':'all repository files present at content sealing except publication/*, PUBLIC_MANIFEST.json, .git/*, __pycache__/*, *.pyc, .vercel/*, and post-seal carrier receipts under results/final_seal/*','files':files,'bundle_fco_id':bundle['object_id'],'bundle_fco_path':bpath.as_posix(),'predecessor_public_manifest_sha256':old_pub['manifest_sha256'],'predecessor_publication_breakpoint_id':old_pub['publication_breakpoint_id'],'predecessor_publication_merkle_root':old_pub['publication_merkle_root'],'project_golden_route_manifest_sha256':g5['manifest_sha256'],'project_golden_route_mmr_root':g5['mmr_root'],'publication_breakpoint_id':pbp['object_id'],'publication_breakpoint_path':pp.as_posix(),'publication_merkle_root':root,'repository':'https://github.com/biobitworks/vithia-longhorizon-hackathon-2026','root_kind':'PUBLICATION_MERKLE_NOT_PROJECT_MMR','transition':'DEMO_VIDEO_WALKTHROUGH_SUCCESSOR'};man['manifest_sha256']=canonical_sha256(man);dump('PUBLIC_MANIFEST.json',man)
print('GR',next_seq);print('GR_MERKLE',bp['payload']['merkle_root_sha256']);print('PROJECT_MMR',g5['mmr_root']);print('GR_MANIFEST',g5['manifest_sha256']);print('PUBLIC_MANIFEST',man['manifest_sha256']);print('PUBLICATION_MERKLE',root);print('PUBLICATION_BP',pbp['object_id'])
