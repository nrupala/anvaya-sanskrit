import sys
sys.path.insert(0, ".")
from vidyut import lipi
import segment, adapter, run_chain

KOSHA = "../vidyut-data/kosha"
line = open("heldout-sentences.txt").read().splitlines()[3]
slp = lipi.transliterate(line, lipi.Scheme.Devanagari, lipi.Scheme.Slp1)
cands = segment.segment_sentence(slp, KOSHA)
print(f"{len(cands)} candidates")
shown = 0
for i, pieces in enumerate(cands):
    keys = [k for k, _ in pieces]
    if "piMgalakas" not in keys and shown > 6:
        continue
    try:
        toks = adapter.adapt(4, pieces, KOSHA)
    except Exception as e:
        print(i, "ADAPT-FAIL", e, keys)
        continue
    try:
        pred = run_chain.reader_pred(toks)
    except Exception as e:
        print(i, "READER-FAIL", type(e).__name__, keys)
        continue
    q = run_chain.judge(toks, pred, pieces)
    print(i, "READS", q, keys)
    shown += 1
    if shown > 14:
        break
