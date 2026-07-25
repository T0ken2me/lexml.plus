<!-- SPDX-License-Identifier: CC-BY-4.0 — LexML v2 — E. Sotiri / Jurisconsul — lexml.eu -->
# LexML end-to-end dry run — report (24 July 2026)

Corpus: 6 real documents — two versions of a 2011 NDA (archive), the 2013
share transfer agreement, the two 2011 litigation conclusions, the 2013
resignation letter. Full pipeline exercised: normalise → segment → classify
(heuristic, tier C — pipeline test, not production classification) → hash →
Merkle → tag under grammar v0.3 → validate → index → live queries.
Total runtime: 118 ms for the whole corpus.

## Results

| Check | Result |
|---|---|
| Tags generated (6 D: + 91 C:) | 97 |
| Validator: generated tags valid | 97/97 after one grammar fix |
| Validator: golden broken set caught | 6/6 (old family, odd-width class, dangling docref, hex provision, double secondary, old date format) |
| Docref collisions across corpus | 0 |
| Tamper test (silent one-phrase edit) | detected via hash mismatch |
| Retrieval: four query types | 0.2 ms total |
| Single-act instrument (letter) | doc tag only, zero clause tags — Rule S4 doctrine working |

## Bug found and fixed (the dry run's purpose)

The grammar capped the matter slug at 12 characters; the first real matter
slug was 14. The validator correctly rejected the two affected document
tags — generator and validator disagreed exactly as designed, and the
grammar is amended: `matter = 1*16( ALPHA / DIGIT / "-" )`. Recorded as the
v0.3 → v0.3.1 delta.

## Two findings beyond the checklist

**1. Cross-version deduplication appeared unprompted.** The severability
clause of the draft NDA and of the signed NDA produced the identical clause
hash (`1391882222`) — the clause survived redrafting verbatim, and
content-addressing collapsed it across two documents automatically. This is
the precedent-genealogy property working at the tag level: identical
boilerplate across the archive will converge to shared hashes at scale,
making "where else does exactly this clause sit" a hash lookup.

**2. The provision index answered a litigation query correctly.** The
authority extractor produced `NCPC026400` from both conclusions (article
264 NCPC, the nullité de forme provision) plus `NCPC015400`, `CC138200`,
`LCA002600` and two date-based case-law tokens (`CAL19300325`,
`TAL19571113` for the 1930 and 1957 authorities). The query "every moyen
citing NCPC" returned the correct units from both pleadings via the
provision-sorted index — the LIT module's authority-first inversion,
demonstrated on real pleadings.

## Lineage (SimHash, draft vs signed NDA)

Of the signed version's 9 units against the draft: 1 identical, 4 lightly
edited, 3 substantively rewritten, 1 new — consistent with the known
drafting history (a fourth party added, the termination mechanics
reworked). The heuristic classifier also assigned identical class
sequences to both versions, an encouraging stability signal even at tier C.

## Honest limitations

Segmentation is regex-based and coarse (the SPA yielded 60 units at
sub-article granularity, the pleadings 6–7 moyen-level units); production
segmentation follows the coding rules per family. Classification here is
keyword-heuristic at tier C by design — the calibrated ensemble replaces
it in production; nothing in this run measures classification accuracy.

## Freeze recommendation

Every component of the spec has now executed against real documents:
grammar (one amendment), hashes and decimal rendering, Merkle roots,
docref referencing, the validator with a complete golden set, the three
index structures plus the provision index, and retrieval semantics for
both contract and litigation families. Recommendation: freeze grammar
v0.3.1 and begin live tagging of the NDA and SPA corpora, with the
ensemble classifier and confidence tiers as specified. The dry-run
pipeline (/home/claude/e2e, session-bound) is the seed of the production
tagger; its port to the production environment is the first implementation
task after freeze.

Companion file: 2026-07-24_LexML_DryRun_Tags_v01.txt — all 97 tags as
generated.
