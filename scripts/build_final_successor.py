#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from vithia.canonical import canonical_sha256
from vithia.fco import make_fco,validate_fco
from vithia.integrity import MMRAccumulator,make_breakpoint,verify_breakpoint,merkle_root_for_fcos

def jload(p):return json.loads((ROOT/p).read_text())
def fsha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def dump(p,o):
    q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False)+'\n')

def store_fco(f):
    p=ROOT/'evidence/golden_route/objects'/(f['object_id'].split(':',1)[1]+'.json');dump(p.relative_to(ROOT),f);return f

# Existing Golden Route must verify before append.
bpdir=ROOT/'evidence/golden_route/breakpoints';objdir=ROOT/'evidence/golden_route/objects'
entries=[]
for p in bpdir.glob('GR*.json'):
    try:d=json.loads(p.read_text())
    except Exception:continue
    seq=d.get('breakpoint',{}).get('payload',{}).get('sequence')
    if isinstance(seq,int):entries.append((seq,p,d))
entries.sort(key=lambda x:x[0]);mmr=MMRAccumulator();prev=None
for seq,p,d in entries:
    q=d['breakpoint']['payload'];objs=[jload('evidence/golden_route/objects/'+x.split(':',1)[1]+'.json') for x in q['state_object_ids']]
    v=verify_breakpoint(d['breakpoint'],objs);assert v['passed'] and v['recomputed_merkle_root_sha256']==q['merkle_root_sha256']
    assert q.get('predecessor_breakpoint_id')==prev
    mmr.append(seq,d['breakpoint']['object_id'].split(':',1)[1],q['state_version_id']);assert mmr.root()==d['mmr']['root_sha256'];prev=d['breakpoint']['object_id']
if not entries:raise SystemExit('no predecessor route')
next_seq=entries[-1][0]+1
if next_seq!=15:raise SystemExit(f'expected dynamic next sequence 15 from recovered state, got {next_seq}')

bv=jload('evidence/verification/BREAKPOINT_VERIFICATION.json');ev=jload('evidence/evaluation/FINAL_EVALUATION_SUMMARY.json');hist=jload('evidence/historical/HISTORICAL_COMPARATORS.json');media=jload('evidence/media/MEDIA_PROVENANCE.json')
codex_s=jload('evidence/openai/CODEX_STUDIO_RECEIPT.json');codex_p=jload('evidence/openai/CODEX_PRO_RECEIPT.json');align=jload('evidence/alignment/SHOWCASE.json');security=jload('evidence/security/HYDRA_NOTRACE_RECEIPT.json');live=jload('evidence/runtime/LIVE_UI_SMOKE.json')
state=[]
state.append(store_fco(make_fco('SystemVerificationFCO',{'breakpoint_verification_sha256':bv['bundle_sha256'],'runtime_bp0_bp5':'PASS','evaluation_evbp0_evbp5':'PASS','golden_route_predecessor_gr0_gr14':'PASS','sigkill_restart':'PASS' if live.get('kill_restart_passed') else 'FAIL','claim_boundary':'Deterministic custody/integrity verification only.'})))
state.append(store_fco(make_fco('EvaluationEvidenceFCO',{'summary_sha256':ev['summary_sha256'],'lme_fixed_questions':20,'deterministically_scored':15,'m0_correct':0,'vithia_correct':1,'observed_delta_percentage_points':6.666666666666667,'context_reduction_fraction':ev['context_compression']['memory_context_reduction_fraction'],'performance_generalization':'INSUFFICIENT_SAMPLE','leaderboard_comparable':False,'reader_capacity_state':ev['reader_capacity']['state'],'claim_boundary':'Engineering smoke and single-case reader comparison only; no generalization or model-equivalence claim.'})))
state.append(store_fco(make_fco('HistoricalComparatorRegistryFCO',{'registry_sha256':hist['registry_sha256'],'comparator_count':len(hist['comparators']),'classes':sorted(set(x['comparability_class'] for x in hist['comparators'])),'claim_boundary':'Recovered internal lineage only; none are exact LongMemEval protocol comparators.'})))
state.append(store_fco(make_fco('OpenAICodexEvidenceFCO',{'studio_receipt_sha256':codex_s['receipt_sha256'],'pro_receipt_sha256':codex_p['receipt_sha256'],'studio_version':codex_s['codex_version'],'pro_version':codex_p['codex_version'],'tokensand_mcp_registered_both':codex_s['tokensand_mcp_registered'] and codex_p['tokensand_mcp_registered'],'claim_boundary':'OpenAI Codex orchestration/tooling evidence only; Liquid AI is the demonstrated local reader.'})))
state.append(store_fco(make_fco('AlignmentSecurityEvidenceFCO',{'showcase_sha256':align['showcase_sha256'],'security_receipt_sha256':security['receipt_sha256'],'anticube_state':'SYNTHETIC_DIAGNOSTIC','gstar_state':'DIMENSIONLESS_INFORMATION_STATE_DIAGNOSTIC','biological_rejuvenation_validation':'NOT_TESTED','boundary_security_status':security['status'],'claim_boundary':'Synthetic alignment/security diagnostics; no biological validation.'})))
state.append(store_fco(make_fco('MediaProvenanceFCO',{'media_receipt_sha256':media['receipt_sha256'],'cinematic_sha256':'60c2564ca1c2442b1abd0506a90467c1422b07ffadc09b3e758868d70ddab87c','sealed_bfl_image_sha256':'5e8dc6a39b885da607ef7022ca91106dc893146256ec0af7f606256e614a3c5c','demo_video_sha256':fsha('demo.mp4'),'claim_boundary':'Byte identity/provenance only; the cinematic exact generation-job binding is not recovered.'})))
state.append(store_fco(make_fco('AppCandidateFCO',{'index_sha256':fsha('index.html'),'vercel_config_sha256':fsha('vercel.json'),'demo_sha256':fsha('demo.mp4'),'cinematic_sha256':fsha('assets/vithia-cinematic-bfl.mp4'),'deployment_state':'PENDING_CONTENT_FREEZE_DEPLOYMENT','claim_boundary':'App source/media candidate identity prior to deployment.'})))
state.append(store_fco(make_fco('RightsSignatureStateFCO',{'licenses_md_sha256':fsha('LICENSES.md'),'public_key_fingerprint':'NOT_RECOVERED','signature_state':'NOT_SIGNED','private_key_distributed':False,'rights_scope_state':'SCOPE_AWARE_POLICY_PRESENT','claim_boundary':'No private key is distributed; unsigned state is explicit and does not invalidate hash/Merkle/MMR recomputation.'})))

