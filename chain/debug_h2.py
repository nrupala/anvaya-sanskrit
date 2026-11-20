import sys
sys.path.insert(0, ".")
from vidyut import lipi
import segment, adapter, run_chain

KOSHA = "../vidyut-data/kosha"
line = open("heldout-sentences.txt").read().splitlines()[1]
slp = lipi.transliterate(line, lipi.Scheme.Devanagari, lipi.Scheme.Slp1)
print("SLP1:", slp)
cands = segment.segment_sentence(slp, KOSHA)
print(f"{len(cands)} candidates")
for i, pieces in enumerate(cands):
    keys = [k for k, _ in pieces]
    try:
        toks = adapter.adapt(2, pieces, KOSHA)
        pred = run_chain.reader_pred(toks)
        q = run_chain.judge(toks, pred, pieces)
        print(i, "READS", q, keys)
    except adapter.Fail as e:
        print(i, "FAIL", e, keys)
