#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from vithia.canonical import canonical_sha256
from vithia.fco import make_fco
from vithia.integrity import merkle_root_for_fcos

def dump(p,o):
    q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
base=json.loads(subprocess.check_output(['git','show','HEAD:PUBLIC_MANIFEST.json'],text=True))
gr=json.loads((ROOT/'evidence/golden_route/GOLDEN_ROUTE_MANIFEST_V4.json').read_text())
excluded_top={'publication','.git','__pycache__','.vercel'}
def scope_file(p):
    rel=p.relative_to(ROOT)
    if rel.as_posix()=='PUBLIC_MANIFEST.json':return False
    if rel.parts and rel.parts[0] in excluded_top:return False
    if '__pycache__' in rel.parts or p.suffix=='.pyc':return False
    if len(rel.parts)>=2 and rel.parts[0]=='results' and rel.parts[1]=='final_seal':return False
    return True
files=[];fcos=[];objdir=ROOT/'publication/objects';objdir.mkdir(parents=True,exist_ok=True)
for p in sorted((x for x in ROOT.rglob('*') if x.is_file() and scope_file(x)),key=lambda x:x.relative_to(ROOT).as_posix()):
    rel=p.relative_to(ROOT).as_posix();b=p.read_bytes();entry={'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};files.append(entry);f=make_fco('PublicFileFCO',entry);dump(Path('publication/objects')/(f['object_id'].split(':',1)[1]+'.json'),f);fcos.append(f)
bundle=make_fco('PublicRepositoryBundleFCO',{'repository':'https://github.com/biobitworks/vithia-longhorizon-hackathon-2026','payload_file_count':len(files),'file_object_ids':[x['object_id'] for x in fcos],'project_golden_route_manifest_sha256':gr['manifest_sha256'],'project_golden_route_mmr_root':gr['mmr_root'],'predecessor_public_manifest_sha256':base['manifest_sha256'],'predecessor_publication_breakpoint_id':base['publication_breakpoint_id'],'transition':'FINAL_VIDEO_PRESENTER_OVERLAY_SUCCESSOR','claim_boundary':'Public bundle identity only; does not establish truth, causality, scientific validity, benchmark superiority, or external platform state.'},predecessor_ids=[base['bundle_fco_id']],source_ids=[x['object_id'] for x in fcos]);bundle_path=Path('publication/objects')/(bundle['object_id'].split(':',1)[1]+'.json');dump(bundle_path,bundle)
root,leaves=merkle_root_for_fcos(fcos+[bundle]);payload={'stage':'PUBLIC_REPOSITORY_FINAL_VIDEO_PRESENTER_OVERLAY_SUCCESSOR','sequence':5,'root_kind':'PUBLICATION_MERKLE_NOT_PROJECT_MMR','predecessor_publication_breakpoint_id':base['publication_breakpoint_id'],'project_golden_route_mmr_root':gr['mmr_root'],'state_object_ids':[x['object_id'] for x in fcos]+[bundle['object_id']],'state_object_count':len(fcos)+1,'merkle_algorithm':'SHA256_DOMAIN_SEPARATED_BINARY_TREE_V1','merkle_leaf_ordering':'declared_state_object_order','merkle_leaf_hashes':leaves,'merkle_root_sha256':root,'claim_boundary':'This publication Merkle root seals declared public payload identities. It is separate from the project cumulative MMR and does not establish semantic truth.'}
bp=make_fco('BreakpointFCO',payload,predecessor_ids=[base['publication_breakpoint_id']],source_ids=payload['state_object_ids']);pub={'schema':'vithia.publication_breakpoint_receipt.v1','breakpoint':bp,'merkle_verified':True,'verification':{'passed':True,'recomputed_merkle_root_sha256':root}};pub_path=Path('publication/PUB5_FINAL_VIDEO_PRESENTER_OVERLAY_SUCCESSOR.json');dump(pub_path,pub)
manifest={'schema':'vithia.public_manifest.v1','manifest_version':base.get('manifest_version',5)+1,'payload_scope':'all repository files present at content sealing except publication/*, PUBLIC_MANIFEST.json, .git/*, __pycache__/*, *.pyc, .vercel/*, and post-seal carrier receipts under results/final_seal/*','files':files,'bundle_fco_id':bundle['object_id'],'bundle_fco_path':bundle_path.as_posix(),'predecessor_public_manifest_sha256':base['manifest_sha256'],'predecessor_publication_breakpoint_id':base['publication_breakpoint_id'],'predecessor_publication_merkle_root':base['publication_merkle_root'],'project_golden_route_manifest_sha256':gr['manifest_sha256'],'project_golden_route_mmr_root':gr['mmr_root'],'publication_breakpoint_id':bp['object_id'],'publication_breakpoint_path':pub_path.as_posix(),'publication_merkle_root':root,'repository':'https://github.com/biobitworks/vithia-longhorizon-hackathon-2026','root_kind':'PUBLICATION_MERKLE_NOT_PROJECT_MMR','transition':'FINAL_VIDEO_PRESENTER_OVERLAY_SUCCESSOR'};manifest['manifest_sha256']=canonical_sha256(manifest);dump('PUBLIC_MANIFEST.json',manifest)
print('FILES',len(files));print('PUBLIC_MANIFEST',manifest['manifest_sha256']);print('PUBLICATION_MERKLE',root);print('PUBLICATION_BP',bp['object_id'])
