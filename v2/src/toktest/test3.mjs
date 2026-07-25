// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Erwin Sotiri / Jurisconsul
import { encode as cl100k } from "gpt-tokenizer/encoding/cl100k_base";
import { encode as o200k } from "gpt-tokenizer/encoding/o200k_base";
import { countTokens as claudeCount } from "@anthropic-ai/tokenizer";
import llama3 from "llama3-tokenizer-js";
const T = { c1: s=>cl100k(s).length, o2: s=>o200k(s).length,
  cl: s=>claudeCount(s), l3: s=>llama3.encode(s,{bos:false,eos:false}).length };
const row = s => `${T.c1(s)}/${T.o2(s)}/${T.cl(s)}/${T.l3(s)}`;
const single = s => T.c1(s)===1 && T.o2(s)===1 && T.cl(s)===1 && T.l3(s)===1;

console.log("— family re-mint candidates (cl100k/o200k/claude/llama3, * = single everywhere) —");
const fams = {
 "CNF replacements": ["CON","SEC","CFD","PRV","KEP"],
 "LIA replacements": ["REM","DAM","CAP","IND","RES"],
 "TRM replacements": ["TER","END","TEN","EXP","FIN"],
 "LIT replacements": ["DIS","PLE","MOY","PRO","ARG"],
 "doctype screen":   ["NDA","SPA","SVC","SRV","SER","LTR","EMP","LSE","LOA"],
 "keep-as-is check": ["DSP","PER","GEN","IPA","ADM"],
};
for (const [g, list] of Object.entries(fams)) {
  console.log(g + ":");
  for (const m of list) console.log(`  ${m}: ${row(m)} ${single(m) ? "*" : ""}`);
}

console.log("\n— composite class check with re-minted families (family+4 digits) —");
for (const c of ["CON0201","REM0400","TER0100","DIS0102","SPA0404","GEN0900","CNF0201","LIA0400"])
  console.log(`  ${c}: ${row(c)}  total=${T.c1(c)}`);

console.log("\n— statute code screen —");
for (const s of ["NCPC","CC","LSC","LIR","GDPR","MICA","DORA","LFS","CDT","LSA","LDA","LCA","CSSF","AMLR","TVA","EUC","CAS","CAL","ROM","BRU","EID"])
  console.log(`  ${s}: ${row(s)} ${single(s) ? "*" : ""}`);

console.log("\n— provision token formats (code-first, sub-article variants) —");
for (const p of ["LIR166","NCPC1244","GDPR28","GDPR28-3","GDPR28.3","GDPR283","LSC710-12","CSSF12552","CSSF12-552","EUC19801","EUC19-801","CC1382","LSC100-1"])
  console.log(`  ${p}: ${row(p)}`);

console.log("\n— full v0.2 tags with re-minted mnemonics —");
for (const t of ["C:461738.CON0201/CC1382/R0/2611405283","C:461738.REM0400/CC1152,CC1226/R1/2611405283","C:461738.DIS0102/NCPC264,NCPC154/R0/2611405283"])
  console.log(`  ${t}  -> ${row(t)}`);
