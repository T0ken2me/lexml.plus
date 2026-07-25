# LexML tokeniser test — results and grammar amendments (v0.2)

Date: 24 July 2026. Method: candidate tag formats measured against four real
BPE tokenisers with offline vocabularies (OpenAI cl100k_base and o200k_base,
Anthropic legacy Claude tokeniser, Llama 3). Caveat: the current Claude 4
tokeniser is unpublished; the legacy one stands in for the family. Every
finding below points the same direction on all four tokenisers, so the
conclusions are robust to tokeniser drift — which is itself the most
important property measured.

## Findings

**1. Hexadecimal hashes are the single biggest waste in the draft grammar.**
Hex fragments to one token per character; decimal digit runs merge three
digits per token. At equal entropy:

| Hash | Chars | Mean tokens |
|---|---|---|
| 32-bit as hex (8 chars) | 8 | 8.0 |
| 32-bit as decimal (10 chars) | 10 | **4.0** |
| 48-bit as hex (12 chars) | 12 | 12.0 |
| 48-bit as decimal (15 chars) | 15 | **5.3** |

More characters, half the tokens. Amendment: all hashes render in decimal.

**2. Family mnemonics have unequal prices.** Single-token on all four
tokenisers: DSP, PER, GEN, CON, SEC, DIS, REM. Costing two tokens: CNF,
LIA, TRM, LIT, DUR. Amendment: a minting rule — no family or doctype
mnemonic is admitted without a tokeniser screen; existing two-token
mnemonics (CNF, LIA, TRM, LIT) are re-minted from the single-token pool at
grammar freeze, with a mapping table (candidates: CNF→CON, LIA→REM,
LIT→DIS; to be screened together with any new families).

**3. Fixed-width class levels beat dotted.** SPA.4.4 costs 5.3 tokens;
SPA0404 (two digits per level, zero-padded) costs 3.3 and preserves the
prefix property exactly (SPA04 prefixes every child of SPA.4, without the
SPA.4/SPA.41 ambiguity that unpadded digits would create). Amendment
adopted.

**4. Compact dates.** YYMM (1303) at 2.0 tokens vs YYYY-MM at 3.8.
Amendment adopted; century ambiguity is not a risk inside a system whose
corpus starts in the 1990s and whose taxonomy versions are dated.

**5. Delimiters matter less than content alphabets.** Colon/dot/slash,
pipes and dashes are within a token of each other. Space-delimited is
cheapest (a further ~2 tokens, and the legacy Claude tokeniser favours it
strongly) but fragile when tags are embedded in prose or JSON; retained as
an optional index-file rendering, not the canonical form.

## Composite result

| Format | Mean tokens/tag |
|---|---|
| XML rendering (same content) | 40.5 |
| JSON rendering | 39.5 |
| Draft grammar v0.1 | 28.8 |
| **Amended grammar v0.2** | **19.5** |
| Space-delimited index rendering | 17.5 |

A 32% cut against the v0.1 draft and roughly 2× against JSON at identical
information content. The 100-tag index scenario measures 20.0 tokens per
tag (cl100k), against the ~15-18 estimated earlier: the estimate was
optimistic and the measured figure now replaces it everywhere.

## Grammar v0.2 delta (supersedes v0.1 fields)

    clausehash  = 10DIGIT ;              (* 32-bit, decimal *)
    roothash    = 15DIGIT ;              (* 48-bit, decimal *)
    docref      = 6DIGIT ;               (* prefix of roothash *)
    class       = family 2*6DIGIT ;      (* fixed 2-digit levels, zero-padded *)
    vintage     = 4DIGIT ;               (* YYMM *)
    family      = 3ALPHA ;               (* single-token screened at minting *)

Examples (v0.1 → v0.2):

    C:a3f9c1.SPA.4.4/166LIR/R0/9b2f4c1a
    C:461738.SPA0404/166LIR/R0/2611405283

    D:LU.SPA/2013-03/fr/matter-0001/a3f9c1d2e5b7
    D:LU.SPA/1303/fr/matter-0001/461738264051927

## Freeze status

The blocking item is cleared. Remaining before freeze: the mnemonic
re-minting screen (one session, using the same harness — kept at
/home/claude/toktest, portable) and the provision-token dictionary. The
validator implements v0.2 field rules as written above.
