
# contributing to lexml+

thank you for helping build **lexml+**. this guide sets expectations for contributors from both legal and engineering backgrounds.

## principles

* **accuracy first**: every rule must cite an authoritative source (ELI/ECLI or contract anchor).
* **machine-checkable**: submissions must pass **SHACL** and, where applicable, JSON Schema checks.
* **traceable**: preserve provenance; never paste text without a source.
* **british english**: consistent spelling, formal but clear tone.

---

## repo structure (quick reference)

* `vocab/0.1/` – vocabulary (`vocab.jsonld`, `vocab.ttl`, `changelog.md`)
* `shacl/0.1/` – SHACL shapes (`lexml_shapes.ttl`)
* `examples/nda/` – example DSL, compiled JSON-LD/LRML, tests
* `rule/` – immutable rule artefacts (`{RULE_ID}.jsonld`, `{RULE_ID}.lrml.xml`)
* `clauses/` – clause library (`seed.yaml`, approved/draft clauses)
* `schemas/` – JSON Schemas for assessment input/output
* `functions/` – Cloudflare Pages Functions (content negotiation, CRM)
* `api/` – OpenAPI specs
* `scripts/` – SQL migrations, helpers

---

## how to contribute (step by step)

### 1) propose a change

* open an **issue** describing:

  * problem statement,
  * proposed change (DSL, vocab term, clause, function),
  * sources (URLs or citations).
* if simple (typo, missing header), proceed straight to a PR.

### 2) create a branch

* branch name pattern:

  * `feat/<short-slug>` for new features,
  * `fix/<short-slug>` for fixes,
  * `docs/<short-slug>` for documentation.

### 3) add or update content

#### for lawyers (DSL / clauses)

* **clause ids**: uppercase, hyphenated, stable: `NDA-RETURN-30D`.
* **DSL** minimal fields:

  ```
  rule <ID>:
    source: <ELI/ECLI or contract://...>
    modality: obligation|prohibition|permission
    subject: <Role>
    action: <VerbPhrase>
    appliesFrom: YYYY-MM-DD
    [timeframe: ISO 8601 duration, e.g., P30D or PT72H]
    [exception|defence|sanction: Identifier]
  ```
* add to `clauses/*.yaml` or `clauses/*.json` with:

  * `id`, `title`, `status` (`approved|draft|needs-review`), `prose`, `dsl`, `sources[]`.
* if you add new DSL, run the compiler/transformer to generate `rule/{ID}.jsonld` and `.lrml.xml` (see **validation**).

#### for developers (code / vocab / shapes)

* **vocabulary** changes:

  * update `vocab/0.1/vocab.ttl` and regenerate `vocab.jsonld`.
  * record changes in `vocab/0.1/changelog.md`.
* **SHACL** changes:

  * update `shacl/0.1/lexml_shapes.ttl`.
  * keep shapes strict: required fields for `lex:subject`, `lex:action`, `prov:wasDerivedFrom`, `lex:appliesFrom`.
* **functions**:

  * keep content negotiation handlers for `/vocab`, `/shacl`, `/rule/{ID}` intact.
  * enforce correct `Content-Type` and `Cache-Control` headers.

### 4) validate

run locally before pushing:

```bash
# validate JSON-LD against SHACL (example NDA)
pyshacl -s shacl/0.1/lexml_shapes.ttl -d examples/nda/nda.jsonld

# validate schemas (requires ajv or similar)
npx ajv validate -s schemas/assessment.input.v1.json -d tests/nda_test.json
npx ajv validate -s schemas/assessment.output.v1.json -d tests/nda_expected.json
```

**acceptance for a PR**:

* no SHACL errors,
* JSON Schemas valid (if used),
* all rule files have sources and correct dates/durations,
* URIs follow the rules in **publishing and URIs**.

### 5) commit and open a PR

* **commit message**:

  * first line ≤ 72 chars, present tense:

    * `feat(dsl): add NDA-INCIDENT-72H obligation with PT72H timeframe`
    * `fix(vocab): correct range of lex:appliesFrom to xsd:date`
* link the issue (`closes #123`) where applicable.
* PR description must include:

  * summary of changes,
  * test evidence (SHACL/Schema output),
  * any impact on URIs or caching.

---

## publishing and URIs

* **immutable versioned files**:

  * `/vocab/0.1/vocab.jsonld`, `/vocab/0.1/vocab.ttl`, `/shacl/0.1/lexml_shapes.ttl`
  * headers: `Cache-Control: public, max-age=31536000, immutable`
* **latest pointers**:

  * `/vocab` and `/shacl` respond with **303**:

    * `Accept: application/ld+json` → JSON-LD
    * `Accept: text/turtle` → Turtle
    * otherwise → HTML landing
* **rule identifiers**:

  * canonical id: `/rule/{RULE_ID}`
  * prefer `.jsonld`, else `.lrml.xml`; landing page optional.

do not rename or move identifiers once published. if you must deprecate, add a deprecation note and keep the file.

---

## coding standards (functions / api)

* language: **typescript**.
* security headers on all responses:

  * `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
  * `X-Content-Type-Options: nosniff`
  * `Referrer-Policy: no-referrer`
  * `Content-Security-Policy: default-src 'self'`
* authentication (admin):

  * magic link (email) by default; argon2id fallback for a break-glass account.
* rate limits on public POST endpoints (`/api/crm/*`).

---

## legal and licensing

* **vocabulary, SHACL, documentation, examples** → **CC-BY 4.0**. include attribution metadata:

  * in TTL/JSON-LD: `dct:license <https://creativecommons.org/licenses/by/4.0/>`.
* **code (compiler, functions, CRM)** → **AGPLv3**. add SPDX header:

  ```
  // SPDX-License-Identifier: AGPL-3.0-or-later
  ```
* **dual licensing**: commercial exceptions via `COMMERCIAL-LICENSE.md` and `ORDER-FORM.md`.

---

## testing

* unit tests for DSL→JSON-LD transform and date/duration maths.
* regression tests: snapshot compiled JSON-LD for stable input.
* API contract tests using the OpenAPI spec in `api/openapi.yaml`.

---

## quality checklist (pre-PR)

* [ ] clause ids and DSL rule ids match exactly
* [ ] `source:` is present and resolvable
* [ ] `appliesFrom` uses `YYYY-MM-DD`
* [ ] `timeframe` uses ISO 8601 duration
* [ ] SHACL validation passes
* [ ] cache headers correct for any new versioned files
* [ ] docs updated (README, changelog) where needed

---

## security and privacy

* do not commit secrets. use environment variables for API keys.
* redact personal data in sample files; demo emails should be fictitious.
* vulnerabilities: report privately via the security contact in `SECURITY.md`.

---

## code of conduct

be respectful, constructive, and concise. critique the work, not the person. disagreements are resolved through evidence (sources, tests, standards).

---

## maintainers

* triage issues weekly,
* label PRs (`dsl`, `vocab`, `shacl`, `docs`, `functions`, `api`),
* require one reviewer from **legal** and one from **engineering** for changes in `vocab/`, `shacl/`, or `rule/`.

---

questions? open an issue with the label **question** and describe your context, the files involved, and the exact result you expect.
