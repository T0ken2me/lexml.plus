<!-- SPDX-License-Identifier: CC-BY-4.0 — LexML v2 — E. Sotiri / Jurisconsul — lexml.eu -->
# LexML extension stress test — four documents outside the NDA family

Date: 24 July 2026. Sample: one share transfer agreement (2013, FR), two
successive versions of litigation conclusions (2011, FR), one corporate
resignation letter (2013, FR). All four from a single client cluster, which
also serves as a cross-document linkage test. Party identifiers omitted here;
the companion CSV holds the unit-level classification of the share transfer
agreement.

## 1. Share transfer agreement — the gap sensor fires exactly as designed

41 clause units classified against taxonomy v0.3 (core + NDA module):

| Measure | Result |
|---|---|
| Units matched to existing leaves | 8/41 (20%) |
| Residual involvement (GEN.X + UNC) | 33/41 (80%) — trigger threshold is 5% |
| Cross-cutting spine (GEN/DSP units) | 8/8 hit an existing leaf (100%) |

The two-layer model behaved precisely as predicted, with one correction to
my earlier estimate. The boilerplate spine transferred perfectly: every
definitions, interpretation, capacity, waiver, entire-agreement, amendment,
governing-law, jurisdiction and execution unit landed on a calibrated leaf
with no ambiguity, across a document family and in French. But the earlier
"60–70% inherited" figure overstates coverage *by unit count* for
R&W-heavy deal documents: the representations catalogue (20 units) and the
warranty mechanics dominate the unit population, and they are 100%
family-specific. The honest formulation: the core covers the *kinds* of
clause it claims, completely; what share of a document that represents
depends on the document's composition.

The residuals cluster by inspection into a coherent SPA module draft:
transfer object; price; payment terms; the R&W catalogue (title to shares,
corporate housekeeping, accounts, tax, employment and social, assets and
encumbrances, litigation, insurance, guarantees given); warranty indemnity
mechanics (scope, de minimis trigger, duration, fiscal carve-out, survival
on restructuring); title and enjoyment transfer; opposability to the
company; security for warranties. Plus two cross-family GEN candidates
promoted by this test: recitals and annexes-integral clauses, which will
recur in every deal document. That module draft goes to the admission gate
per the governance rulebook before any leaf is minted.

## 2. Litigation conclusions — a different unit model, not just new leaves

The pleadings do not decompose into contract clauses at all; forcing them
through the clause taxonomy would be a category error. Their natural units
are *moyens*, and their natural coordinates differ: procedural vs
substantive classification (exception de nullité, libellé obscur; then
responsabilité contractuelle/délictuelle), posture (principal vs
subsidiaire), and above all the cited authorities — NCPC articles, the
insurance-contract statute, case law. For litigation documents the
compressed provision field becomes the primary retrieval key ("every
pleading that argued article 26 of the 1997 insurance law"), which is where
the ELI/ECLI-style encoding earns its place. Conclusion: litigation is a
module with its own unit type and field weighting, to be specified
separately; the tag grammar accommodates it without change since the fields
are the same, only their usage differs.

## 3. Version lineage — measured on real drafting

The two conclusions are successive drafts of the same pleading. The
document-level SimHash distance is 16/64 — far inside the same-lineage band
(random pairs average ~32) — and paragraph-level matching shows the
drafting history: of 62 paragraphs in the later version, 3 carried over
identically, 6 lightly edited, 52 substantively redrafted, 1 new. The
lexical layer reconstructs the genealogy of a pleading through heavy
redrafting, on real firm documents, with no model involved. This is the
strongest single validation so far of keeping the SimHash code alongside
the semantic one.

## 4. Resignation letter — document-level tagging suffices

A single-operative-act instrument (manager resignation with RCS publication
instruction). Clause-level tagging is pointless here; the tag's document-type
field carries the whole classification (corporate act: management
resignation). Finding: the system needs the already-implied document-level
tag as a first-class object, with clause-level tags optional below it —
short corporate acts, letters and notices are tagged once, not per
paragraph.

## 5. The graph emerges

The four documents interlink: the share transfer agreement expressly
defines the pending litigation (the conclusions' case) as a disclosed
item in its R&W; the resignation letter is the seller-manager's exit
executed alongside the transfer; all concern the same company. With
matter, party-role and provision fields in the coordinates plus content
hashes, these links materialise automatically at tagging time — the
archive becomes a navigable graph of the firm's history, not a folder
tree. Retrieval questions like "show the litigation disclosed in that
deal" become coordinate lookups.

## Actions

1. Draft SPA family module from the residual clusters above; run the
   two-model admission gate on a stratified sample from the archive's
   deal documents.
2. Specify the litigation module's unit model (moyen-level, authority-first
   coordinates) as a separate short spec.
3. Promote recitals and annexes-integral to GEN candidates in the same
   gate run.
4. Add the document-level tag as a first-class object in the grammar spec.
