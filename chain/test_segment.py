#!/usr/bin/env python3
"""Segmentation check against the spike's hand pada-split."""
import sys
import time

sys.path.insert(0, ".")
from vidyut import lipi
import segment

D2S = lambda s: lipi.transliterate(s, lipi.Scheme.Devanagari, lipi.Scheme.Slp1)

CASES = [
    ("अस्ति दाक्षिणात्ये जनपदे महिलारोप्यं नाम नगरम्",
     ["asti", "dAkziRAtye", "janapade", "mahilAropyam", "nAma", "nagaram"]),
    ("तत्र सकलार्थिसार्थकल्पद्रुमः प्रवरमुकुटमणिमरीचिमञ्जरीचर्चितचरणयुगलः सकलकलापारङ्गतोऽमरशक्तिर्नाम राजा बभूव",
     ["tatra", "sakalArTisArTakalpadrumas",
      "pravaramukuwamaRimarIcimaYjarIcarcitacaraRayugalas",
      "sakalakalApAraNgatas", "amaraSaktis", "nAma", "rAjA", "baBUva"]),
    ("तस्य त्रयः पुत्राः परमदुर्मेधसो वहुशक्तिरुग्रशक्तिरनन्तशक्तिश्चेति नामानो बभूवुः",
     ["tasya", "trayas", "putrAs", "paramadurmeDasas", "vahuSaktis",
      "ugraSaktis", "anantaSaktis", "ca", "iti", "nAmAnas", "baBUvus"]),
    ("अथ राजा ताञ्शास्त्रविमुखान् आलोक्य सचिवान् आहूय प्रोवाच",
     ["aTa", "rAjA", "tAn", "SAstravimuKAn", "Alokya", "sacivAn", "AhUya",
      "provAca"]),
]

KOSHA = "../vidyut-data/kosha"
ok = 0
for dev, want in CASES:
    t0 = time.time()
    cands = segment.segment_sentence(D2S(dev), KOSHA)
    dt = time.time() - t0
    keylists = [[k for k, _ in c] for c in cands]
    rank = keylists.index(want) if want in keylists else -1
    mark = "OK " if rank >= 0 else "BAD"
    if rank >= 0:
        ok += 1
    print(f"{mark} ({dt:.1f}s) gold at rank {rank} of {len(keylists)}")
    if rank != 0:
        for i, kl in enumerate(keylists[:3]):
            print(f"     cand{i}={kl}")
        if rank < 0:
            print(f"     want={want}")
print(f"{ok}/{len(CASES)} sentences carry the gold segmentation")
