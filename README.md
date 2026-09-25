# Vithia — Verifiable Long-Horizon Agents

Vithia is a hackathon MVP for long-running agents whose persistent evidence, active context, decisions, failures, and restart state remain independently inspectable.

Long Horizon Agents Hack 2026

- Tokens& project: https://tokensand.com/p/vithia-verifiable-long-horizon-agents?mode=developer
- Working demo: https://vithia-longhorizon-hackathon.vercel.app/
- Demo video: https://vithia-longhorizon-hackathon.vercel.app/demo.mp4
- Public repository: https://github.com/biobitworks/vithia-longhorizon-hackathon-2026

## What was built

The runtime separates a growing evidence graph from the bounded context actually shown to the model:

source → FCO atoms → FCG → Anticube/ΔG* metadata → Golden/Dark paths → exact ContextProjectionFCO → output/observation → successor FCG → Merkle/MMR breakpoint

The exported Golden Route contains **15 independently recomputable breakpoints (GR0–GR14)**. Latest cumulative MMR: `3a86b49ea3a148ed9abd66009179f17ad4d63457e4dca74463e82ebe2ae05287`.

Manifest identity: `ce71b6cfbc903f49e397109b04f3381aa523a1e717682d2ef9894056aef9420a`.

Hashes and Merkle/MMR inclusion establish exact-byte identity/inclusion, not truth, causality, scientific validity, or model quality.

## Fresh publication validation

Nimble live search: PASS (3 results / 3 URLs). RawTree telemetry: PASS (200/200 + exact readback). Liquid AI 1.2B tool-selection health: PASS. Liquid AI 2.6B bounded classifier: PARTIAL, 0/6 on the fresh validation run. BFL prior image/video evidence remains sealed; finetuning remains BLOCKED_NO_CHECKPOINT. Direct Tinybird ingest remains NOT_TESTED/PARTIAL.

## Verify

`python3 scripts/verify_golden_route.py`
`python3 scripts/verify_public_repo.py`

See SETUP.md, SUBMISSION.md, SPONSOR_STATUS.md, and docs/BREAKPOINT_PROTOCOL.md.