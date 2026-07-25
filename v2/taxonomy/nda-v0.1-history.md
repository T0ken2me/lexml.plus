# Seed clause taxonomy — NDA family (v0.1)

Status: DRAFT — pre-calibration. This version exists to be tested, not applied.
Purpose: input to the granularity experiment (two-model independent classification,
agreement measured per level). Nodes failing the agreement threshold are merged or
redefined; nothing here is frozen until the experiment has run.

Scope: non-disclosure agreements, Luxembourg practice, unilateral and mutual.
Prefix property: every child code begins with its parent code, so a subtree query
is a string prefix match (`DSP.` returns all dispute-resolution clauses).

---

## Coding rules

1. Unit of classification: the smallest separately numbered or paragraphed clause.
   Composite clauses (e.g. governing law + jurisdiction in one sentence) take a
   primary code and at most one secondary code, primary being the clause's
   dominant legal function.
2. Classify function, not heading. A clause headed "Confidentiality" that in
   substance caps liability is LIA.1.
3. Hierarchical fallback: assign the deepest node the classifier is confident of;
   a parent code (e.g. `DSP.2`) is a valid answer. Agreement is measured per level,
   so fallback behaviour is itself data.
4. Residuals: `<FAM>.X` = belongs to the family, fits no leaf. `UNC` = fits no
   family. Residual frequency above ~5% in the experiment signals a coverage gap.
5. Language-neutral: the same code applies to the French and English rendering of
   the same clause; language lives in the tag's language field, not the taxonomy.

---

## DSP — dispute resolution

### DSP.1 — amicable resolution and mediation
Discriminator vs DSP.2/DSP.3: the clause organises a *pre-contentious* step; it
does not itself confer decisional power on an arbitrator or court.

- **DSP.1.1 — negotiation / escalation ladder.** Structured management-level
  discussions before any formal process.
- **DSP.1.2 — mediation, voluntary.** Mediation offered or agreed without being a
  condition precedent to proceedings.
- **DSP.1.3 — mediation, mandatory tiered.** Mediation as a condition precedent to
  litigation or arbitration, typically with a time trigger.
  Anchors: arts 1251-1 et seq. NCPC (civil and commercial mediation, introduced by
  the law of 24 February 2012) [VERIFY article range].
Discriminator DSP.1.2 vs DSP.1.3: is commencing proceedings *conditional* on the
mediation step? If yes → 1.3.

### DSP.2 — arbitration
- **DSP.2.1 — institutional arbitration.** Reference to an institution's rules
  (ICC, LCIA, DIS, CAM etc.).
- **DSP.2.2 — ad hoc / UNCITRAL arbitration.** No administering institution.
- **DSP.2.3 — arbitral mechanics.** Seat, language, number of arbitrators,
  finality and waiver of recourse, where drafted as a separate clause.
  Anchors: arts 1224 et seq. NCPC as reformed by the law of 19 April 2023 on
  arbitration.
Discriminator DSP.2.3 vs 2.1/2.2: does the clause *establish* arbitration or only
*configure* an arbitration established elsewhere?

### DSP.3 — court jurisdiction
- **DSP.3.1 — exclusive jurisdiction.**
- **DSP.3.2 — non-exclusive or asymmetric jurisdiction.** Includes one-way
  options benefiting a single party.
Anchors: Regulation (EU) 1215/2012 (Brussels I bis), art. 25.

### DSP.4 — governing law
- **DSP.4.1 — choice of law.** Designation of the applicable substantive law.
- **DSP.4.2 — exclusions.** Renvoi, conflict rules, CISG exclusion where drafted
  separately.
Anchors: Regulation (EC) 593/2008 (Rome I), art. 3.
Discriminator DSP.3 vs DSP.4: forum selection vs law selection; composite clauses
take both codes under coding rule 1.

### DSP.5 — interim relief carve-out
Preservation of the right to seek injunctive or conservatory measures before state
courts notwithstanding DSP.1/DSP.2.

---

## CNF — confidentiality core

### CNF.1 — definition of confidential information
- **CNF.1.1 — broad definition.** All information disclosed, however conveyed,
  with or without a non-exhaustive enumeration.
- **CNF.1.2 — restricted definition.** Only marked or designated information, or
  information confirmed in writing within a set period.
Discriminator: does unmarked oral disclosure fall within the definition? Yes → 1.1.

### CNF.2 — obligations of the receiving party
- **CNF.2.1 — non-disclosure.** The prohibition on communicating to third parties.
- **CNF.2.2 — non-use / purpose limitation.** Use restricted to the defined
  purpose.
- **CNF.2.3 — standard of care.** Same care as own information / reasonable care
  benchmarks.
- **CNF.2.4 — permitted recipients.** Need-to-know disclosure to representatives,
  affiliates, advisers, with flow-down of obligations.
Discriminator 2.1 vs 2.2: prohibition on *external communication* vs prohibition
on *internal exploitation*.

### CNF.3 — exceptions and carve-outs
- **CNF.3.1 — status carve-outs.** Public domain, prior possession, independent
  development, third-party receipt without breach.
- **CNF.3.2 — compelled disclosure.** Disclosure required by law, regulator or
  court order, with notice and cooperation mechanics.
Discriminator: does the exception depend on the information's *status* (3.1) or on
an *external command* addressed to the recipient (3.2)?

### CNF.4 — duration of confidentiality obligations
Fixed term, indefinite, or differentiated duration for trade secrets. Distinct
from TRM.1 (term of the agreement itself) — see discriminator under TRM.

