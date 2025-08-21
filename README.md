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


## Key ideas

- **DSL** – short, human-readable rule syntax (rule NDA-12-4: modality: obligation …).
- **JSON-LD** – linked data serialisation of rules, interoperable with RDF tools.
- **LegalRuleML** – XML serialisation for formal reasoning.
- **SHACL** – shapes to validate rule structures (e.g. modalities, dates, exceptions).
- **Publishing principles:**
→ Stable URIs (/vocab/0.1/vocab.jsonld, /shacl/0.1/…, /rule/{ID})
→ Content negotiation on /vocab and /shacl (JSON-LD, Turtle, or HTML landing).
→ Versioned directories are immutable (cache-forever).

## Deployment

**GitHub → Cloudflare Pages + Functions**
**Functions handle:
  → /vocab and /shacl → 303 redirects with content negotiation
  → /rule/{ID} → resolves to .jsonld or .lrml.xml
  → /api/crm/* → contact, licensing, feedback, admin

Database: **Cloudflare D1**
Email: **SendGrid** (transactional + magic links for admin login)

## Licensing

LexML+ is licensed under a multi-licence model to balance adoption and protection.

- **Vocabulary & SHACL shapes**: [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
  → free to use, remix, and redistribute with attribution.

- **Documentation & examples**: [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
  → free to reuse with attribution.

- **Compiler & scripts**: [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html)  
  → free software, modifications and SaaS deployments must also be AGPL compliant.  
  For commercial licensing exceptions, please contact [Your Contact Info].

**Summary:** you can use LexML+ openly, but attribution is always required, and commercial SaaS providers must either open their code under AGPL or obtain a commercial licence.
