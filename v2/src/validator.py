# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Erwin Sotiri / Jurisconsul
"""LexML reference validator — grammar v0.3.1 (FROZEN 2026-07-24).
Usage: python validator.py <tagfile> [rootsfile]
Each line of tagfile: a D: or C: tag (optionally prefixed by ids, last token used).
Semantic checks needing corpus context (docref resolution, hash recomputation)
run only when roots/clause text are supplied programmatically via validate()."""
import re, sys, unicodedata, hashlib

FAMS = {"CON","REM","TER","DIS","DSP","GEN","IPA","PER","SPA","DPR","UNC"}
RE_D = re.compile(r"^D:([A-Z]{2})\.([A-Z]{2,4})/(\d{4})/([a-z]{2})(?:/([a-z0-9-]{1,16}))?/(\d{15})$")
RE_C = re.compile(r"^C:(\d{6})\.(?:([A-Z]{3})(\d{2,6}|X)|(UNCX))(?:\+([A-Z]{3})(\d{2,6}|X))?/([A-Z0-9,]*)/R(\d{1,2})/(\d{10})$")
RE_PROV = re.compile(r"^([A-Z]{2,4})(\d{4})(\d{2})$|^([A-Z]{2,3})(\d{4})(\d{1,6})$")

def norm(t):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", t)).strip().lower()
def clausehash(t):
    return str(int.from_bytes(hashlib.sha256(norm(t).encode()).digest()[:4], "big")).zfill(10)

def validate(tag, roots=None, clause_texts=None):
    errs = []
    if tag.startswith("D:"):
        return errs if RE_D.match(tag) else ["grammar: doc-tag"]
    m = RE_C.match(tag)
    if not m: return ["grammar: clause-tag"]
    docref, fam, cls, unc, fam2, cls2, provs, rev, ch = m.groups()
    if fam and fam not in FAMS: errs.append(f"unknown family {fam}")
    if fam2 and fam2 not in FAMS: errs.append(f"unknown secondary family {fam2}")
    if cls and cls != "X" and len(cls) % 2: errs.append("class not 2-digit padded")
    if roots is not None and not any(r.startswith(docref) for r in roots):
        errs.append("dangling docref")
    for p in filter(None, (provs or "").split(",")):
        if not RE_PROV.match(p): errs.append(f"bad prov {p}")
    if clause_texts and ch in clause_texts and clausehash(clause_texts[ch]) != ch:
        errs.append("hash mismatch")
    return errs

if __name__ == "__main__":
    roots = None
    if len(sys.argv) > 2:
        roots = [l.strip() for l in open(sys.argv[2]) if l.strip()]
    bad = 0
    for i, line in enumerate(open(sys.argv[1]), 1):
        tag = line.split()[-1].strip()
        if not tag: continue
        errs = validate(tag, roots)
        if errs: bad += 1; print(f"line {i}: {tag} -> {errs}")
    print(f"{'PASS' if not bad else 'FAIL'} ({bad} invalid)")
