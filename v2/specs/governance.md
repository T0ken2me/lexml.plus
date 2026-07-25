# LexML taxonomy governance — extension and maintenance rulebook (v1.0)

Purpose: the standing mechanism by which the clause taxonomy extends to new
document families and repairs itself, without manual curation and without
degrading into an uncontrolled vocabulary. This document governs every family
after the NDA pilot.

## 1. Two-layer structure

The taxonomy is modular. The **cross-cutting core** (GEN, DSP, LIA, TRM, DPR
and the general CNF machinery) applies to every contract type and is
calibrated once; a governing-law clause carries DSP.4.1 whatever the document
family. **Family modules** (the NDA-specific leaves today; SPA, loan,
services, MiCAR/CASP documentation modules to follow) add only the leaves the
family genuinely needs. A new family therefore starts with roughly two thirds
of its taxonomy pre-calibrated, and the marginal cost of each family falls as
the core hardens.

## 2. Append-only versioning

The taxonomy is a Git-versioned artifact. Every leaf carries the version that
introduced it. Leaves are never deleted: a deprecated leaf is marked and
mapped to its successor, so every tag ever written remains resolvable against
the taxonomy state that produced it. Prefix codes make extension structurally
safe — new leaves cannot invalidate existing tags.

## 3. Gap detection (automatic)

Three sensors run over the tagged corpus; none requires scheduled review:

- **Residual rate.** A family whose `.X` + `UNC` involvement exceeds 5%
  of tagged clauses has missing leaves. This is the trigger, measured
  continuously, per family and per document type.
- **Orphan clustering.** Residual clauses are clustered by their binary
  semantic codes; a cluster of residuals within a tight Hamming radius is a
  candidate leaf, delivered with its example set attached.
- **Divergence queue.** Where ensemble classifiers disagree systematically on
  a boundary, the pattern proposes a tiebreak rule (as Rules 9–11 were
  produced by the run of 24 July 2026).

## 4. Admission gate (non-negotiable)

No leaf or rule enters production without passing the calibration gate: two
structurally different models classify a stratified sample containing the
candidate, independently, and agreement must meet the thresholds — 90% at
level 1, 85% at level 2, 80% at level 3. A candidate that fails is merged
upward or its discriminator redrafted; it is not admitted "provisionally".
The gate is the single control that separates this system from a folksonomy.

## 5. Human approval point

Judgement enters at exactly one step: approving a proposed leaf's definition
and discriminator before the gate runs. Routine classification, gap
detection, clustering and re-tagging involve no human review; validation at
point of use (a fee earner using or correcting a retrieved clause) feeds the
confidence tiers as a by-product of billable work.

## 6. Repair loop

tag → monitor residual and divergence rates → cluster orphans → draft leaf or
rule → approve → calibration gate → append to taxonomy (new version) →
re-tag affected clauses only (located by prefix or residual code; cost scales
with the change, not the corpus).

## 7. Accuracy register

Every calibration run is recorded with date, design, sample and per-level
figures (see the register in the current taxonomy version). The register is
the firm's evidence of measured error rate should the system's output ever
need to be defended professionally.

## 8. Extension order

Families are added by archive volume, since the gap sensors only operate on
tagged corpora. Indicative order after NDAs: services and engagement
agreements; corporate suite; MiCAR/CASP documentation as the first
specialised branch. Each extension begins with the family-module draft, a
stratified sample of 100–150 clauses from the archive, and the gate.
