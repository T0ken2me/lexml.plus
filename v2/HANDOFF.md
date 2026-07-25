# HANDOFF

The operational build brief for the production tagger (corpus locations,
environment access, build order against internal systems) is internal and
is not published here. It ships with the internal repository bundle and
lives in the firm vault.

What this public tree provides is everything needed to implement LexML v2
against any corpus: the frozen grammar (specs/), the calibrated
taxonomies (taxonomy/), the dictionaries, the reference validator
(src/validator.py) and the dry-run pipelines demonstrating the full
chain. Invariants that bind any implementation:

- Hash canonical form: NFC, whitespace-collapsed, lowercase; SHA-256;
  decimal rendering (10/15 digits); Merkle leaves in document order.
- Rule S4: front matter is never a clause unit; single-act instruments
  carry a document tag only.
- Tags carry identity and classification only; confidence, reviewers and
  usage live in a maintenance record keyed by clause hash.
- Taxonomy and dictionaries are append-only; deprecation is a mapping.
- No new mnemonic without the tokeniser screen (src/toktest).
