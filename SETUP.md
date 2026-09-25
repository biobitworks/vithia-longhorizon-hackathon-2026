# Setup and verification

Hosted demo: https://vithia-longhorizon-hackathon.vercel.app/

Demo video: https://vithia-longhorizon-hackathon.vercel.app/demo.mp4

Prerequisite: Python 3.

```bash
git clone https://github.com/biobitworks/vithia-longhorizon-hackathon-2026.git
cd vithia-longhorizon-hackathon-2026
python3 scripts/verify_golden_route.py
python3 scripts/verify_public_repo.py
```

`verify_golden_route.py` recomputes every exported breakpoint Merkle root, replays the cumulative MMR, checks the V3 manifest identity, and verifies the admitted BFL image hash.

`verify_public_repo.py` verifies the separate publication-bundle Merkle seal over the declared public payload files.

No provider credentials are required for verification. Live sponsor calls require provider credentials supplied via environment variables; credentials and raw private API responses are intentionally not distributed.

## Final successor verification

After cloning, also run python3 scripts/verify_runtime_evidence.py, python3 scripts/secret_scan.py, and python3 scripts/verify_final_seal.py.

verify_runtime_evidence.py independently recomputes the exported BP0–BP5 and EVBP0–EVBP5 chains. secret_scan.py checks the public payload for high-confidence credential patterns. verify_final_seal.py verifies the post-publication seal carrier after it is present.
