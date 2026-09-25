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