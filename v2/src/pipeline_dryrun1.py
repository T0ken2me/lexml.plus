# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Erwin Sotiri / Jurisconsul
"""LexML end-to-end dry run: 6 documents -> tags -> validator -> indexes -> queries."""
import hashlib, json, math, re, time, unicodedata

FAMS = {"CON","REM","TER","DIS","DSP","GEN","IPA","PER","SPA"}  # v0.3 re-minted
T0 = time.perf_counter()

# ---------- normalisation (canonical form for hashing) ----------
def norm(t):
    t = unicodedata.normalize("NFC", t)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

def sha(t): return hashlib.sha256(norm(t).encode()).digest()
def clausehash(t): return str(int.from_bytes(sha(t)[:4], "big")).zfill(10)     # 32b -> 10 digits
def roothash_bytes(hs):
    lvl = list(hs)
    while len(lvl) > 1:
        if len(lvl) % 2: lvl.append(lvl[-1])
        lvl = [hashlib.sha256(lvl[i] + lvl[i+1]).digest() for i in range(0, len(lvl), 2)]
    return lvl[0]
def roothash(hs): return str(int.from_bytes(roothash_bytes(hs)[:6], "big")).zfill(15)  # 48b -> 15 digits

# ---------- documents ----------
DOCS = [
 # id, path, doctype, vintage YYMM, lang, matter
 ("N1","corpus/doc-N1.txt","NDA","1108","fr","matter-0003"),
 ("N2","corpus/doc-N2.txt","NDA","1108","fr","matter-0003"),
 ("S1","corpus/doc-S1.txt","SPA","1303","fr","matter-0001"),
 ("P1","corpus/doc-P1.txt","DIS","1110","fr","matter-0002"),
 ("P2","corpus/doc-P2.txt","DIS","1106","fr","matter-0002"),
 ("L1","corpus/doc-L1.txt","LTR","1303","fr","matter-0001"),
]

# ---------- segmentation ----------
FRONT = re.compile(r"(conclu entre|table.?s? des mati|pour\s*:|contre\s*:|fait à|signature|_____)", re.I)
def seg_numbered(t):   # NDA style: "1. Title. body"
    parts = re.split(r"(?m)^(?=\d\.\s+[A-ZÉÈ])", t)
    units = [p.strip() for p in parts if re.match(r"^\d\.", p.strip())]
    pre = parts[0]
    m = re.search(r"PREAMBULE(.*)", pre, re.S)
    if m and len(m.group(1).strip()) > 100: units.insert(0, "PREAMBULE " + m.group(1).strip()[:4000])
    return units
def seg_spa(t):        # markdown headings / ARTICLE
    parts = re.split(r"(?m)^(?=#{1,6}\s|ARTICLE\s+\d)", t)
    units = []
    for p in parts:
        p = p.strip()
        if len(p) < 80: continue
        if FRONT.search(p[:120]) and not re.match(r"#|ARTICLE", p): continue
        units.append(p[:6000])
    return units
def seg_pleading(t):   # moyens: numbered sections / markdown headings
    parts = re.split(r"(?m)^(?=#{1,6}\s|\d\.\d\s|\d\.\s+Quant)", t)
    units = [p.strip()[:6000] for p in parts if len(p.strip()) > 250 and not FRONT.search(p[:150])]
    return units

