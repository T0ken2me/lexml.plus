<!-- SPDX-License-Identifier: CC-BY-4.0 — LexML v2 — E. Sotiri / Jurisconsul — lexml.eu -->
# LexML grammar v0.3.1 — FREEZE RECORD

Frozen: 24 July 2026. From this version, tags written are tags honoured:
amendments require a new grammar version through the governance gate, and
every prior tag remains resolvable against the version that produced it.

## Consolidated grammar (final)

    tag         = doc-tag | clause-tag ;
    doc-tag     = "D:" jur "." doctype "/" vintage "/" lang
                  [ "/" matter ] "/" roothash ;
    clause-tag  = "C:" docref "." class [ "+" class ]
                  "/" [ provisions ] "/R" rev "/" clausehash ;
    jur         = 2ALPHA ;                (* ISO 3166-1 alpha-2, or EU *)
    doctype     = 2*4 ALPHA ;             (* NDA SPA DIS SVC DOM MEM LTR ... *)
    vintage     = 4DIGIT ;                (* YYMM; 0000 = unknown, flagged *)
    lang        = 2ALPHA ;                (* ISO 639-1, lowercase *)
    matter      = 1*16( ALPHA / DIGIT / "-" ) ;   (* amended from 12: run-1 bug *)
    class       = family 2*6DIGIT | family "X" | "UNCX" ;
    family      = 3ALPHA ;                (* single-token screened at minting *)
    provisions  = prov *( "," prov ) ;
    prov        = code 4DIGIT 2DIGIT | court 4DIGIT 1*6DIGIT ;
    rev         = 1*2DIGIT ;
    roothash    = 15DIGIT ;               (* Merkle root, 48-bit, decimal *)
    docref      = 6DIGIT ;                (* prefix of roothash *)
    clausehash  = 10DIGIT ;               (* SHA-256 first 32 bits, decimal *)

Conventions fixed at freeze: hashes computed over NFC-normalised,
whitespace-collapsed, lowercased text; Merkle leaves in document order;
UNCX is the sole representation for units outside every family; front
matter is never a clause unit (Rule S4); single-act instruments carry a
doc-tag only; secondary class at most once.

## Families at freeze (re-minted, screened)

CON (confidentiality) · REM (remedies and liability) · TER (term and
termination) · DIS (disputes: DSP-adjacent litigation family for
pleadings) · DSP (dispute resolution clauses) · GEN · IPA · PER · SPA ·
DPR [token screen pending — the one open screen] · reserved pool: SEC CAP
IND RES END EXP FIN PLE PRO ARG EMP SER. Doctype transparency doctrine:
doctypes may trade one token for zero-shot recognisability (NDA retained).

## Dictionaries at freeze

Statute codes (18) and court codes (5) per the provision dictionary of
24 July 2026, plus OPC, LDOM and CDT patterns added in dry run 2; the
dictionary is append-only and versioned with the taxonomy.

## Evidence base

| Run | Result |
|---|---|
| NDA gate (independent) | L1 98.5 / L2 93.0 / exact 90.8 — passed |
| SPA gate (independent) | L1 100 / L2 97.8 / exact 94.6 — passed |
| Tokeniser test (4 BPE families) | ~18 tokens/tag; every finding consistent across all four |
| Dry run 1 (6 docs) | 97/97 valid; 6/6 broken caught; 1 grammar bug found and fixed |
| Dry run 2 (7 docs, 3 new genres) | 224/224 valid; 0 collisions over 13 docs |

## Open items carried past freeze (do not block tagging)

DPR token screen · SVC module gate · MEM module spec (third unit model) ·
DOM micro-module · LIT gate · NDA 2015-2022 out-of-sample re-verification ·
SPA sample top-up. All flow through the governance loop as scheduled
maintenance.
