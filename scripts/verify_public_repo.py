#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from vithia.canonical import canonical_sha256
from vithia.fco import make_fco, validate_fco
from vithia.integrity import merkle_root_for_fcos

manifest=json.loads((ROOT/"PUBLIC_MANIFEST.json").read_text())
objects_dir=ROOT/"publication/objects"
fcos=[]; ok=True
for entry in manifest["files"]:
    p=ROOT/entry["path"]; b=p.read_bytes(); h=hashlib.sha256(b).hexdigest()
    file_ok=(len(b)==entry["bytes"] and h==entry["sha256"]); ok &= file_ok
    f=make_fco("PublicFileFCO",{"path":entry["path"],"bytes":len(b),"sha256":h})
    stored=json.loads((objects_dir/(f["object_id"].split(":",1)[1]+".json")).read_text())
    fco_ok=(stored==f and validate_fco(stored)); ok &= fco_ok; fcos.append(stored)
bundle=json.loads((ROOT/manifest["bundle_fco_path"]).read_text()); ok &= validate_fco(bundle); fcos.append(bundle)
root,_=merkle_root_for_fcos(fcos)
bp=json.loads((ROOT/"publication/PUB0_PUBLIC_REPO_PREP.json").read_text())
root_ok=(root==bp["breakpoint"]["payload"]["merkle_root_sha256"])
manifest_hash=canonical_sha256({k:v for k,v in manifest.items() if k!="manifest_sha256"})
manifest_ok=(manifest_hash==manifest["manifest_sha256"])
print("FILES:",len(manifest["files"]))
print("MANIFEST_SHA256:",manifest["manifest_sha256"],"MATCH",manifest_ok)
print("PUBLICATION_MERKLE:",root,"MATCH",root_ok)
print("OVERALL:","PASS" if ok and root_ok and manifest_ok else "FAIL")
raise SystemExit(0 if ok and root_ok and manifest_ok else 1)