# ---------- heuristic classifier (tier C — pipeline test only) ----------
RULES = [
 (r"pr[ée]ambule|expos[ée]", "GEN1500"), (r"d[ée]finition", "CON0101"),
 (r"^\d\.\s*exclusions|ne constitue pas", "CON0301"),
 (r"restrictions.{0,30}obligations|ne communiquer une information", "CON0200"),
 (r"^\d\.\s*droits|aucun transfert de droits|propri[ée]t[ée] de la partie", "IPA0100"),
 (r"dur[ée]e de l'?accord|tacite reconduction", "TER0100"),
 (r"indemnisation|montant minimum du pr[ée]judice", "REM0400"),
 (r"loi applicable|r[ée]gi par la loi", "DSP0401"),
 (r"ind[ée]pendance des clauses|nulle ou non ex[ée]cutoire", "GEN0500"),
]
SPA_RULES = [
 (r"d[ée]finitions", "GEN0900"), (r"interpr[ée]tation", "GEN0900"),
 (r"objet", "SPA0100"), (r"prix", "SPA0201"), (r"modalit[ée]s de paiement", "SPA0202"),
 (r"d[ée]clarations et garanties", "SPA0400"), (r"garantie du c[ée]dant", "SPA0501"),
 (r"suret[ée]|garantie bancaire", "SPA0506"), (r"transfert de propri", "SPA0600"),
 (r"opposabilit", "SPA0600"), (r"juridiquement contraignant", "GEN1000"),
 (r"renonciation", "GEN0200"), (r"int[ée]gralit[ée]", "GEN0100"),
 (r"modification", "GEN0100"), (r"droit applicable", "DSP0401"),
 (r"r[èe]glement des diff[ée]rends|juridiction", "DSP0301"),
 (r"annexes", "GEN1600"), (r"pr[ée]ambule", "GEN1500"),
]
def classify(u, doctype):
    head = norm(u[:200])
    rules = SPA_RULES if doctype == "SPA" else RULES
    if doctype == "DIS":
        if re.search(r"nullit|libell|exception|communication des pi", head): return "DIS0102"
        return "DIS0201"
    for pat, code in rules:
        if re.search(pat, head): return code
    return ("SPA0400" if doctype == "SPA" else "GEN0000")  # GEN0000 = deliberate invalid to test validator? no:
# NOTE: fallback residual uses family + X convention -> encode residual as family+"00"
def classify2(u, doctype):
    c = classify(u, doctype)
    return c if c != "GEN0000" else "GENX"  # residual marker

# ---------- provision extraction (pleadings + SPA) ----------
PROV_PATTERNS = [
 (re.compile(r"article\s+(\d{1,4})\s+d[ue]s?\s+(?:nouveau\s+)?code de proc", re.I), lambda m: f"NCPC{int(m.group(1)):04d}00"),
 (re.compile(r"article\s+(\d{1,4})\s+du\s+code\s+civil", re.I), lambda m: f"CC{int(m.group(1)):04d}00"),
 (re.compile(r"art\.?\s*(\d{1,4})\s+du\s+c\s*ode\s+c\s*ivil", re.I), lambda m: f"CC{int(m.group(1)):04d}00"),
 (re.compile(r"article\s+(\d{1,3})\s+de la loi\s+du 27 juillet 1997", re.I), lambda m: f"LCA{int(m.group(1)):04d}00"),
 (re.compile(r"article\s+(\d{1,4})\s+des conditions", re.I), lambda m: None),  # contract-internal, not statute
 (re.compile(r"cour\s+(\d{1,2})\s+mars\s+1930", re.I), lambda m: "CAL19300325"),
 (re.compile(r"luxembourg,\s*13 novembre 1957", re.I), lambda m: "TAL19571113"),
]
def provisions(u):
    out = []
    for pat, f in PROV_PATTERNS:
        for m in pat.finditer(u):
            tok = f(m)
            if tok and tok not in out: out.append(tok)
    return out[:4]

