<!-- SPDX-License-Identifier: CC-BY-4.0 — LexML v2 — E. Sotiri / Jurisconsul — lexml.eu -->
# Litigation module — unit model and coordinates (spec v0.1)

Scope: pleadings and judicial acts for Luxembourg courts (assignations,
conclusions, mémoires, requêtes). Contract-clause taxonomy does not apply;
this module defines its own unit type. Family code: LIT.

## Unit model

The unit is the **moyen**: one argued ground, typically one numbered section
or sub-section of the pleading. Front matter (parties, rôle, chamber,
comparution) and the dispositif are document-level metadata, not units.
A moyen re-argued across successive versions of the same pleading keeps its
identity through the lexical fingerprint (SimHash lineage, validated on real
drafts at 16/64 document-level distance with paragraph genealogy).

## Classification axes

Unlike contract clauses, a moyen carries three orthogonal coordinates:

1. **Nature** (the taxonomy axis):
   - LIT.P — procedural: LIT.P.1 nullité d'acte; LIT.P.2 libellé obscur;
     LIT.P.3 irrecevabilité; LIT.P.4 prescription; LIT.P.5 compétence;
     LIT.P.6 communication de pièces; LIT.P.X residual
   - LIT.F — fond: LIT.F.1 responsabilité contractuelle; LIT.F.2
     responsabilité délictuelle/quasi-délictuelle; LIT.F.3 garanties et
     assurances; LIT.F.4 préjudice et quantum; LIT.F.5 exécution/résolution;
     LIT.F.X residual
   (Draft depth; the admission gate sets the final granularity.)
2. **Posture**: P (principal), S (subsidiaire), T (plus subsidiaire) —
   one character, positional.
3. **Authorities**: the cited provisions and case law in compressed
   ELI/ECLI-style tokens (e.g. 264NCPC, 154NCPC, 26L1997ASS, 1382CC,
   case-law tokens by court and date). This field is the PRIMARY retrieval
   key for the family.

## Field weighting — the inversion

For contracts, retrieval filters on clause class first, provisions second.
For litigation the weighting inverts: the dominant queries are
authority-first ("every moyen that argued article 26 of the 1997 insurance
law", "our pleadings citing this Cour de cassation line"), then filtered by
nature and outcome. The tag grammar is unchanged — the same provisions field
exists in every clause tag — only the index ordering differs: the litigation
index is sorted by provision token, the contract index by class prefix.

## Additional document-level fields (LIT documents)

Rôle number, chamber, procedural stage (assignation, conclusions n,
réplique), party posture (demandeur/défendeur), and outcome link once a
decision exists. Outcome linkage turns the archive into measurable advocacy
history: which moyens, argued on which authorities, succeeded before which
chambers.

## Gate

Calibration mirrors the contract protocol: 100+ moyens sampled from the
litigation archive, two independent classifiers, thresholds 90/85 (two
levels only). To be scheduled after the SPA gate closes.
