#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
skip={".git","publication","__pycache__",".vercel"}
patterns=[
 ("openai_key",re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
 ("hf_token",re.compile(r"\bhf_[A-Za-z0-9]{20,}")),
 ("aws_access",re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
 ("butterbase_key",re.compile(r"\bbb_sk_[A-Za-z0-9_-]{12,}")),
 ("bearer",re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{24,}",re.I)),
 ("private_key",re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]
hits=[]
for p in ROOT.rglob("*"):
    if not p.is_file() or any(x in skip for x in p.parts):continue
    if p.suffix.lower() in {".png",".jpg",".jpeg",".gif",".webp",".mp4",".mov",".pdf",".pyc"}:continue
    try:
        if p.stat().st_size>5_000_000:continue
        s=p.read_text(errors="ignore")
    except Exception:continue
    for name,rx in patterns:
        for m in rx.finditer(s):
            hits.append((str(p.relative_to(ROOT)),name,m.start()))
for p in ROOT.rglob(".env*"):
    if ".git" not in p.parts and p.is_file(): hits.append((str(p.relative_to(ROOT)),"env_file_present",0))
print("SECRET_SCAN_HITS:",len(hits))
for h in hits[:50]: print("|".join(map(str,h)))
print("OVERALL:","PASS" if not hits else "FAIL")
raise SystemExit(0 if not hits else 1)