# ---------- validator ----------
RE_D = re.compile(r"^D:([A-Z]{2})\.([A-Z]{2,4})/(\d{4})/([a-z]{2})(?:/([a-z0-9-]{1,16}))?/(\d{15})$")
RE_C = re.compile(r"^C:(\d{6})\.([A-Z]{3})(\d{2,6}|X)(?:\+([A-Z]{3})(\d{2,6}|X))?(?:/([A-Z0-9,]{0,64}))?/R(\d{1,2})/(\d{10})$")
RE_PROV = re.compile(r"^([A-Z]{2,4})(\d{4})(\d{2})$|^([A-Z]{2,3})(\d{4})(\d{1,6})$")
def validate(tag, roots, clause_texts):
    errs = []
    if tag.startswith("D:"):
        m = RE_D.match(tag)
        if not m: return ["grammar: doc-tag regex fail"]
        return errs
    m = RE_C.match(tag)
    if not m: return ["grammar: clause-tag regex fail"]
    docref, fam, cls, fam2, cls2, provs, rev, ch = m.groups()
    if fam not in FAMS: errs.append(f"unknown family {fam}")
    if fam2 and fam2 not in FAMS: errs.append(f"unknown secondary family {fam2}")
    if cls != "X" and len(cls) % 2: errs.append("class levels not 2-digit padded")
    if not any(r.startswith(docref) for r in roots): errs.append("dangling docref")
    if provs:
        for p in provs.split(","):
            if p and not RE_PROV.match(p): errs.append(f"bad prov token {p}")
    if ch in clause_texts and clausehash(clause_texts[ch]) != ch:
        errs.append("hash mismatch")
    return errs

# ---------- run pipeline ----------
all_tags, clause_store, doc_tags, simhashes = [], {}, {}, {}
def simhash64(t):
    words = norm(t).split()
    grams = [" ".join(words[i:i+3]) for i in range(max(1, len(words)-2))]
    v = [0]*64
    for g in grams:
        h = int(hashlib.md5(g.encode()).hexdigest(), 16)
        for b in range(64): v[b] += 1 if (h >> b) & 1 else -1
    return int("".join("1" if x > 0 else "0" for x in v), 2)

report = {"docs": [], "validator": {}, "queries": {}, "findings": []}
for did, path, doctype, vintage, lang, matter in DOCS:
    text = open(f"/home/claude/e2e/{path}", encoding="utf-8").read()
    if doctype == "LTR":
        units = []                       # single-act instrument: doc tag only
    elif doctype == "DIS":
        units = seg_pleading(text)
    elif doctype == "SPA":
        units = seg_spa(text)
    else:
        units = seg_numbered(text)
    hashes = [sha(u) for u in units] or [sha(text)]
    root = roothash(hashes)
    docref = root[:6]
    dtag = f"D:LU.{doctype}/{vintage}/{lang}/{matter}/{root}"
    doc_tags[did] = dtag; all_tags.append((did, "DOC", dtag))
    ctags = []
    for i, u in enumerate(units):
        code = classify2(u, doctype)
        fam, cls = code[:3], code[3:]
        ch = clausehash(u)
        provs = provisions(u)
        posture = "S" if re.search(r"subsidiaire", norm(u[:400])) else ""
        ptok = ",".join(provs)
        ctag = f"C:{docref}.{fam}{cls}" + (f"/{ptok}" if ptok else "/") + f"/R0/{ch}"
        clause_store[ch] = u
        simhashes.setdefault(did, []).append((ch, simhash64(u)))
        ctags.append(ctag); all_tags.append((did, f"U{i+1:02d}", ctag))
    report["docs"].append({"id": did, "doctype": doctype, "units": len(units),
                           "doc_tag": dtag, "clause_tags": len(ctags)})

roots = [t.split("/")[-1] for _, k, t in all_tags if k == "DOC"]
# docref collision check
refs = [r[:6] for r in roots]
report["findings"].append(f"docref collisions: {len(refs) - len(set(refs))} of {len(refs)}")

# ---------- validator: run on every generated tag + golden broken set ----------
ok, bad = 0, []
for did, k, t in all_tags:
    errs = validate(t, roots, clause_store)
    if errs: bad.append((did, k, t, errs))
    else: ok += 1