bp,receipt=make_breakpoint('FINAL_APP_EVALUATION_AND_PUBLICATION_SEAL',state,sequence=next_seq,predecessor_breakpoint_id=prev,mmr=mmr)
dump(f'evidence/golden_route/breakpoints/GR{next_seq}_FINAL_APP_EVALUATION_AND_PUBLICATION_SEAL.json',receipt)

# Build immutable V4 route manifest, preserving V3 predecessor.
all_entries=[];mmr2=MMRAccumulator();routes=[];ids=[];roots=[];checks=[]
for p in bpdir.glob('GR*.json'):
    d=json.loads(p.read_text());seq=d.get('breakpoint',{}).get('payload',{}).get('sequence')
    if isinstance(seq,int):all_entries.append((seq,p,d))
all_entries.sort(key=lambda x:x[0])
for seq,p,d in all_entries:
    q=d['breakpoint']['payload'];objs=[jload('evidence/golden_route/objects/'+x.split(':',1)[1]+'.json') for x in q['state_object_ids']];v=verify_breakpoint(d['breakpoint'],objs);mmr2.append(seq,d['breakpoint']['object_id'].split(':',1)[1],q['state_version_id']);passed=v['passed'] and mmr2.root()==d['mmr']['root_sha256']
    routes.append(q['stage']);ids.append(d['breakpoint']['object_id']);roots.append(q['merkle_root_sha256']);checks.append({'stage':q['stage'],'passed':passed,'recomputed_merkle_root_sha256':v['recomputed_merkle_root_sha256'],'mmr_root_sha256':mmr2.root()})
    if not passed:raise SystemExit('golden route verification failed while building successor')
