# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Erwin Sotiri / Jurisconsul
"""Dry run 2: seven new documents (memos, service agreements, domiciliation
template) through the pipeline; results merged with run 1 for corpus checks."""
import re, json, time, hashlib
src = open("/home/claude/e2e/pipeline.py", encoding="utf-8").read()
exec(src.split("# ---------- run pipeline")[0])   # reuse defs: norm, hashes, seg, validator, simhash...


def simhash64(t):
    words = norm(t).split()
    grams = [" ".join(words[i:i+3]) for i in range(max(1, len(words)-2))]
    v = [0]*64
    for g in grams:
        h = int(hashlib.md5(g.encode()).hexdigest(), 16)
        for b in range(64): v[b] += 1 if (h >> b) & 1 else -1
    return int("".join("1" if x > 0 else "0" for x in v), 2)


def seg_svc(t):
    lines = t.split("\n"); units=[]; top=""; cur=[]
    def flush():
        if cur:
            u=(top+" :: "+" ".join(cur)).strip()
            if len(u)>250 and u.count("|")<8: units.append(u[:6000])
    for ln in lines:
        if re.match(r"^#\s", ln):
            flush(); cur=[]; top=ln.lstrip("# ").strip()
        elif re.match(r"^##\s", ln):
            flush(); cur=[ln.lstrip("# ").strip()]
        elif cur is not None:
            cur.append(ln.strip())
    flush()
    return units

def seg_dom(t):
    parts=re.split(r"(?m)^(?=Article\s+\d)", t)
    return [p.strip()[:6000] for p in parts if len(p.strip())>200 and re.match(r"Article", p.strip())]

def seg_mem(t):
    blocks=re.split(r"\n\s*\n", t); units=[]; buf=""
    for b in blocks:
        b=b.strip()
        if b.count("|")>6 or len(b)<40: continue
        buf=(buf+" "+b).strip()
        if len(buf)>700: units.append(buf[:6000]); buf=""
    if len(buf)>300: units.append(buf[:6000])
    return units

T0 = time.perf_counter()
FAMS.update({"DPR", "UNC"})   # DPR readmitted (screen pending); UNC pseudo-family decision under test

DOCS2 = [
 ("M1","corpus/doc-M1.txt","MEM","1403","en","matter-0005"),
 ("V1","corpus/doc-V1.txt","SVC","1508","en","matter-0004"),
 ("V2","corpus/doc-V2.txt","SVC","1612","en","matter-0004"),
 ("M2","corpus/doc-M2.txt","MEM","0000","fr","matter-0006"),      # unknown vintage sentinel
 ("D1","corpus/doc-D1.txt","DOM","1201","fr","matter-0007"),
 ("M3","corpus/doc-M3.txt","MEM","1705","fr","matter-0008"),
 ("M4","corpus/doc-M4.txt","MEM","1406","en","matter-0009"),
]

def _old_seg_svc(t):
    # numbered top-level sections; drop TOC/table noise and short fragments
    body = t
    parts = re.split(r"(?m)^(?=#{1,6}\s?\d|\d{1,2}\s+[A-Z][a-zA-Z' ]{3,}$|\d{1,2}\t[A-Z])", body)
    units = []
    for p in parts:
        p = p.strip()
        if len(p) < 250: continue
        if p.count("|") > 8: continue                 # header/footer tables
        if re.match(r"contents", p, re.I): continue
        units.append(p[:6000])
    return units

def _old_seg_mem(t):
    parts = re.split(r"(?m)^(?=#{1,6}\s|\*\*[A-ZÀ-Ü])", t)
    units = [p.strip()[:6000] for p in parts if len(p.strip()) > 300 and p.count("|") < 8]
    return units

EN_RULES = [
 (r"^definitions", "GEN0900"), (r"^interpretation", "GEN0900"), (r"force majeure|relief event", "UNCX"), (r"service levels?|sla", "UNCX"), (r"^fees|payment", "UNCX"), (r"duties", "UNCX"), (r"regulatory change", "UNCX"), (r"beneficiar", "UNCX"), (r"^object of", "UNCX"), (r"audit", "UNCX"), (r"insurance", "UNCX"), (r"subcontract", "UNCX"), (r"governing law|applicable law", "DSP0401"),
 (r"jurisdiction|courts? of", "DSP0301"), (r"confidentialit", "CON0200"),
 (r"^\d{0,2}\s*term\b|duration", "TER0100"), (r"termination", "TER0300"),
 (r"limitation of liability", "REM0100"), (r"representations and warranties", "GEN1000"),
 (r"intellectual property", "IPA0100"), (r"data protection|personal data", "DPR0100"),
 (r"entire agreement", "GEN0100"), (r"notices", "GEN0400"), (r"severab", "GEN0500"),
 (r"assignment", "GEN0300"),
]
DOM_RULES = [
 (r"objet de la convention", "SPA0100"),  # deliberate stress: transfer leaf misuse? no — use residual below
]
def classify_v2(u, doctype):
    head = norm(u[:220])
    if doctype == "MEM":
        return "UNCX"                       # advisory genre: no clause taxonomy — pseudo-family decision
    if doctype == "SVC":
        for pat, code in EN_RULES:
            if re.search(pat, head): return code
        return "UNCX"  # service-specific: fees, SLA, duties, force majeure...
    if doctype == "DOM":
        for pat, code in RULES + [(r"objet", "UNCX"), (r"dénonciation|résiliation", "TER0300"),
                                  (r"honoraires|rémunération", "UNCX"), (r"obligations", "UNCX")]:
            if isinstance(code, str) and re.search(pat, head): return code
        return "UNCX"
    return "UNCX"

