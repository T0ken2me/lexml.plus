<!-- SPDX-License-Identifier: CC-BY-4.0 — LexML v2 — E. Sotiri / Jurisconsul — lexml.eu -->
# LexML dry run 2 — seven new documents (24 July 2026)

Corpus: a ManCo establishment memorandum (EN, 2014), two versions of the
same IT service agreement (EN, 2015 draft and 2016 signed), a labour-law
memo (FR), a domiciliation agreement template (FR, 2012), a trademark
filing memorandum (FR, 2017) and a patent fee-quote memorandum (EN, 2014).
Three genres the pipeline had never seen. 217 clause units + 7 document
tags; validator 224/224; combined 13-document corpus: 0 docref collisions;
runtime 350 ms.

## The recheck earned its keep: segmentation was the failure

The first pass produced 0 units for both service agreements and 1 for the
domiciliation template — the run-1 regex segmenters silently failed on the
new layouts, while the validator "passed" the near-empty output. Lesson
recorded as a production requirement: **segmentation must be layout-aware
per source format** (docx heading styles, article numbering conventions),
and a minimum-yield sanity check (units per 10k characters) belongs in the
pipeline so an empty segmentation fails loudly instead of passing quietly.
After per-layout segmenters: 21/61/76/26/24/5/4 units.

## Residual rates confirm the module map

| Doc | Genre | Residual rate |
|---|---|---|
| Service agreements (V1, V2) | contract | 49% / 50% |
| Domiciliation template | contract | 92% |
| Four memoranda | advisory | 100% each |

Exactly the pattern the two-layer model predicts. In the service
agreements, the cross-cutting spine classified cleanly in English
(definitions, R&W, limitation of liability, term, termination,
confidentiality, data protection, governing law, notices); everything
residual is the SVC module in waiting — service levels, fees, duties,
regulatory change, beneficiaries, force majeure, audit — matching the
roadmap's "services next by archive volume". The domiciliation template is
a small dedicated module (DOM). The memoranda are the significant finding:
100% residual across all four confirms that **advisory documents are a
genre, not a clause family** — like litigation, they need their own unit
model (a MEM module: question presented, analysis, recommendation,
fee/scope sections), which is now the third unit model alongside contracts
and pleadings.

## The authority axis carries the memos

Despite classifying at 100% residual, the labour-law memo became fully
retrievable through its provisions: the extractor produced seven Code du
travail tokens (CDT012401–CDT012412, the L.124-x dismissal articles), the
ManCo memo yielded the chapter-15 token (OPC001500) and the domiciliation
template the 1999 law (LDOM). The LIT insight generalises: for advisory
genres, retrieval runs authority-first, and the provision index makes an
unclassified memo findable by what it analyses. "Which memos discuss
L.124 dismissal notice" is already answerable on this corpus.

## Cross-version deduplication at scale

Between the 2015 draft and the 2016 signed service agreement: 9 clause
units share identical content hashes (passed through untouched), 29 sit
in the lightly-edited SimHash band, 38 substantively rewritten. The
genealogy of a heavily negotiated commercial contract, reconstructed
mechanically — consistent with run 1's finding on the NDA pair, now
demonstrated on a 60-76-unit instrument.

## Actions arising

1. MEM module spec (third unit model, authority-first, section taxonomy) —
   small, mirrors the LIT spec.
2. SVC module draft from the 49% residual clusters — next gate candidate,
   confirming the roadmap order.
3. DOM micro-module (the template is house paper; one gate sample from the
   domiciliation archive).
4. Production segmentation: layout-aware per format + minimum-yield check
   (grammar and validator untouched — no spec bugs this run).
5. Grammar note: vintage sentinel 0000 used for the undated labour memo;
   convention to be recorded in v0.3.1 (unknown vintage = 0000, flagged
   for enrichment).

Companion file: 2026-07-24_LexML_DryRun2_Tags_v01.txt (224 tags).
