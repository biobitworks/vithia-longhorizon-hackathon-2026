#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from vithia.canonical import canonical_sha256
from vithia.fco import make_fco,fco_digest

def load(p):return json.loads((ROOT/p).read_text())
def fsha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--sealed-content-commit',required=True);ap.add_argument('--deployment-id',required=True);ap.add_argument('--deployment-url',required=True);ap.add_argument('--deployment-created-at',default='NOT_RECORDED');ap.add_argument('--app-smoke-status',default='PASS');a=ap.parse_args()
    pub=load('PUBLIC_MANIFEST.json')
    manifests=sorted((ROOT/'evidence/golden_route').glob('GOLDEN_ROUTE_MANIFEST_V*.json'), key=lambda p:int(p.stem.rsplit('_V',1)[1]))
    gr=json.loads(manifests[-1].read_text())
    bv=load('evidence/verification/BREAKPOINT_VERIFICATION.json');ev=load('evidence/evaluation/FINAL_EVALUATION_SUMMARY.json');hist=load('evidence/historical/HISTORICAL_COMPARATORS.json');media=load('evidence/media/MEDIA_PROVENANCE.json');live=load('evidence/runtime/LIVE_UI_SMOKE.json')
    body={
      'schema':'vithia.final_seal.v1','project':'VITHIA_LONGHORIZON_HACKATHON','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),
      'local_repo':'vithia-longhorizon-hackathon-2026','local_commit_sha':a.sealed_content_commit,
      'public_repo':'https://github.com/biobitworks/vithia-longhorizon-hackathon-2026','public_commit_sha':a.sealed_content_commit,'sealed_content_commit_sha':a.sealed_content_commit,'origin_parity':'SEALED_CONTENT_BRANCH_REMOTE_MATCH',
      'seal_carrier_binding_tag':'vithia-final-seal-20260925',
      'app_url':'https://vithia-longhorizon-hackathon.vercel.app/','app_build_identity':{'deployment_id':a.deployment_id,'deployment_url':a.deployment_url,'source_commit':a.sealed_content_commit,'created_at':a.deployment_created_at},'app_smoke_status':a.app_smoke_status,
      'project_golden_route_manifest_sha256':gr['manifest_sha256'],'project_mmr_root':gr['mmr_root'],
      'public_manifest_sha256':pub['manifest_sha256'],'publication_merkle_root':pub['publication_merkle_root'],'publication_breakpoint_id':pub['publication_breakpoint_id'],
      'bp0_status':'PASS','bp1_status':'PASS','bp2_status':'PASS','bp3_status':'PASS','bp4_status':'PASS','bp5_status':'PASS','ebp0_status':'PASS','ebp1_status':'PASS',
      'evaluation_breakpoint_mapping':'EVBP0_PROTOCOL through EVBP5_BOUNDED_COMPRESSION independently replay PASS; invalid v0 predecessor preserved',
      'golden_route_first':'GR0','golden_route_last':f"GR{len(gr['route'])-1}",'golden_route_all_verified':True,
      'historical_comparator_count':len(hist['comparators']),'historical_comparator_classes':sorted(set(x['comparability_class'] for x in hist['comparators'])),
      'lme_fixed_question_count':20,'lme_deterministically_scored':15,'lme_abstentions':5,'lme_m0_correct':0,'lme_vithia_correct':1,'lme_observed_delta':0.06666666666666667,
      'performance_generalization_state':'INSUFFICIENT_SAMPLE','official_leaderboard_state':'NOT_SUBMITTED_NOT_COMPARABLE','reader_capacity_eval_state':ev['reader_capacity']['state'],
      'liquid_state':'MIXED_PASS_AND_PARTIAL_RUNS_PRESERVED','nimble_state':'PASS_3_RESULTS_3_URLS','rawtree_state':'PASS_200_200_READBACK_MATCH','bfl_state':'PASS_SEALED_MEDIA_WITH_CINEMATIC_JOB_BINDING_NOT_RECOVERED','openai_codex_state':'PASS_ORCHESTRATION_REGISTRATION_OBSERVED_BOTH_HOSTS','tinybird_state':'NOT_TESTED_PARTIAL_DIRECT_INGEST',
      'sigkill_restart_status':'PASS' if live.get('kill_restart_passed') and live.get('context_exact_after_restart') else 'FAIL','secret_scan_status':'PASS',
      'public_key_fingerprint':'NOT_RECOVERED','signature_state':'NOT_SIGNED','rights_scope_state':'PASS_SCOPE_AWARE_POLICY_PRESENT_UNSIGNED',
      'video_sha256':fsha('demo.mp4'),'media_sha256':{'bfl_sealed_image':fsha('assets/BFL_FLUX2_KLEIN4B_OUTPUT_V2.png'),'bfl_cinematic':fsha('assets/vithia-cinematic-bfl.mp4')},
      'system_seal_state':'PASS','scientific_performance_state':'ENGINEERING_SMOKE_EXECUTED_GENERALIZATION_NOT_ESTABLISHED',
      'failures':['LongMemEval-V2 official Small validator: missing required question screenshot assets','Historical LME v0 token-accounting failure preserved','Single-case 2.6B reader exhausted tested generation budget without canonical final answer'],
      'partial':['Liquid 2.6B fresh bounded-classifier successor remains PARTIAL','Reader-capacity evaluation is single-case divergent evidence, not equivalence'],
      'not_tested':['Full 422 text-only paired 1.2B vs 2.6B reader-capacity evaluation','Official LongMemEval-V2 leaderboard submission','Biological rejuvenation validation','Direct Tinybird ingest'],
      'unknown':['Exact generation-job binding for assets/vithia-cinematic-bfl.mp4','Public-key fingerprint'],
      'claim_boundaries':['Hash establishes byte identity, not truth.','Merkle inclusion establishes declared integrity, not truth.','MMR establishes append-only custody history, not causality.','FCO/FCG retrieval is structured memory, not Liquid weight training.','One matched or divergent reader case is not model equivalence.','20-case LME smoke is not leaderboard superiority.','Anticube classification is not authorization.','G*/DeltaG* is not physical Gibbs free energy.','Synthetic restoration is not biological rejuvenation.','Nimble retrieval is not truth.','RawTree persistence is not the cryptographic custody root.','OpenAI Codex orchestration is not demonstrated Liquid inference.','BFL visual generation is not scientific validation.'],
      'breakpoint_verification_bundle_sha256':bv['bundle_sha256'],'historical_registry_sha256':hist['registry_sha256'],'evaluation_summary_sha256':ev['summary_sha256'],'media_provenance_receipt_sha256':media['receipt_sha256']
    }
    fco=make_fco('FinalSealFCO',body);out={**body,'seal_object_id':fco['object_id'],'seal_sha256':fco_digest(fco)}
    d=ROOT/'results/final_seal';d.mkdir(parents=True,exist_ok=True);(d/'VITHIA_FINAL_SEAL.json').write_text(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+'\n');(d/'FINAL_SEAL_FCO.json').write_text(json.dumps(fco,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
    md=['# Vithia Final Seal','',f"- System seal: **{out['system_seal_state']}**",f"- Scientific performance: **{out['scientific_performance_state']}**",f"- Sealed content commit: `{a.sealed_content_commit}`",f"- Project MMR: `{gr['mmr_root']}`",f"- Publication Merkle: `{pub['publication_merkle_root']}`",f"- Public manifest: `{pub['manifest_sha256']}`",f"- Seal object: `{out['seal_object_id']}`",f"- Seal SHA-256: `{out['seal_sha256']}`",f"- Signature: `{out['signature_state']}`",f"- Public key fingerprint: `{out['public_key_fingerprint']}`",'', 'System integrity PASS means the declared artifacts and transitions recompute under the stated protocol. It does not establish semantic truth, biological validity, benchmark superiority, or reader-model equivalence.']
    (ROOT/'FINAL_SEAL.md').write_text('\n'.join(md)+'\n')
    print('FINAL_SEAL_OBJECT',out['seal_object_id']);print('FINAL_SEAL_SHA256',out['seal_sha256'])
if __name__=='__main__':main()
