#!/usr/bin/env python3
"""Score the full chain on raw text against a gold file.

Usage: score_chain.py <kosha-dir> <sentence-file> <gold.json>
Runs the chain, then scores the preserved reader's STRICT and
POSITIONAL output against the gold relations. Gold tokens pair to
chain tokens by what the reader itself sees — the case bundle for
substantives, the closed-class subtype for avyayas, the class alone
for predicates — by ordinal within the key (text order both sides).
A gold relation whose dep or head has no pair (a fused or shattered
segmentation) is a structural miss, counted before the reader runs.
"""
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_chain

SPIKE = os.path.expanduser(
    "~/workspace/codetopo-work/SANSKRIT-SPIKE-2026-11-19")


def mapkey(t):
    if t.get("vibhakti"):
        # gender is deliberately not part of the key: the chain
        # borrows gender for pattern-sourced tokens by design, so
        # pairing on it would score the borrowing, not the reading
        return (t["sent"], "B", t["vibhakti"], t["vacana"])
    if t["cls"] == "AVYAYA":
        return (t["sent"], "A", t.get("subtype"))
    return (t["sent"], t["cls"])


def main():
    kosha_path, sent_file, gold_file = sys.argv[1:4]
    gold = json.load(open(gold_file))
    tokens = []
    for i, line in enumerate(open(sent_file), 1):
        line = line.strip()
        if not line:
            continue
        ts, pieces = run_chain.run_sentence(i, line, kosha_path)
        print(f"S{i}: {[k for k, _ in pieces]}")
        tokens.extend(ts)
    cmap, gmap = {}, {}
    for t in tokens:
        cmap.setdefault(mapkey(t), []).append(t["id"])
    for t in gold["tokens"]:
        gmap.setdefault(mapkey(t), []).append(t["id"])
    pair = {}
    for k, gids in gmap.items():
        cids = cmap.get(k, [])
        for n, gid in enumerate(gids):
            if n < len(cids):
                pair[gid] = cids[n]
    # where a sentence's token count matches the gold's exactly,
    # pairing is by position (identity) — the bundle pairing above
    # is only the fallback for divergent tokenizations
    from collections import Counter
    cc = Counter(t["sent"] for t in tokens)
    gc = Counter(t["sent"] for t in gold["tokens"])
    for s in gc:
        if cc.get(s) == gc[s]:
            gt = [t for t in gold["tokens"] if t["sent"] == s]
            ct = [t for t in tokens if t["sent"] == s]
            if all(g.get("vibhakti") == c.get("vibhakti")
                   and g.get("vacana") == c.get("vacana")
                   for g, c in zip(gt, ct)):
                for g, c in zip(gt, ct):
                    pair[g["id"]] = c["id"]
    remapped, missed_structure = [], []
    for r in gold["relations"]:
        if r["dep"] in pair and r["head"] in pair:
            remapped.append({"id": r["id"], "dep": pair[r["dep"]],
                             "head": pair[r["head"]], "rel": r["rel"]})
        else:
            missed_structure.append(r["id"])
    total = len(gold["relations"])
    print(f"structural misses (segmentation): {missed_structure}")
    with tempfile.TemporaryDirectory() as d:
        json.dump({"tokens": tokens, "relations": remapped},
                  open(f"{d}/gold.json", "w"), ensure_ascii=False)
        for mode in ("STRICT", "POSITIONAL"):
            r = subprocess.run(
                [sys.executable, os.path.join(SPIKE, "rule_reader.py"),
                 mode], cwd=d, capture_output=True, text=True)
            head = [l for l in r.stdout.splitlines()
                    if l.startswith("MODE")]
            if not head:
                print(f"{mode}: reader failed: {r.stderr[-300:]}")
                continue
            rec = int(head[0].split()[2].split("/")[0])
            pct = 100.0 * rec / total
            print(f"MODE={mode}  recovered {rec}/{total} = {pct:.1f}%"
                  f"  (reader-scored {len(remapped)},"
                  f" structural {len(missed_structure)})")
            for l in r.stdout.splitlines():
                if " MISS " in l:
                    print("   ", l)
    json.dump(tokens, open("chain-tokens.json", "w"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
