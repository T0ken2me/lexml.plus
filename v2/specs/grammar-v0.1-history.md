# LexML tag grammar — spec v0.1 (pre-freeze)

Status: DRAFT. Freezes only after the tokeniser test on candidate alphabets.
This version introduces the document-level tag as a first-class object
(stress-test action 4) and defines both tag types formally.

## Two tag types

**Document tag (D).** One per document version. Carries what is true of the
whole instrument: jurisdiction, document type, vintage, language, optional
matter slug, and the Merkle root of its clause hashes. Single-operative-act
instruments (letters, notices, corporate acts) carry ONLY a document tag —
clause tags are optional below it, mandatory only for clause-structured
instruments.

**Clause tag (C).** One per clause unit. References its document by hash
prefix and does not repeat jurisdiction or language (inherited from the
document tag); carries the class, optional secondary class, referenced
provisions, revision counter and content hash.

## Grammar (EBNF)

    tag         = doc-tag | clause-tag ;
    doc-tag     = "D:" jur "." doctype "/" vintage "/" lang
                  [ "/" matter ] "/" roothash ;
    clause-tag  = "C:" docref "." class [ "+" class ]
                  [ "/" provisions ] "/" rev "/" clausehash ;
    jur         = 2*ALPHA ;              (* ISO 3166-1 alpha-2, or EU *)
    doctype     = 2*4 ALPHA ;            (* NDA, SPA, LIT, SVC, LTR ... *)
    vintage     = 4DIGIT "-" 2DIGIT ;    (* YYYY-MM *)
    lang        = 2ALPHA ;               (* ISO 639-1 *)
    matter      = 1*12( ALPHA / DIGIT / "-" ) ;
    class       = family *( "." 1*2DIGIT ) ;
    family      = 3ALPHA ;               (* CNF, DSP, SPA, LIT ... *)
    provisions  = prov *( "," prov ) ;
    prov        = 1*16( ALPHA / DIGIT ) ;  (* compressed ELI/ECLI token *)
    rev         = "R" 1*2DIGIT ;
    roothash    = 12HEXDIG ;             (* Merkle root, truncated *)
    docref      = 6HEXDIG ;              (* prefix of roothash *)
    clausehash  = 8HEXDIG ;              (* SHA-256 truncated *)

Examples:

    D:LU.SPA/2013-03/fr/matter-0001/a3f9c1d2e5b7
    C:a3f9c1.SPA.4.4/2013-03LIR/R0/9b2f4c1a
    C:a3f9c1.DSP.4.1+DSP.3.1//R0/1c7e2d90
    D:LU.LTR/2013-03/fr/matter-0001/77b1c04a2f10

## Validation rules (machine-checkable, complete)

1. Fixed field order; no optional reordering.
2. family must exist in the taxonomy version current at tagging time; the
   taxonomy version is resolvable from vintage.
3. docref must prefix-match an existing document tag's roothash.
4. clausehash must equal the truncated hash of the normalised clause text;
   mismatch flags the clause for re-tagging (the silent-edit detector).
5. Secondary class ("+") appears at most once (coding rule 1).
6. Posture and litigation-specific fields ride in the provisions position
   for LIT documents per the LIT module spec.

## Deliberate exclusions

Confidence tier, reviewer, assignment history and usage events are NOT in
the tag: they live in the maintenance record keyed by clausehash, per the
two-layer decision (retrieval never pays for governance metadata). The
SimHash and semantic binary codes likewise live in the index, keyed by
clausehash, never inline.

## Pre-freeze checklist

1. Tokeniser test: measure candidate delimiters and field alphabets against
   the tokenisers of the models in production use; adjust SEP characters and
   hash lengths to minimise token count. [BLOCKING]
2. Provision-token dictionary: closed list of compression rules from ELI/ECLI
   to prov tokens for the statutes the practice cites most.
3. Reference validator implementation plus golden test set.
