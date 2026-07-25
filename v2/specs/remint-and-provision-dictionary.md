# LexML mnemonic re-mint and provision-token dictionary (v0.1)

Date: 24 July 2026. Method: same four-tokeniser harness as the tokeniser
test (cl100k, o200k, legacy Claude, Llama 3). Adoption criterion: single
token on all four, verified in situ inside a full class code.

## 1. Family re-mints (adopted)

| Old | New | In-situ cost (class code) | Semantic |
|---|---|---|---|
| CNF | **CON** | CON0201 = 3 tokens (was 4) | confidentiality |
| LIA | **REM** | REM0400 = 3 (was 4) | remedies and liability |
| TRM | **TER** | TER0100 = 3 (was 4) | term and termination |
| LIT | **DIS** | DIS0102 = 3 (was 4) | disputes / pleadings |

Unchanged: DSP, PER, GEN (single everywhere); IPA, ADM and doctype SPA cost
two tokens only on the legacy Claude tokeniser, one on every current-era
vocabulary — kept, on watch. Migration is a pure mapping (old family →
new family) applied at the taxonomy layer; no tag semantics change.

**Reserved single-token pool** for future families, pre-screened: SEC, CAP,
IND, RES, END, EXP, FIN, PLE, PRO, ARG, EMP, SER. Minting rule stands: no
mnemonic without the screen.

## 2. The transparency exception (doctrine)

NDA measured at two tokens on every vocabulary, and is NOT re-minted. Token
cost is not the only axis: a mnemonic every model understands zero-shot has
retrieval value that a cheaper opaque code lacks, and doctype codes appear
only in document tags (one per document) rather than clause tags (dozens
per document), so the frequency-weighted cost is negligible. Rule: the
single-token screen binds families (high-frequency, taxonomy always in
context); for doctypes, semantic transparency may outweigh one token.

## 3. Provision-token grammar

    prov        = statute-ref | case-ref ;
    statute-ref = code art sub ;
    code        = 2*4 ALPHA ;          (* closed dictionary below *)
    art         = 4DIGIT ;             (* zero-padded article number *)
    sub         = 2DIGIT ;             (* 00 = none; covers "-n" suffixes
                                          and paragraph numbers alike *)
    case-ref    = court year num ;
    court       = 2*3 ALPHA ;          (* closed dictionary below *)
    year        = 4DIGIT ;
    num         = 1*6DIGIT ;           (* case number, or MMDD where the
                                          citation is date-based *)

No separators: zero-padding makes the fields positional, which the
tokeniser test showed is free (NCPC124400 = NCPC1244 = 4 tokens, while any
separator adds one to two tokens). Four-digit years in case-refs because
the corpus cites case law back to the 1930s. Known collapse: a statute's
article 28(3) and a hypothetical article 28-3 share a token; no statute in
the dictionary presents both forms.

Examples: art. 1244 NCPC → `NCPC124400` · art. 710-12 LSC → `LSC071012` ·
art. 28(3) GDPR → `GDPR002803` · art. 26 loi 1997 assurances → `LCA002600`
· Cour d'appel 25 mars 1930 → `CAL19300325` · CJEU C-311/18 →
`EUC2020311` [numbering convention: year of decision + case number].

## 4. Statute dictionary (initial, practice-weighted)

| Code | Instrument | Tokens |
|---|---|---|
| CC | Code civil (LU) | 1 |
| NCPC | Nouveau Code de procédure civile | 2 |
| LSC | loi modifiée du 10 août 1915, sociétés commerciales | 2 |
| CDT | Code du travail | 2 |
| LIR | loi modifiée du 4 décembre 1967, impôt sur le revenu | 2 |
| TVA | loi modifiée du 12 février 1979, TVA | 2 |
| LFS | loi modifiée du 5 avril 1993, secteur financier | 2 |
| LCA | loi du 27 juillet 1997, contrat d'assurance | 2 |
| LDA | loi du 18 avril 2001, droits d'auteur [VERIFY date] | 2 |
| LSA | loi du 26 juin 2019, secrets d'affaires | 2 |
| GDPR | Regulation (EU) 2016/679 | 2 |
| MICA | Regulation (EU) 2023/1114 (MiCAR) | 2 |
| DORA | Regulation (EU) 2022/2554 | 2 |
| AMLR | Regulation (EU) 2024/1624 [VERIFY number] | 2 |
| EIDA | Regulation (EU) 910/2014 (eIDAS) | 2 |
| BRU | Regulation (EU) 1215/2012 (Brussels I bis) | 2 |
| ROM | Regulation (EC) 593/2008 (Rome I) | 1 |
| CSSF | CSSF circulars: CSSF + yy + number (CSSF12552) | 2 |

Court dictionary: CAS (Cour de cassation LU), CAL (Cour d'appel LU, single
token), TAL (Tribunal d'arrondissement Lux) [VERIFY token cost at first
use], EUC (CJEU), ECH (ECtHR). Extension by the minting rule; the
dictionary is versioned with the taxonomy.

## 5. Measured full-tag costs after re-mint

| Tag | Tokens (cl100k) |
|---|---|
| `C:461738.CON0201/CC1382/R0/2611405283` | 18 |
| `C:461738.DIS0102/NCPC264,NCPC154/R0/2611405283` | 22 |

The re-mint takes the typical clause tag from 19.5 to ~18 mean tokens; a
two-provision litigation tag sits at 22. The grammar v0.3 delta is: family
codes per the table in section 1, prov tokens per section 3. With this,
every pre-freeze item on the grammar is closed except the reference
validator, which now has a complete, deterministic specification to
implement.