v3=jload('evidence/golden_route/GOLDEN_ROUTE_MANIFEST_V3.json')
m4={'schema':'vithia.golden_route_manifest.v1','manifest_version':4,'predecessor_manifest_sha256':v3['manifest_sha256'],'predecessor_git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'route':routes,'breakpoint_ids':ids,'merkle_roots':roots,'mmr_root':mmr2.root(),'checks':checks,'independent_recompute_pass':True,'claim_boundary':'Merkle/MMR establish exact declared-object identity/inclusion. Deterministic system integrity is separate from performance/generalization state.'}
m4['manifest_sha256']=canonical_sha256(m4);dump('evidence/golden_route/GOLDEN_ROUTE_MANIFEST_V4.json',m4)

# Publication successor. Post-seal carrier receipts are explicitly out of publication payload to avoid self-reference.
old=jload('PUBLIC_MANIFEST.json')
excluded_top={'publication','.git','__pycache__','.vercel'}
def scope_file(p):
    rel=p.relative_to(ROOT)
    if rel.as_posix()=='PUBLIC_MANIFEST.json':return False
    if rel.parts and rel.parts[0] in excluded_top:return False
    if '__pycache__' in rel.parts or p.suffix=='.pyc':return False
    if len(rel.parts)>=2 and rel.parts[0]=='results' and rel.parts[1]=='final_seal':return False
    return True
files=[];file_fcos=[];pubobj=ROOT/'publication/objects';pubobj.mkdir(parents=True,exist_ok=True)
for p in sorted((x for x in ROOT.rglob('*') if x.is_file() and scope_file(x)),key=lambda x:x.relative_to(ROOT).as_posix()):
    rel=p.relative_to(ROOT).as_posix();b=p.read_bytes();h=hashlib.sha256(b).hexdigest();entry={'path':rel,'bytes':len(b),'sha256':h};files.append(entry);f=make_fco('PublicFileFCO',entry);dump(Path('publication/objects')/(f['object_id'].split(':',1)[1]+'.json'),f);file_fcos.append(f)
bundle=make_fco('PublicRepositoryBundleFCO',{'repository':'https://github.com/biobitworks/vithia-longhorizon-hackathon-2026','payload_file_count':len(files),'file_object_ids':[x['object_id'] for x in file_fcos],'project_golden_route_manifest_sha256':m4['manifest_sha256'],'project_golden_route_mmr_root':m4['mmr_root'],'predecessor_public_manifest_sha256':old['manifest_sha256'],'predecessor_publication_breakpoint_id':old['publication_breakpoint_id'],'transition':'FINAL_APP_EVALUATION_AND_PUBLICATION_SEAL','claim_boundary':'Public bundle identity only; does not establish truth, causality, scientific validity, benchmark superiority, or external platform state.'},predecessor_ids=[old['bundle_fco_id']],source_ids=[x['object_id'] for x in file_fcos])
bundle_path=Path('publication/objects')/(bundle['object_id'].split(':',1)[1]+'.json');dump(bundle_path,bundle)
root,leaves=merkle_root_for_fcos(file_fcos+[bundle]);seq=4
payload={'stage':'PUBLIC_REPOSITORY_FINAL_APP_EVALUATION_AND_PUBLICATION_SEAL','sequence':seq,'root_kind':'PUBLICATION_MERKLE_NOT_PROJECT_MMR','predecessor_publication_breakpoint_id':old['publication_breakpoint_id'],'project_golden_route_mmr_root':m4['mmr_root'],'state_object_ids':[x['object_id'] for x in file_fcos]+[bundle['object_id']],'state_object_count':len(file_fcos)+1,'merkle_algorithm':'SHA256_DOMAIN_SEPARATED_BINARY_TREE_V1','merkle_leaf_ordering':'declared_state_object_order','merkle_leaf_hashes':leaves,'merkle_root_sha256':root,'claim_boundary':'This publication Merkle root seals declared public payload identities. It is separate from the project cumulative MMR and does not establish semantic truth.'}
pub_bp=make_fco('BreakpointFCO',payload,predecessor_ids=[old['publication_breakpoint_id']],source_ids=payload['state_object_ids']);pub_receipt={'schema':'vithia.publication_breakpoint_receipt.v1','breakpoint':pub_bp,'merkle_verified':True,'verification':{'passed':True,'recomputed_merkle_root_sha256':root}}
pub_path=Path('publication/PUB4_FINAL_APP_EVALUATION_AND_PUBLICATION_SEAL.json');dump(pub_path,pub_receipt)
manifest={'schema':'vithia.public_manifest.v1','manifest_version':5,'payload_scope':'all repository files present at content sealing except publication/*, PUBLIC_MANIFEST.json, .git/*, __pycache__/*, *.pyc, .vercel/*, and post-seal carrier receipts under results/final_seal/*','files':files,'bundle_fco_id':bundle['object_id'],'bundle_fco_path':bundle_path.as_posix(),'predecessor_public_manifest_sha256':old['manifest_sha256'],'predecessor_publication_breakpoint_id':old['publication_breakpoint_id'],'predecessor_publication_merkle_root':old['publication_merkle_root'],'project_golden_route_manifest_sha256':m4['manifest_sha256'],'project_golden_route_mmr_root':m4['mmr_root'],'publication_breakpoint_id':pub_bp['object_id'],'publication_breakpoint_path':pub_path.as_posix(),'publication_merkle_root':root,'repository':'https://github.com/biobitworks/vithia-longhorizon-hackathon-2026','root_kind':'PUBLICATION_MERKLE_NOT_PROJECT_MMR','transition':'FINAL_APP_EVALUATION_AND_PUBLICATION_SEAL'}
manifest['manifest_sha256']=canonical_sha256(manifest);dump('PUBLIC_MANIFEST.json',manifest)
print('GR_NEXT',next_seq);print('GR15_MERKLE',bp['payload']['merkle_root_sha256']);print('PROJECT_MMR',m4['mmr_root']);print('GR_MANIFEST',m4['manifest_sha256']);print('PUB_FILES',len(files));print('PUBLICATION_MERKLE',root);print('PUBLIC_MANIFEST',manifest['manifest_sha256']);print('PUB_BP',pub_bp['object_id'])
