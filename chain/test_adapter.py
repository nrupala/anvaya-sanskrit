#!/usr/bin/env python3
"""Adapter check: gold segmentations in -> preserved reader scores."""
import json
import subprocess
import sys
import tempfile

sys.path.insert(0, ".")
import adapter

import os
KOSHA = "../vidyut-data/kosha"
SPIKE = os.path.expanduser(
    "~/workspace/codetopo-work/SANSKRIT-SPIKE-2026-11-19")

GOLD_PIECES = {
    1: [("asti", "kosha"), ("dAkziRAtye", "kosha"), ("janapade", "kosha"),
        ("mahilAropyam", "kosha"), ("nAma", "kosha"), ("nagaram", "kosha")],
    2: [("tatra", "kosha"), ("sakalArTisArTakalpadrumas", "kosha"),
        ("pravaramukuwamaRimarIcimaYjarIcarcitacaraRayugalas", "pattern"),
        ("sakalakalApAraNgatas", "pattern"), ("amaraSaktis", "kosha"),
        ("nAma", "kosha"), ("rAjA", "kosha"), ("baBUva", "kosha")],
    3: [("tasya", "kosha"), ("trayas", "kosha"), ("putrAs", "kosha"),
        ("paramadurmeDasas", "kosha"), ("vahuSaktis", "pattern"),
        ("ugraSaktis", "kosha"), ("anantaSaktis", "kosha"),
        ("ca", "kosha"), ("iti", "kosha"), ("nAmAnas", "kosha"),
        ("baBUvus", "kosha")],
    4: [("aTa", "kosha"), ("rAjA", "kosha"), ("tAn", "kosha"),
        ("SAstravimuKAn", "kosha"), ("Alokya", "kosha"),
        ("sacivAn", "kosha"), ("AhUya", "kosha"), ("provAca", "kosha")],
}

gold = json.load(open(f"{SPIKE}/gold.json"))
tokens = []
for sent in (1, 2, 3, 4):
    try:
        ts = adapter.adapt(sent, GOLD_PIECES[sent], KOSHA)
    except adapter.Fail as e:
        print(f"S{sent}: ADAPTER FAIL {e}")
        sys.exit(1)
    for t in ts:
        print(f"  {t['id']} {t['cls']:<11} {t['form']} stem={t['stem']} "
              f"v={t['vibhakti']} n={t['vacana']} g={t['linga']} "
              f"p={t['person']} prop={t['proper']} np={t['naming_predicate']}")
    tokens.extend(ts)

with tempfile.TemporaryDirectory() as d:
    json.dump({"tokens": tokens, "relations": gold["relations"]},
              open(f"{d}/gold.json", "w"), ensure_ascii=False)
    for mode in ("STRICT", "POSITIONAL"):
        r = subprocess.run([sys.executable, f"{SPIKE}/rule_reader.py",
                            mode], cwd=d, capture_output=True, text=True)
        lines = [l for l in r.stdout.splitlines()
                 if l.startswith("MODE") or " MISS " in l]
        print("\n".join(lines))