PROV2 = PROV_PATTERNS + [
 (re.compile(r"loi\s+(?:modifiée\s+)?du\s+31 mai 1999", re.I), lambda m: "LDOM000000"),
 (re.compile(r"loi\s+(?:modifiée\s+)?du\s+5 avril 1993", re.I), lambda m: "LFS0000000"[:10] and "LFS000000"),
 (re.compile(r"circulaire\s+(?:CSSF\s+)?12/552", re.I), lambda m: "CSSF12552"),
 (re.compile(r"chapt?er\s+15|chapitre\s+15", re.I), lambda m: "OPC001500"),   # law of 17 Dec 2010, ch. 15
 (re.compile(r"L\.?\s?(\d{3})-(\d{1,2})", re.I), lambda m: f"CDT{int(m.group(1)):04d}{int(m.group(2)):02d}"),
]
def provisions2(u):
    out = []
    for pat, f in PROV2:
        for m in pat.finditer(u):
            tok = f(m)
            if tok and tok not in out: out.append(tok)
    return out[:5]

# previous corpus roots for combined collision check
prev = [l.split()[2] for l in open("/home/claude/e2e/out/tags.txt") if " DOC " in l]
prev_roots = [t.split("/")[-1] for t in prev]

all_tags, clause_store2, sim2, report = [], {}, {}, {"docs": [], "residuals": {}, "findings": []}
for did, path, doctype, vintage, lang, matter in DOCS2:
    text = open(f"/home/claude/e2e/{path}", encoding="utf-8").read()
    units = seg_svc(text) if doctype == "SVC" else seg_mem(text) if doctype == "MEM" else seg_dom(text)
    hs = [sha(u) for u in units] or [sha(text)]
    root = roothash(hs); docref = root[:6]
    dtag = f"D:LU.{doctype}/{vintage}/{lang}/{matter}/{root}"
    all_tags.append((did, "DOC", dtag))
    resid = 0
    for i, u in enumerate(units):
        code = classify_v2(u, doctype)
        fam, cls = code[:3], code[3:]
        if fam == "UNC": resid += 1
        ch = clausehash(u); provs = provisions2(u)
        ctag = f"C:{docref}.{fam}{cls}" + ("/" + ",".join(provs) if provs else "/") + f"/R0/{ch}"
        clause_store2[ch] = u
        sim2.setdefault(did, []).append((ch, simhash64(u)))
        all_tags.append((did, f"U{i+1:02d}", ctag))
    report["docs"].append({"id": did, "doctype": doctype, "units": len(units), "doc_tag": dtag})
    report["residuals"][did] = f"{resid}/{len(units)}" + (f" ({resid/len(units):.0%})" if units else "")

roots = prev_roots + [t.split("/")[-1] for _, k, t in all_tags if k == "DOC"]
refs = [r[:6] for r in roots]
report["findings"].append(f"combined corpus docref collisions: {len(refs)-len(set(refs))} of {len(refs)} documents")

ok, bad = 0, []
for did, k, t in all_tags:
    errs = validate(t, roots, clause_store2)
    if errs: bad.append((did, k, t[:60], errs))
    else: ok += 1
report["validator"] = {"generated": len(all_tags), "valid": ok, "invalid": bad}

# cross-version dedup + lineage: the two service agreement versions
shared = 0
h1 = {ch for ch, _ in sim2.get("V1", [])}
for ch, _ in sim2.get("V2", []):
    if ch in h1: shared += 1
def ham(a, b): return bin(a ^ b).count("1")
pairs = []
for ch2, s2 in sim2.get("V2", []):
    if sim2.get("V1"):
        pairs.append(min(ham(s1, s2) for _, s1 in sim2["V1"]))
buck = [sum(1 for d in pairs if d <= 3), sum(1 for d in pairs if 3 < d <= 14),
        sum(1 for d in pairs if 14 < d <= 25), sum(1 for d in pairs if d > 25)]
report["findings"].append(f"service agreement V2 vs V1: identical clause hashes shared={shared}; lineage identical/edited/rewritten/new={buck}")

# provision index queries on new corpus
prov_index = {}
for d, k, t in all_tags:
    m = re.search(r"/([A-Z0-9,]+)/R", t)
    if m and m.group(1):
        for p in m.group(1).split(","): prov_index.setdefault(p, []).append((d, k))
report["queries"] = {
 "labour-code articles found (CDT*)": sorted([p for p in prov_index if p.startswith("CDT")])[:8],
 "docs touching CSSF 12/552": [d for d, _ in prov_index.get("CSSF12552", [])],
 "docs touching chapter 15 (OPC001500)": [d for d, _ in prov_index.get("OPC001500", [])],
 "domiciliation law (LDOM)": [d for d, _ in prov_index.get("LDOM000000", [])],
}
report["findings"].append(f"runtime {round((time.perf_counter()-T0)*1000)} ms")

with open("/home/claude/e2e/out/tags2.txt", "w") as f:
    for d, k, t in all_tags: f.write(f"{d} {k} {t}\n")
print(json.dumps(report, indent=1, ensure_ascii=False))
