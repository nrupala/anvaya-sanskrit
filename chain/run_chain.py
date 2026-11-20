#!/usr/bin/env python3
"""The full chain, end to end, on raw printed text:

  Devanagari text
    -> vidyut lipi transliteration (Devanagari -> SLP1)
    -> DP sandhi segmenter (K best candidate segmentations)
    -> vidyut kosha candidate analyses
    -> adapter (agreement fixing; the judge picks the segmentation
       whose reading is complete and best evidenced)
    -> the spike's preserved rule reader (anvaya mode)
    -> relations

Usage: run_chain.py <kosha-dir> <sentence-file>
The sentence file holds one Devanagari sentence per line.
Prints the chosen tokens as JSON.
"""
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vidyut import lipi

import adapter
import segment

D2S = lambda s: lipi.transliterate(s, lipi.Scheme.Devanagari,
                                   lipi.Scheme.Slp1)
SPIKE = os.path.expanduser(
    "~/workspace/codetopo-work/SANSKRIT-SPIKE-2026-11-19")
READER_SRC = open(os.path.join(SPIKE, "rule_reader.py")).read()


def reader_pred(tokens, mode="POSITIONAL"):
    """Run the preserved reader over tokens; return its pred dict."""
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "gold.json"), "w") as f:
            json.dump({"tokens": tokens,
                       "relations": [{"dep": tokens[0]["id"],
                                      "head": tokens[-1]["id"],
                                      "rel": "none", "id": "g0"}]}, f,
                      ensure_ascii=False)
        argv, cwd = sys.argv, os.getcwd()
        sys.argv = ["rule_reader.py", mode]
        os.chdir(d)
        try:
            ns = {}
            with redirect_stdout(io.StringIO()):
                exec(compile(READER_SRC, "rule_reader.py", "exec"), ns)
            return ns["pred"]
        finally:
            sys.argv, cwd = argv, cwd
            os.chdir(cwd)


def judge(tokens, pred, pieces):
    # completeness: every token related, except the finite verb
    # (the reader's root — it is a head, never a dependent) and
    # avyayas outside the reader's subtype vocabulary (kadacit,
    # eva, mithya...), which the reader's grammar does not relate
    complete = all(t["id"] in pred or t["cls"] == "FINVERB"
                   or (t["cls"] == "AVYAYA" and not t.get("subtype"))
                   for t in tokens)
    function = sum(1 for t in tokens
                   if t["cls"] == "AVYAYA" and t.get("subtype"))
    # indeclinables recognized — but only full words count: a
    # shattered fragment that happens to be flagged indeclinable
    # (upa, a prefix) is not a recovered avyaya
    avy = sum(1 for t, (k, _s) in zip(tokens, pieces)
              if t["cls"] == "AVYAYA"
              and (len(k) >= 4 or t.get("subtype")))
    patterns = sum(1 for (_k, s) in pieces if s == "pattern")
    # agreement coherence: how many substantive pairs share a full
    # case bundle. The right reading of a sentence is the one whose
    # words agree with each other in clusters (tan with the two
    # -an plurals it qualifies among), not the one whose fragments
    # each sit alone.
    bundles = [(t["vibhakti"], t["vacana"], t["linga"])
               for t in tokens if t.get("vibhakti")]
    coherence = sum(1 for i, b in enumerate(bundles)
                    for j, o in enumerate(bundles) if i < j and b == o)
    # order: a complete reading; then the sentence's connective
    # tissue recovered (ca, iti, the nama device); then more
    # indeclinables recognized as indeclinables; then fewer pattern
    # guesses; then fewer pieces. (Two terms were tried and
    # removed: agreement coherence, which rewarded phantom
    # clusters, and a short-piece fragment count, which punished
    # legitimate short words — raja, tan.)
    return (complete, function, avy, -patterns, -len(pieces))


def run_sentence(sent_no, dev_text, kosha_path):
    cands = segment.segment_sentence(D2S(dev_text), kosha_path)
    best = None
    for pieces in cands:
        try:
            tokens = adapter.adapt(sent_no, pieces, kosha_path)
            pred = reader_pred(tokens)
        except Exception:
            # a reading the preserved reader cannot process at all
            # (it assumes an expressed karta) is not a reading
            continue
        q = judge(tokens, pred, pieces)
        if best is None or q > best[0]:
            best = (q, tokens, pieces)
    if best is None:
        raise adapter.Fail(f"S{sent_no}: no segmentation read completely")
    return best[1], best[2]


def main():
    kosha_path, sent_file = sys.argv[1], sys.argv[2]
    out = []
    for i, line in enumerate(open(sent_file), 1):
        line = line.strip()
        if not line:
            continue
        tokens, pieces = run_sentence(i, line, kosha_path)
        print(f"S{i}: {[k for k, _ in pieces]}", file=sys.stderr)
        out.extend(tokens)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