BROKEN = [
 "C:%s.CNF0201//R0/1234567890" % refs[0],          # old family, not re-minted
 "C:%s.CON021//R0/1234567890" % refs[0],           # odd-width class
 "C:999999.CON0201//R0/1234567890",                # dangling docref
 "C:%s.CON0201/9b2f4c1a/R0/1234567890" % refs[0],  # hex prov token
 "C:%s.CON0201+REM04+TER01//R0/1234567890" % refs[0],  # double secondary
 "D:LU.NDA/2011-08/fr/matter-0003/123456789012345",   # old date format
]
broken_caught = sum(1 for b in BROKEN if validate(b, roots, clause_store))
report["validator"] = {"generated_tags": len(all_tags), "valid": ok,
                       "invalid_generated": [(d, k, e) for d, k, _, e in bad],
                       "golden_broken": len(BROKEN), "caught": broken_caught}

# ---------- tamper test ----------
some = next(iter(clause_store))
tampered_text = clause_store[some] + " sauf accord contraire."
tamper_detect = clausehash(tampered_text) != some
report["findings"].append(f"tamper test (silent edit changes hash): {'DETECTED' if tamper_detect else 'MISSED'}")

# ---------- indexes ----------
tag_index = sorted(t for _, k, t in all_tags if k != "DOC")
hash_index = {t.split("/")[-1]: (d, k) for d, k, t in all_tags if k != "DOC"}
prov_index = {}
for d, k, t in all_tags:
    m = re.search(r"/([A-Z0-9,]+)/R", t)
    if m and m.group(1):
        for p in m.group(1).split(","):
            prov_index.setdefault(p, []).append((d, k))
class Bloom:
    def __init__(s, n, fp=0.01):
        s.m = math.ceil(-n*math.log(fp)/math.log(2)**2); s.k = max(1, round(s.m/n*math.log(2)))
        s.bits = bytearray(s.m)
    def _h(s, x): 
        a = int(hashlib.md5(x.encode()).hexdigest(), 16); b = int(hashlib.sha1(x.encode()).hexdigest(), 16)
        return [(a + i*b) % s.m for i in range(s.k)]
    def add(s, x):
        for p in s._h(x): s.bits[p] = 1
    def q(s, x): return all(s.bits[p] for p in s._h(x))
bloom = Bloom(len(tag_index))
for t in tag_index: bloom.add(t.split(".")[1].split("/")[0])

# ---------- live retrieval queries ----------
t1 = time.perf_counter()
q_dsp = [t for t in tag_index if re.search(r"\.\bDSP", t)]
q_law = [t for t in tag_index if ".DSP04" in t]
q_ncpc = {p: v for p, v in prov_index.items() if p.startswith("NCPC")}
t2 = time.perf_counter()
report["queries"]["all DSP clauses (prefix)"] = len(q_dsp)
report["queries"]["governing-law only (DSP04 prefix)"] = len(q_law)
report["queries"]["moyens citing NCPC (provision index)"] = {p: len(v) for p, v in q_ncpc.items()}
report["queries"]["bloom: corpus has CON clauses"] = bloom.q("CON0101")
report["queries"]["query time ms (all four)"] = round((t2-t1)*1000, 2)

# ---------- lineage: N1 vs N2 ----------
def ham(a, b): return bin(a ^ b).count("1")
pairs = []
for ch2, s2 in simhashes["N2"]:
    best = min(simhashes["N1"], key=lambda x: ham(x[1], s2))
    pairs.append(ham(best[1], s2))
ident = sum(1 for d in pairs if d <= 3); edited = sum(1 for d in pairs if 3 < d <= 14)
rew = sum(1 for d in pairs if 14 < d <= 25); new = sum(1 for d in pairs if d > 25)
report["queries"]["lineage N2 vs N1 (units: identical/edited/rewritten/new)"] = [ident, edited, rew, new]
report["findings"].append(f"total runtime {round((time.perf_counter()-T0)*1000)} ms for full corpus pipeline")

with open("/home/claude/e2e/out/tags.txt", "w") as f:
    for d, k, t in all_tags: f.write(f"{d} {k} {t}\n")
with open("/home/claude/e2e/out/report.json", "w") as f:
    json.dump(report, f, indent=1, ensure_ascii=False)
print(json.dumps(report, indent=1, ensure_ascii=False))
