# Hackathon submission details

## One-line summary

**Verifiable long-horizon agents.** Vithia keeps long-running evidence separate from the small context used for each answer, records exactly what the model saw, preserves failed and competing paths, and can reconstruct committed state after restart.

## What a person sees

The dashboard is intentionally split into two surfaces.

On the **human side**, you select a question and read the answer in normal language. The selector includes five project-evidence prompts plus a fixed 20-case LongMemEval-V2 text-only smoke set.

On the **AI custody side**, Vithia shows the evidence route used for that answer: source custody, memory/graph construction, retrieval or governance metadata, selected and retained paths, exact model-visible context, model invocation, and successor state.

This is not a hidden chain-of-thought display. It is an auditable record of inputs, selections, outputs, and state transitions.

## LongMemEval-V2 status

The public dataset staging contains 451 questions: 422 text-only and 29 image-bearing questions. Exact source checksums are recorded in `evidence/dashboard/LME_V2_DASHBOARD_SUCCESSOR.json`.

A fixed 20-case text-only smoke subset is available in the dashboard. A live case executed with `LiquidAI/lfm2.5-1.2b-instruct:q4_k_m`; BP0–BP5 independently recomputed PASS.

The live dashboard does **not** compute an official benchmark score. `benchmark_scoring_state=NOT_COMPUTED_LIVE_DASHBOARD` and `leaderboard_comparable=false`.
The official multimodal Small validator remains **FAIL_MISSING_QUESTION_SCREENSHOTS** because required screenshot assets are incomplete. That state is preserved; it is not promoted to PASS.

## How Vithia works

Vithia does not treat a long conversation or task history as one opaque context window. Work is split into independently addressable objects (FCOs) connected by a temporal/provenance graph (FCG).

For each answer, the runtime can preserve:

source → FCO/FCG state → retrieval/governance metadata → candidate paths → selected Golden path + retained Dark paths → exact bounded context → model output → observation → successor state → Merkle/MMR breakpoint

BP4 freezes the exact bytes presented to the model. Breakpoint receipts bind declared object identities to recomputable Merkle roots. The MMR records append-only breakpoint succession.

Those structures establish **identity and inclusion**, not truth, causality, scientific correctness, or model quality.

## Sponsor and runtime lanes

External actions are bound to the same evidence lineage when executed:

- Liquid AI: 1.2B validation **PASS**; fresh 2.6B bounded-classifier validation **PARTIAL_0_OF_6**.
- Nimble: fresh live search **PASS**.
- RawTree: fresh insert/query/readback **PASS**.
- Tinybird direct ingest: **NOT_TESTED/PARTIAL**.
- Black Forest Labs: sealed image/video evidence **PASS**; finetune **BLOCKED_NO_CHECKPOINT**.

Failed and partial attempts remain addressable predecessors rather than being overwritten by later successes.
## Current cryptographic state

Golden Route GR0–GR14 remains the project-level hackathon route:

- cumulative MMR: `3a86b49ea3a148ed9abd66009179f17ad4d63457e4dca74463e82ebe2ae05287`
- manifest: `ce71b6cfbc903f49e397109b04f3381aa523a1e717682d2ef9894056aef9420a`

The LongMemEval-V2 dashboard successor is a separate bounded run:

- live-case MMR: `68d2b57d0c094a90453d0959e67ff8d511ebfa6a9e7ecc468d2152aa0a21dfb6`
- receipt identity: `3260629789a22dfd9697c40acae393475c2996cdb34d7bbe2d994451817957bb`
- independent BP0–BP5 recomputation: **PASS**

The public repository itself is resealed whenever its public bytes change; see `PUBLIC_MANIFEST.json` for the current publication successor.

## Persistent links

- Tokens& project: https://tokensand.com/p/vithia-verifiable-long-horizon-agents?mode=developer
- Public project page: https://vithia-longhorizon-hackathon.vercel.app/
- Demo video: https://vithia-longhorizon-hackathon.vercel.app/demo.mp4
- Public repository: https://github.com/biobitworks/vithia-longhorizon-hackathon-2026
- Vithia model card: https://huggingface.co/biobitworks/fco-vithia-fmo-076
- Published FCO DOI: https://doi.org/10.5281/zenodo.21829929
