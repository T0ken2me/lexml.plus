# Seed clause taxonomy — NDA family (v0.3)

Status: CALIBRATED. Leaf set unchanged from v0.2 (56 leaves + residuals). This
version adds three coding rules derived from the independent-model run of
24 July 2026 (Sonnet vs reference, 130 clauses: L1 98.5%, L2 93.0%, exact
90.8%, all thresholds passed). The rules resolve the three systematic
divergence patterns; applied post hoc they resolve 10 of the 12 divergences
(the remaining 2, C20 and G4, were classifier-side). In-sample resolution is
by construction; the rules bind prospectively and are re-verified on the next
sample extension.

## New coding rules

- **Rule 9 — term prevails over survival.** A clause that establishes the
  duration or commencement of the agreement takes TRM.1 as primary even where
  it also provides for the survival of confidentiality or other obligations;
  the survival limb takes the secondary code (TRM.2, or CNF.4 where the limb
  fixes a distinct confidentiality duration). TRM.2 as primary is reserved for
  standalone survival clauses that do not themselves establish the agreement's
  term. (Resolves A7, C7, C17, D13, H12.)

- **Rule 10 — law before forum.** A composite clause designating both the
  governing law and the competent forum takes DSP.4.1 as primary and the forum
  leaf (DSP.3.1 or DSP.3.2) as secondary, irrespective of drafting order. The
  convention reflects that the choice of law is logically anterior to the
  choice of forum; its purpose is uniformity, not doctrine. (Resolves D16,
  E8, H13.)

- **Rule 11 — limb inventory for Rule 6.** The "distinct limbs" of a CNF.2
  clause are counted against a closed inventory of four types: (i) disclosure
  control (CNF.2.1); (ii) use control, including reproduction and copying
  (CNF.2.2); (iii) care and protection measures (CNF.2.3); (iv) recipient
  management, flow-down and liability for recipients (CNF.2.4). Three or more
  types present: CNF.2.0. Two types: the limb the clause would be pleaded
  under in a breach claim takes primary, the other secondary. Types are
  counted, not sentences or verbs: "divulguer, copier, distribuer ou
  utiliser" is two types (disclosure; use), not four. (Resolves H5.)

- **Scope note, CNF.1.1 (supplements v0.2).** Where a clause combines a
  definitional limb (what counts as confidential, marking-irrelevance) with a
  no-obligation limb (no duty to disclose or transact, GEN.12), the
  definitional limb prevails as primary and GEN.12 takes secondary.
  (Resolves B2.)

## Rule register (cumulative)

Rules 1–5: unit, function-over-heading, hierarchical fallback, residuals,
language-neutrality (v0.1). Rules 6–8 and scope notes: composites, remedies
tiebreak, operative-over-declaratory (v0.2). Rules 9–11 and the CNF.1.1
supplement: this version.

## Measured accuracy register

| Run | Date | Design | L1 | L2 | Exact |
|---|---|---|---|---|---|
| 1 | 2026-07-22 | same-model, two framings (upper bound) | 96.9% | 95.2% | 89.2% |
| 2 | 2026-07-22 | v0.2 in-sample re-run (by construction) | 100% | 100% | 100% |
| 3 | 2026-07-24 | independent model (Sonnet), v0.2 | 98.5% | 93.0% | 90.8% |

Projected v0.3 ceiling on the run-3 sample: ~98.5% exact (10/12 divergences
resolved by rule; 2 classifier-side).