### CNF.5 — return or destruction of information
Including certification and retention carve-outs (legal archiving, automatic
back-ups).

### CNF.6 — trade secrets regime
Clauses invoking the specific protection of trade secrets.
Anchors: law of 26 June 2019 on the protection of undisclosed know-how and
business information, transposing Directive (EU) 2016/943.
Discriminator vs CNF.1: reliance on the statutory regime and its definitional
thresholds, not merely contractual confidentiality.

---

## DPR — data protection

- **DPR.1 — general GDPR compliance.** Mutual undertaking to comply with
  Regulation (EU) 2016/679 without allocating controller/processor roles.
- **DPR.2 — controller–processor mechanics.** Instructions, art. 28(3) content,
  role allocation.
- **DPR.3 — security measures.** Technical and organisational measures, art. 32.
- **DPR.4 — transfers and sub-processing.** Third-country transfers, SCCs,
  authorisation of sub-processors.
Discriminator DPR.1 vs DPR.2: does the clause allocate roles and impose
instruction-bound processing? If yes → 2.

---

## IPA — intellectual property

- **IPA.1 — reservation of rights / no licence.** Disclosure confers no IP rights.
- **IPA.2 — rights in results.** Ownership or assignment of materials or results
  generated during the evaluation.
- **IPA.3 — feedback and residuals.** Rights in feedback; residual knowledge
  (unaided memory) carve-outs.
Discriminator IPA.1 vs IPA.3: 1 protects the *discloser's existing* rights; 3
allocates rights in what the *recipient* generates or retains.

---

## PER — personnel restrictions

- **PER.1 — non-solicitation of personnel.** Prohibition on soliciting or hiring
  the other party's staff, with duration.
- **PER.2 — general-advertisement carve-out.** Untargeted recruitment excepted.
- **PER.3 — non-circumvention.** Prohibition on bypassing the counterparty to deal
  with its clients, sources or contacts.
Discriminator PER.1 vs PER.3: restriction on *hiring people* vs restriction on
*doing business around* the counterparty.

---

## LIA — liability and remedies

- **LIA.1 — liability cap.** Aggregate or per-event ceilings.
- **LIA.2 — cap carve-outs.** Fraud (dol), gross negligence (faute lourde),
  mandatory liability. Anchors: arts 1150–1151 Code civil [VERIFY].
- **LIA.3 — equitable relief acknowledgement.** Damages inadequate; injunction
  available without proof of harm where permissible.
- **LIA.4 — clause pénale / liquidated damages.** Pre-agreed sums per breach.
  Anchors: arts 1152 and 1226 et seq. Code civil (judicial revision power).
- **LIA.5 — indemnity.** Hold-harmless for third-party claims or defined losses.
Discriminator LIA.4 vs LIA.5: fixed pre-estimate owed between the parties (4) vs
loss-based recovery, typically third-party-facing (5).

---

## TRM — term and termination

- **TRM.1 — term of the agreement.** Duration of the NDA as a contract.
- **TRM.2 — survival.** Provisions surviving expiry or termination.
- **TRM.3 — termination rights.** Convenience or cause termination of the NDA.
Discriminator TRM.1 vs CNF.4: lifetime of the *contract* vs lifetime of the
*confidentiality obligation*; the two routinely diverge and must not share a code.

---

## GEN — general provisions

- **GEN.1 — entire agreement.**
- **GEN.2 — no waiver.**
- **GEN.3 — assignment.** Restrictions on transfer of the agreement.
- **GEN.4 — notices.**
- **GEN.5 — severability.**
- **GEN.6 — execution.** Counterparts, electronic signature.
  Anchors: Regulation (EU) 910/2014 (eIDAS) where e-signature is addressed.
- **GEN.7 — no partnership or agency.**
- **GEN.8 — announcements and publicity.** Restrictions on disclosing the
  existence or terms of the NDA or the underlying discussions.
Discriminator GEN.8 vs CNF.2.1: secrecy of the *relationship itself* vs secrecy of
the *information exchanged*.

---

## Residual codes

- `DSP.X`, `CNF.X`, `DPR.X`, `IPA.X`, `PER.X`, `LIA.X`, `TRM.X`, `GEN.X` —
  in-family residuals.
- `UNC` — unclassifiable within the NDA family.

Leaf count: 48 (+9 residuals). Target after calibration: whatever survives the
agreement threshold; expected pruning pressure on CNF.2 and DSP.2 sublevels.

---

## Calibration experiment protocol

1. **Sample.** 100–150 clauses drawn from the firm's NDA precedents, stratified by
   document age and by drafting origin (house paper vs counterparty paper).
   Anonymisation of party identifiers before processing.
2. **Classifiers.** Two structurally different models, independent runs,
   deterministic settings, identical instructions containing this taxonomy and the
   coding rules verbatim. Neither sees the other's output.
3. **Measurement.** Raw agreement and chance-corrected agreement (Cohen's kappa)
   at level 1 (family), level 2 and level 3 separately. Residual and UNC rates per
   family.
4. **Decision rule.** Retain a level where agreement ≥ the threshold set at run
   time (working hypothesis: 90% at level 1, 85% at level 2, 80% at level 3).
   Below threshold: merge sibling leaves into the parent and re-run on the
   disagreement set only.
5. **Outputs.** Calibrated taxonomy v1.0; measured per-level error rate (the
   figure the governance layer will cite); disagreement log feeding the first
   maintenance queue.

---

*Status tags in this document follow house convention: [VERIFY] marks statutory
references to be confirmed against Legilux before v1.0.*
