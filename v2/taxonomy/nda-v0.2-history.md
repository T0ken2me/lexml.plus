# Seed clause taxonomy — NDA family (v0.2)

Status: DRAFT — post-calibration-run-1. Changes from v0.1 are driven entirely by
the 14 observed divergences and the 9.2% residual rate. Unchanged nodes are not
restated; v0.1 remains the base document.

## New leaves

**GEN — general provisions**
- **GEN.9 — definitions and interpretation machinery.** Defined-terms tables,
  construction rules (headings, singular/plural, gender), party-group
  definitions. Previously orphaned (D1, G1).
- **GEN.10 — representations of capacity and authority.** Due incorporation,
  power to execute, no conflict with law or constitutional documents (D2).
- **GEN.11 — no warranty.** CI provided "as is"; no representation as to
  accuracy, completeness or non-infringement (F8, G13).
- **GEN.12 — no obligation to proceed.** No duty to disclose, transact or enter
  further agreements; disclosure is not an offer (F12, G14, and the second limb
  of B2).
- **GEN.13 — privilege preservation.** Common-interest and no-waiver language
  for material subject to professional privilege (F11).
- **GEN.14 — purpose / objet clause.** Article stating the object of the
  agreement itself (H1).

**LIA — liability and remedies**
- **LIA.6 — costs and fees recovery.** Prevailing-party attorney and expert
  fees, procedural costs (F17).

## New coding rules

- **Rule 6 — composite obligations (resolves the CNF.2 threshold failure).**
  A single clause imposing three or more distinct CNF.2 limbs (non-disclosure,
  non-use, care, permitted recipients) takes **CNF.2.0 — composite obligations
  clause**, a new honest fallback leaf. A clause imposing one or two limbs takes
  the limb it would be pleaded under in a breach claim, the second limb as
  secondary code.
- **Rule 7 — remedies tiebreak.** A clause containing both indemnity language
  and a pre-agreed sum takes LIA.4 as primary (the stipulated sum is the
  operative innovation); LIA.5 applies only where recovery is purely loss-based.
- **Rule 8 — operative over declaratory.** Where a clause combines a declaratory
  limb (ownership is retained) with an operative one (return or destroy), the
  operative limb gives the primary code (resolves B7-type composites).
- **Scope note, CNF.2.2.** Reproduction and copying restrictions are non-use
  restrictions (resolves D8).
- **Scope note, CNF.2.3.** Covers protection-measure obligations whether or not
  a care benchmark (own-information / reasonable care) is stated (resolves H6).
- **Scope note, CNF.1.1.** Marking-irrelevance stipulations ("confidential
  whether or not marked") are definitional and take CNF.1.1 (resolves B2).

## Node count

48 → 56 leaves (+ CNF.2.0 fallback + 7 new; residual codes unchanged).
DSP.5 (interim relief carve-out) recorded zero primary assignments in run 1 —
retained on watch; interim-relief language so far appears only embedded in
jurisdiction clauses.
