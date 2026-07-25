// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 Erwin Sotiri / Jurisconsul
import { encode as cl100k } from "gpt-tokenizer/encoding/cl100k_base";
import { encode as o200k } from "gpt-tokenizer/encoding/o200k_base";
import { countTokens as claudeCount } from "@anthropic-ai/tokenizer";
import llama3 from "llama3-tokenizer-js";
const T = { cl100k: s=>cl100k(s).length, o200k: s=>o200k(s).length,
  claude: s=>claudeCount(s), llama3: s=>llama3.encode(s,{bos:false,eos:false}).length };
const mean = s => ((T.cl100k(s)+T.o200k(s)+T.claude(s)+T.llama3(s))/4);

// 1) equal-entropy hashes: 32 bits = 8 hex = 10 decimal digits; 48 bits = 12 hex = 15 digits
console.log("equal-entropy hash comparison:");
for (const [n,s] of [["hex8 (32b)","9b2f4c1a"],["dec10 (32b)","2611405283"],
                     ["hex12 (48b)","a3f9c1d2e5b7"],["dec15 (48b)","461738264051927"]])
  console.log(`  ${n}: chars=${s.length} mean=${mean(s).toFixed(1)}`);

// 2) family mnemonic screen: which 3-letter codes are single tokens everywhere?
console.log("\nfamily mnemonic screen (tokens cl100k/o200k/claude/llama3):");
for (const f of ["CNF","DSP","IPA","PER","LIA","TRM","GEN","SPA","LIT","SVC","CON","SEC","DIS","LAW","REM","DUR","ADM"])
  console.log(`  ${f}: ${T.cl100k(f)}/${T.o200k(f)}/${T.claude(f)}/${T.llama3(f)}`);

// 3) class encodings
console.log("\nclass encodings:");
for (const [n,s] of [["dotted SPA.4.4","SPA.4.4"],["dotted SPA.4.12","SPA.4.12"],
                     ["fixed SPA0404","SPA0404"],["fixed SPA0412","SPA0412"],["short SPA44","SPA44"]])
  console.log(`  ${n}: mean=${mean(s).toFixed(1)}`);

// 4) optimised composite vs draft — same information content
const draft   = "C:a3f9c1.SPA.4.4/166LIR/R0/9b2f4c1a";
const optA    = "C:107329.SPA0404/166LIR/R0/2611405283";      // dec docref + fixed class + dec hash
const optB    = "C 107329 SPA0404 166LIR R0 2611405283";      // space-delimited variant
const draftD  = "D:LU.SPA/2013-03/fr/matter-0001/a3f9c1d2e5b7";
const optD    = "D:LU.SPA/1303/fr/matter-0001/461738264051927";
console.log("\ncomposite comparison:");
for (const [n,s] of [["clause draft",draft],["clause optimised",optA],["clause opt space",optB],
                     ["doc draft",draftD],["doc optimised",optD]])
  console.log(`  ${n}: chars=${s.length} cl100k=${T.cl100k(s)} o200k=${T.o200k(s)} claude=${T.claude(s)} llama3=${T.llama3(s)} mean=${mean(s).toFixed(1)}`);

// 5) index scenario with optimised tags
const mk=i=>`C:107329.SPA04${String(i%12).padStart(2,"0")}/166LIR/R${i%4}/26114052${(83+i)}`;
const idx=Array.from({length:100},(_,i)=>mk(i)).join("\n");
console.log(`\noptimised index 100 tags: cl100k=${T.cl100k(idx)} (${(T.cl100k(idx)/100).toFixed(1)}/tag) claude=${T.claude(idx)} (${(T.claude(idx)/100).toFixed(1)}/tag)`);
