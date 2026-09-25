# Vithia — Verifiable Long-Horizon Agents

> [!IMPORTANT]
> **Post-submission video notice — September 25, 2026.** The Tokens& submission page is now frozen and its **“Demo video”** button still opens the earlier YouTube playlist. The canonical final walkthrough is the sealed **2:56.8 presenter-overlay video** at https://vithia-longhorizon-hackathon.vercel.app/demo.mp4. Its SHA-256 is `f88c29331642a26d8233d865a5ebba52c1c1c6bdaa19ee16455499d75521cecc`, matching the production Vercel bytes and the repository final seal. The historical submission page has not been rewritten after the deadline.

Vithia is a hackathon MVP for agents that need to work across long histories without hiding all prior state inside one giant prompt.

## Read this first

For a person using the demo, the idea is simple: **the conversation stays readable, while the evidence used by the AI stays inspectable**.

The live dashboard separates two views:

- **Human view:** choose a question, read the answer, and see which model actually answered.
- **AI custody view:** inspect the evidence path, exact bounded context, retained alternatives, and cryptographic breakpoints created during the run.

The selector now exposes both **Project evidence** questions and a fixed **20-case LongMemEval-V2 text-only smoke set**. A live LongMemEval-V2 case was executed with LiquidAI/LFM2.5-1.2B and all six BP0–BP5 breakpoints independently recomputed successfully. This live run is an engineering smoke test, **not an official LongMemEval-V2 score and not leaderboard-comparable**.

The full multimodal LongMemEval-V2 Small set is still gated because required question screenshot assets are incomplete. That failure is preserved rather than promoted to PASS.

## Try it

- Tokens& project: https://tokensand.com/p/vithia-verifiable-long-horizon-agents?mode=developer
- Public project page: https://vithia-longhorizon-hackathon.vercel.app/
- Demo video: https://vithia-longhorizon-hackathon.vercel.app/demo.mp4
- Public repository: https://github.com/biobitworks/vithia-longhorizon-hackathon-2026
## What the technical terms mean

- **FCO:** one independently addressable evidence or state object.
- **FCG:** the graph connecting those objects through provenance and time.
- **Golden path:** the context route selected for the current answer.
- **Dark paths:** competing routes retained instead of erased.
- **Breakpoint:** a recomputable commitment to a declared state.
- **MMR:** the cumulative append-only commitment across breakpoints.

The runtime separates a growing evidence graph from the bounded context actually shown to the model:

source → FCO atoms → FCG → Anticube/ΔG* metadata → Golden/Dark paths → exact ContextProjectionFCO → output/observation → successor FCG → Merkle/MMR breakpoint

Anticube/ΔG* fields in this hackathon runtime are simulation/governance metadata unless a receipt explicitly states otherwise.

## Current verified state

The exported Golden Route contains **15 independently recomputable breakpoints (GR0–GR14)**.

- Golden Route cumulative MMR: `3a86b49ea3a148ed9abd66009179f17ad4d63457e4dca74463e82ebe2ae05287`
- Golden Route manifest: `ce71b6cfbc903f49e397109b04f3381aa523a1e717682d2ef9894056aef9420a`
- LongMemEval-V2 dashboard successor receipt: `evidence/dashboard/LME_V2_DASHBOARD_SUCCESSOR.json`
- LME live-case MMR: `68d2b57d0c094a90453d0959e67ff8d511ebfa6a9e7ecc468d2152aa0a21dfb6`
Hashes and Merkle/MMR inclusion establish exact-byte identity and inclusion. They do **not** establish truth, causality, scientific validity, or general model quality.

### Sponsor/runtime status

Nimble live search: **PASS** (3 results / 3 URLs). RawTree telemetry: **PASS** (200/200 + exact readback). Liquid AI 1.2B tool-selection health: **PASS**. Liquid AI 2.6B bounded classifier: **PARTIAL, 0/6** on the fresh validation run. BFL prior image/video evidence remains sealed; finetuning remains **BLOCKED_NO_CHECKPOINT**. Direct Tinybird ingest remains **NOT_TESTED/PARTIAL**.

These labels describe observed execution state; they are not product rankings.

## Machine-readable verification

For exact state rather than presentation copy:

- `evidence/golden_route/` — Golden Route objects and GR0–GR14 receipts
- `evidence/dashboard/LME_V2_DASHBOARD_SUCCESSOR.json` — bounded LME dashboard successor
- `SPONSOR_STATUS.md` — literal sponsor-lane execution states
- `docs/BREAKPOINT_PROTOCOL.md` — breakpoint construction
- `PUBLIC_MANIFEST.json` — sealed public repository payload

Run:

```bash
python3 scripts/verify_golden_route.py
python3 scripts/verify_public_repo.py
```

See `SUBMISSION.md`, `SETUP.md`, and `SECURITY.md` for the remaining public handoff.

## Final evidence successor

The finalization successor keeps **system integrity** separate from **scientific performance inference**. The live BP0–BP5 runtime and EVBP0–EVBP5 evaluation chains independently replay their declared Merkle roots and cumulative MMR state. The 20-case LongMemEval-V2 result remains an engineering smoke: 15 deterministically scored cases, M0 0/15, bounded FCG memory 1/15 (+6.67 percentage points observed), with no generalization or leaderboard claim.

A bounded-context successor reduced average memory-context tokens from 1,618.8 to 945.8 (41.6%) on the same 15 scored cases while the observed correct count remained 1/15. This is an observed compression result, not evidence of broad performance equivalence.

The reader-capacity question is now explicit: **given the same cryptographically frozen evidence projection, how much reader capacity is required to preserve the task outcome?** A single shared-context Liquid 1.2B/2.6B case was executed and diverged; equivalence/noninferiority is therefore not established. Historical OLLARMA, Vithia replay, and ButterBase evidence is exposed separately as structural lineage, not as LongMemEval scores.

The public evidence app exposes five views: Live Agent, Evaluation, Alignment + Security, Evidence + Sponsors, and Final Seal. OpenAI Codex is attributed as orchestration/tooling; Liquid AI is the demonstrated local inference reader.
