#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from vithia.integrity import verify_breakpoint, MMRAccumulator
from vithia.fco import validate_fco

def verify_series(label,bpdir,objdir,pattern):
    rows=[]
    for p in (ROOT/bpdir).glob(pattern):
        try:j=json.loads(p.read_text())
        except Exception:continue
        seq=j.get("breakpoint",{}).get("payload",{}).get("sequence")
        if isinstance(seq,int):rows.append((seq,p,j))
    rows.sort(key=lambda x:x[0]); mmr=MMRAccumulator(); prev=None; ok=True
    for seq,p,j in rows:
        bp=j["breakpoint"]; q=bp["payload"]; objs=[]; missing=[]
        for oid in q["state_object_ids"]:
            op=ROOT/objdir/(oid.split(":",1)[1]+".json")
            if not op.exists():missing.append(str(op));continue
            objs.append(json.loads(op.read_text()))
        v=verify_breakpoint(bp,objs)
        mmr.append(seq,bp["object_id"].split(":",1)[1],q["state_version_id"])
        checks={
          "objects":not missing and all(validate_fco(x) for x in objs),
          "merkle":v["passed"],
          "mmr":mmr.root()==j["mmr"]["root_sha256"],
          "predecessor":q.get("predecessor_breakpoint_id")==prev,
          "claim_boundary":bool(q.get("claim_boundary")),
        }
        passed=all(checks.values());ok &= passed
        print(f"{label} {p.name}: {'PASS' if passed else 'FAIL'} merkle={v['recomputed_merkle_root_sha256']} mmr={mmr.root()}")
        prev=bp["object_id"]
    return ok,len(rows)

r,nr=verify_series("RUNTIME","evidence/runtime/breakpoints","evidence/runtime/objects","BP*.json")
e,ne=verify_series("EVALUATION","evidence/evaluation/breakpoints","evidence/evaluation/objects","EVBP[0-9]*.json")
ok=r and e and nr==6 and ne>=6
print("RUNTIME_COUNT:",nr);print("EVALUATION_COUNT:",ne);print("OVERALL:","PASS" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
