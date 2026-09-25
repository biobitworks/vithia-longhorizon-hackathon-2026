# Hackathon submission details

## One-line summary

**Verifiable long-horizon agents.** Vithia turns long-running agent work into independently addressable evidence, bounded context, cryptographic breakpoints, and restartable successor state.

## Project details

Vithia is a verifiable runtime for long-horizon agents. Instead of treating a long conversation or task history as one opaque context window, Vithia turns work into independently addressable evidence objects (FCOs) connected in a temporal evidence graph (FCG). Each cycle records source evidence, graph state, policy/field metadata, candidate Golden and Dark paths, the exact bounded context shown to the model, and successor state.

Canonical object hashes are committed through Merkle state breakpoints and a cumulative MMR so later execution can reconstruct what existed and what the model actually saw. A cold-restart demo kills the agent process and reconstructs bounded context and custody state from persisted state rather than replaying the original conversation.

Sponsor lanes bind external actions to the same evidence lineage: Liquid AI for bounded/runtime inference tests, Nimble for live external retrieval, RawTree for persistent telemetry, and Black Forest Labs for generated media evidence. Failed and partial attempts remain in the lineage.

## Technical architecture

Source → AtomFCO → FCG_t → Anticube/ΔG* metadata → PathSet → Golden/Dark paths → ContextProjectionFCO → model/action output → ObservationFCO → FCG_(t+1) → BreakpointFCO → cumulative MMR

BP4 freezes the exact context bytes presented to the model. Breakpoint receipts declare ordered object identities and recomputable Merkle roots. The MMR records append-only breakpoint succession. These integrity structures establish identity/inclusion only.

## Lessons learned

Long-horizon reliability improves when evidence, scoring, selection, context, action, and observation are separate addressable objects rather than one opaque trace. Persisting failures was useful: failed RawTree and Nimble attempts remain predecessors to successful successors. A fresh Liquid 2.6B classifier validation also failed to reproduce an earlier pass, so the negative successor is retained. Cryptographic custody makes restart and state comparison precise, but it does not establish truth or causality.

## Persistent links

https://tokensand.com/p/vithia-verifiable-long-horizon-agents?mode=developer
https://vithia-longhorizon-hackathon.vercel.app/
https://vithia-longhorizon-hackathon.vercel.app/demo.mp4
https://github.com/biobitworks/vithia-longhorizon-agents-hackathon-2026
https://huggingface.co/biobitworks/fco-vithia-fmo-076
https://doi.org/10.5281/zenodo.21829929
