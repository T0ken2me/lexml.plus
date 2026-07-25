# LexML — machine-optimised legal clause coordinates

Compact "legal coordinates" per clause so LLMs retrieve Jurisconsul's
document archive without reading whole documents. Grammar v0.3.1 FROZEN
2026-07-24 (specs/grammar-v0.3.1-FROZEN.md). Two families calibrated
(NDA, SPA), both admitted through the two-model gate; grammar, hashing,
Merkle, validator and indexes proven in two end-to-end dry runs on 13
real documents (321 tags, 0 collisions, all valid).

## Layout
- specs/        grammar (frozen + history), governance rulebook, tokeniser
                test, re-mint + provision dictionary, LIT module spec
- taxonomy/     NDA v0.3 (calibrated), SPA v0.2 (admitted), history
- dictionaries/ families.json, statutes.json (machine-readable, versioned)
- registers/    accuracy runs, dry-run reports, stress test
- data/         calibration samples, dry-run tag outputs, workbook
- src/          validator.py (frozen reference), dry-run pipelines,
                tokeniser harness (toktest/)
- artifacts/    two-model gate UIs (React; call claude-sonnet-4-6)

## Ground rules (from the governance spec)
Append-only taxonomy under Git; no leaf without the 90/85/80 two-model
gate; residual >5 percent triggers module work; humans approve leaf
definitions only; every calibration run lands in registers/.

## State at freeze
Calibrated: NDA (98.5/93.0/90.8), SPA (100/97.8/94.6). Queued through the
loop: SVC module (~50 percent residual measured), MEM module spec (third
unit model), DOM micro-module, LIT gate, DPR token screen, NDA 2015-2022
out-of-sample, SPA sample top-up. See HANDOFF.md for the build plan.
