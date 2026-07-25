# From LexML+ (v1) to LexML v2 — why the fundamentals changed

v1 and v2 are answers to different questions, and the honest framing is
supersession of purpose, not refinement. This note records what changed
and why, so the published v1 record stays intact and intelligible.

## What each generation describes

**v1 (LexML+)** models *rules*: deontic content (obligations,
permissions, modalities, exceptions) expressed in a lawyer-friendly DSL
and compiled to JSON-LD and LegalRuleML, validated by SHACL shapes,
aimed at automated compliance assessment and explainable reasoning. Its
consumers are semantic-web tooling, formal reasoners and human authors.

**v2 (LexML)** models *clauses and documents as retrievable objects*:
each clause carries a coordinate — cryptographic content hash, lexical
fingerprint, taxonomy class, cited provisions — so that large language
models can locate, deduplicate, version-trace and retrieve firm
knowledge without reading whole documents. Its consumer is an LLM
context window, and its budget is measured in tokens.

## Why the change

1. **The consumer changed.** Between 2025 and 2026 the practical reader
   of structured legal data became the language model, not the RDF
   reasoner. A representation optimised for triple stores is close to
   worst-case for a BPE tokeniser; v2's grammar was designed against
   four real tokenisers and costs roughly half the tokens of an
   equivalent JSON rendering.
2. **Human readability was dropped as a requirement.** v1's DSL kept
   the lawyer in the syntax. v2 concluded that humans read documents
   and models read coordinates; asking one notation to serve both made
   it worse at each. Machine-only formatting (fixed positions, decimal
   hashes, zero-padded classes) follows directly.
3. **Authored rules gave way to measured classification.** v1 rules are
   written one by one and validated structurally (SHACL). v2 classifies
   clauses statistically with independent-model agreement gates
   (90/85/80 thresholds), records measured error rates in public
   registers, and repairs its taxonomy through residual-rate sensors
   rather than curation.
4. **Identity became cryptographic.** v1 identifies rules by minted
   URIs; v2 identifies clauses by content hash, which yields
   tamper-evidence, cross-document deduplication and version genealogy
   as free consequences rather than added features.

## What survives

The publishing principles carry over almost unchanged: stable
identifiers, immutable versioned directories, append-only evolution
with deprecation-by-mapping. v2's taxonomy governance is a
generalisation of v1's versioning discipline. The NDA domain remains
the reference example in both generations.

## Mapping

No mechanical mapping between v1 rule identifiers and v2 clause
coordinates is maintained: the objects differ (deontic rules vs clause
instances). Where a conceptual correspondence exists (v1 vocabulary
clause categories and v2 taxonomy families), it can be reconstructed
from the two published vocabularies; a mapping table will be added only
if a concrete use case requires one.

## Status

v1 stays published and served; its URIs will not break. Development,
calibration and all new work happen in v2.
