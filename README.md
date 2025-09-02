# LexML+

**LexML+** is a hybrid framework for expressing legal rules in a **lawyer-friendly DSL** and compiling them into **JSON-LD** and **LegalRuleML** for automation, compliance checking, and explainability.
This repository contains the **vocabulary**, **SHACL shapes**, **example contracts**, **schemas**.

---

## 📂 Repository layout

```
/                     # site root
├─ vocab/             # controlled vocabulary (JSON-LD + TTL), versioned
│  └─ 0.1/
│     ├─ vocab.jsonld
│     ├─ vocab.ttl
│     └─ changelog.md
├─ shacl/             # SHACL validation shapes, versioned
│  └─ 0.1/
│     └─ lexml_shapes.ttl
├─ examples/          # sample rules and contracts
│  └─ nda/
│     ├─ nda-lexml.dsl
│     ├─ nda.jsonld
│     ├─ nda.lrml.xml
│     ├─ nda_test.json
│     └─ nda_expected.json
├─ rule/              # individual rule identifiers, immutable
│  ├─ NDA-12-4.jsonld
│  ├─ NDA-12-4.lrml.xml
│  └─ …
├─ clauses/           # clause library (seed YAML/JSON)
│  └─ seed.yaml
├─ schemas/           # input/output JSON Schemas for assessments
│  ├─ assessment.input.v1.json
│  └─ assessment.output.v1.json
├─ api/               # OpenAPI specs
│  └─ openapi.yaml
├─ functions/         # Cloudflare Pages Functions (content negotiation, CRM)
├─ scripts/           # SQL migrations, helpers
└─ README.md
```

---

## 🔑 Key ideas

* **DSL** – short, human-readable rule syntax (`rule NDA-12-4: modality: obligation …`).
* **JSON-LD** – linked data serialisation of rules, interoperable with RDF tools.
* **LegalRuleML** – XML serialisation for formal reasoning.
* **SHACL** – shapes to validate rule structures (e.g. modalities, dates, exceptions).
* **Publishing principles**:

  * Stable URIs (`/vocab/0.1/vocab.jsonld`, `/shacl/0.1/…`, `/rule/{ID}`)
  * Content negotiation on `/vocab` and `/shacl` (JSON-LD, Turtle, or HTML landing).
  * Versioned directories are immutable (cache-forever).

---

## ⚖️ Licensing

* **Vocabulary, SHACL, examples** → [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).
* **Code (compiler, functions, CRM)** → [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html).
* **Commercial use** → available under dual licensing, see `ORDER-FORM.md` and `PRICING-ANNEX.md`.

All users must display attribution:

> *Powered by LexML+ – © 2025 \ Erwin SOTIRI*

---

## 🚀 Deployment

* **GitHub → Cloudflare Pages + Functions**
* Functions handle:

  * `/vocab` and `/shacl` → 303 redirects with content negotiation
  * `/rule/{ID}` → resolves to `.jsonld` or `.lrml.xml`
  * `/api/crm/*` → contact, licensing, feedback, admin
* Database: **Cloudflare D1**
* Email: **SendGrid** (transactional + magic links for admin login)

---

## 🤝 Contributing

1. Fork the repo, create a branch (`feature/my-change`).
2. Update or add files (DSL, vocab, clauses, schemas).
3. Run SHACL validation (`pyshacl -s shacl/0.1/lexml_shapes.ttl -d examples/nda/nda.jsonld`).
4. Submit a pull request.

---


