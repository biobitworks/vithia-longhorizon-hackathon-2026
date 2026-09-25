#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from vithia.fco import make_fco,fco_digest
seal_path=ROOT/'results/final_seal/VITHIA_FINAL_SEAL.json'
if not seal_path.exists():print('FINAL_SEAL: NOT_PRESENT');raise SystemExit(2)
s=json.loads(seal_path.read_text());body={k:v for k,v in s.items() if k not in {'seal_object_id','seal_sha256'}};f=make_fco('FinalSealFCO',body)
checks={}
checks['seal_object_id']=f['object_id']==s['seal_object_id'];checks['seal_sha256']=fco_digest(f)==s['seal_sha256']
pub=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text());manifests=sorted((ROOT/'evidence/golden_route').glob('GOLDEN_ROUTE_MANIFEST_V*.json'),key=lambda p:int(p.stem.rsplit('_V',1)[1]));gr=json.loads(manifests[-1].read_text())
checks['public_manifest']=pub['manifest_sha256']==s['public_manifest_sha256'];checks['publication_merkle']=pub['publication_merkle_root']==s['publication_merkle_root'];checks['project_mmr']=gr['mmr_root']==s['project_mmr_root'];checks['gr_manifest']=gr['manifest_sha256']==s['project_golden_route_manifest_sha256']
checks['video_sha']=hashlib.sha256((ROOT/'demo.mp4').read_bytes()).hexdigest()==s['video_sha256'];checks['bfl_image_sha']=hashlib.sha256((ROOT/'assets/BFL_FLUX2_KLEIN4B_OUTPUT_V2.png').read_bytes()).hexdigest()==s['media_sha256']['bfl_sealed_image'];checks['cinematic_sha']=hashlib.sha256((ROOT/'assets/vithia-cinematic-bfl.mp4').read_bytes()).hexdigest()==s['media_sha256']['bfl_cinematic']
checks['system_state']=s['system_seal_state']=='PASS';checks['required_bp']=all(s[f'bp{i}_status']=='PASS' for i in range(6)) and s['ebp0_status']=='PASS' and s['ebp1_status']=='PASS';checks['golden_route']=s['golden_route_all_verified'] is True;checks['secret_scan']=s['secret_scan_status']=='PASS';checks['sealed_commit_in_history']=subprocess.run(['git','cat-file','-e',s['sealed_content_commit_sha']+'^{commit}']).returncode==0
ok=all(checks.values())
for k,v in checks.items():print(k,':','PASS' if v else 'FAIL')
print('FINAL_SEAL_OBJECT:',s['seal_object_id']);print('FINAL_SEAL_SHA256:',s['seal_sha256']);print('OVERALL:','PASS' if ok else 'FAIL')
raise SystemExit(0 if ok else 1)
