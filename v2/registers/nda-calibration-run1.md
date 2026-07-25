<!-- SPDX-License-Identifier: CC-BY-4.0 — LexML v2 — E. Sotiri / Jurisconsul — lexml.eu -->
# LexML clause taxonomy — calibration run 1 (NDA family)

Date: 22 July 2026. Sample: 130 clause units from 8 distinct NDAs in the firm
archive, stratified by drafting origin (house line and counterparty paper,
including one UK-firm draft), language (EN/FR, one bilingual template) and age
(2007–2024). Coding per taxonomy v0.1 rules. Two classification passes:
definition-driven (document order) and discriminator-driven (reverse order).

Method caveat, stated plainly: both passes were produced by the same model under
two structurally different framings, not by two independent models as the
protocol specifies. Same-model passes correlate errors, so every agreement
figure below is an upper bound. The run is valid for what it was designed to
find — taxonomy defects, coverage gaps and unstable nodes — but the agreement
percentages must be re-measured with a second model before v1.0.

## Results against thresholds

| Level | Agreement | Threshold | Status |
|---|---|---|---|
| Level 1 (family) | 96.9% (126/130) | 90% | pass |
| Level 2 (within family) | 95.2% (120/126) | 85% | pass |
| Level 3 (within node) | 92.9% (52/56) | 80% | pass overall |
| CNF.2 sublevel only | 78.9% (15/19) | 80% | **fail** |
| Exact leaf, whole sample | 89.2% (116/130) | — | reference |
| Residual/UNC involvement | 9.2% (12/130) | flag >5% | **coverage gap** |

## Findings

1. **The hierarchy holds at levels 1 and 2.** Divergences crossing families were
   4/130, all involving residual codes or genuine composites, none involving two
   substantive leaves being confused with each other.

2. **CNF.2 fails its threshold, exactly as predicted.** The four divergences
   (D8, E3, F3, H6) are all composite obligation clauses mixing non-disclosure,
   non-use, care and permitted-recipient limbs in one paragraph. The taxonomy is
   not wrong; the coding rule is incomplete. Fix for v0.2: a dominant-function
   tiebreak — where a single clause imposes several CNF.2 limbs, the primary code
   is the limb the clause would be cited for in a breach claim, with CNF.2.0
   "composite obligations clause" available as an honest fallback. Merging the
   four leaves would lose retrieval precision the rest of the data shows is
   achievable.

3. **The remedies cluster is the single worst node.** LIA.4 vs LIA.5 divergence
   recurred on every 2007–2008-line clause (A5, B12, C5, C15, D12): the house
   template of that era drafted indemnity and liquidated damages in one breath.
   Fix: coding rule stating that a clause containing both takes LIA.4 as primary
   when a pre-agreed sum is stipulated, LIA.5 otherwise.

4. **Coverage gaps, confirmed by 9.2% residuals.** Recurrent orphans requiring
   new leaves in v0.2: interpretation/definitions machinery (D1, G1);
   representations of capacity and authority (D2); no-warranty / AS-IS
   disclaimers (F8, G13); no-obligation-to-proceed (F12, G14); privilege
   preservation (F11); costs and prevailing-party fees (F17); purpose/objet
   clauses (H1). Seven new leaves, mostly under GEN.

5. **Template lineage is visible in the raw corpus.** The 2008 house template is
   a near-verbatim descendant of the 2007 mutual NDA with jurisdiction and law
   switched from France to Luxembourg — precisely the edit pattern the SimHash
   layer detects mechanically. The lexical fingerprint will reconstruct the
   precedent genealogy of the archive as a by-product.

6. **Bilingual behaviour is clean.** The EN and FR halves of the bilingual
   template classified identically limb for limb, supporting the
   language-neutral coding rule.

## Next actions

1. Taxonomy v0.2: seven new leaves, CNF.2 dominant-function rule, LIA.4/5
   tiebreak, DSP.5 unused so far (interim-relief language appeared only embedded
   in jurisdiction clauses — keep, monitor).
2. Re-run this same 130-clause sample with a genuinely independent second model
   to obtain a defensible agreement figure (the CSV is structured for this).
3. Extend the sample toward 150+ with 2015–2022 house paper, which is
   under-represented relative to the 2007–2013 cluster.

Companion file: 2026-07-22_LexML_CalibrationSample_v01.csv (130 rows, both
passes, per-clause agreement).
