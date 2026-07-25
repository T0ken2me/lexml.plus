// Tokeniser test for LexML tag grammar candidates.
// Measures token counts across three offline BPE families.
import { encode as cl100k } from "gpt-tokenizer/encoding/cl100k_base";
import { encode as o200k } from "gpt-tokenizer/encoding/o200k_base";
import { countTokens as claudeCount } from "@anthropic-ai/tokenizer";
import llama3 from "llama3-tokenizer-js";

const T = {
  cl100k: s => cl100k(s).length,
  o200k: s => o200k(s).length,
  claude_legacy: s => claudeCount(s),
  llama3: s => llama3.encode(s, { bos: false, eos: false }).length,
};

// ——— Candidate formats for the same clause tag content ———
// content: doc a3f9c1, class SPA.4.4, provision art. 166 LIR, rev 0, hash 9b2f4c1a
const CAND = {
  // current draft grammar
  "A_draft (C: . / R)":        "C:a3f9c1.SPA.4.4/166LIR/R0/9b2f4c1a",
  // delimiter variants
  "B_pipe":                    "C|a3f9c1|SPA.4.4|166LIR|R0|9b2f4c1a",
  "C_space":                   "C a3f9c1 SPA.4.4 166LIR R0 9b2f4c1a",
  "D_dash":                    "C-a3f9c1-SPA.4.4-166LIR-R0-9b2f4c1a",
  "E_all_dots":                "C.a3f9c1.SPA.4.4.166LIR.R0.9b2f4c1a",
  // case variants
  "F_lowercase":               "c:a3f9c1.spa.4.4/166lir/r0/9b2f4c1a",
  // provision order variants
  "G_prov_code_first":         "C:a3f9c1.SPA.4.4/LIR166/R0/9b2f4c1a",
  // hash alphabet variants (same entropy, different alphabet)
  "H_hash_digits":             "C:107329.SPA.4.4/166LIR/R0/26114052",
  "I_hash_base32upper":        "C:UF64Q3.SPA.4.4/166LIR/R0/TN5EWQZA",
  // fixed-width no-delimiter (positional parse only)
  "J_fixedwidth":              "Ca3f9c1SPA044166LIR—R09b2f4c1a".replace("—",""),
  // verbose baselines
  "K_json":                    '{"doc":"a3f9c1","class":"SPA.4.4","prov":["166LIR"],"rev":0,"hash":"9b2f4c1a"}',
  "L_xml":                     '<clause doc="a3f9c1" class="SPA.4.4" prov="166LIR" rev="0" hash="9b2f4c1a"/>',
};

// ——— Doc tag candidates ———
const DOC = {
  "draft":     "D:LU.SPA/2013-03/fr/matter-0001/a3f9c1d2e5b7",
  "compactdate":"D:LU.SPA/1303/fr/matter-0001/a3f9c1d2e5b7",
  "no_matter": "D:LU.SPA/2013-03/fr/a3f9c1d2e5b7",
};

// ——— Field-level probes ———
const FIELDS = {
  "family SPA": "SPA", "family spa": "spa", "family GEN": "GEN", "family CNF": "CNF",
  "class SPA.4.4": "SPA.4.4", "class spa.4.4": "spa.4.4",
  "prov 166LIR": "166LIR", "prov LIR166": "LIR166", "prov 1244NCPC": "1244NCPC", "prov NCPC1244": "NCPC1244",
  "hash hex8 9b2f4c1a": "9b2f4c1a", "hash digits8 26114052": "26114052", "hash b32 TN5EWQZA": "TN5EWQZA",
  "date 2013-03": "2013-03", "date 1303": "1303", "rev R0": "R0",
};

function table(obj) {
  const rows = [];
  for (const [name, s] of Object.entries(obj)) {
    const r = { name, chars: s.length };
    for (const [tk, f] of Object.entries(T)) r[tk] = f(s);
    r.mean = ((r.cl100k + r.o200k + r.claude_legacy + r.llama3) / 4).toFixed(1);
    rows.push(r);
  }
  return rows;
}

console.log("=== CLAUSE TAG CANDIDATES (same content) ===");
console.table(table(CAND));
console.log("=== DOC TAG CANDIDATES ===");
console.table(table(DOC));
console.log("=== FIELD PROBES ===");
console.table(table(FIELDS));

// ——— Index-reading scenario: 100 tags newline-separated ———
const mk = (i) => `C:a3f9c1.SPA.4.${i % 12}/166LIR/R${i % 4}/9b2f4c${(10 + i).toString(16)}`;
const idx100 = Array.from({ length: 100 }, (_, i) => mk(i)).join("\n");
const idx100_pipe = idx100.replace(/:/g, "|").replace(/\//g, "|");
console.log("=== INDEX SCENARIO: 100 tags, newline-separated ===");
for (const [tk, f] of Object.entries(T))
  console.log(`${tk}: draft=${f(idx100)} tokens (${(f(idx100) / 100).toFixed(1)}/tag)  pipe=${f(idx100_pipe)} tokens`);
