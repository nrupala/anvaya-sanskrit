import sys
sys.path.insert(0, ".")
from vidyut import lipi
import segment, adapter, run_chain

KOSHA = "../vidyut-data/kosha"
line = open("heldout-sentences.txt").read().splitlines()[3]
toks, pieces = run_chain.run_sentence(4, line, KOSHA)
print("WINNER:", [k for k, _ in pieces])
slp = lipi.transliterate(line, lipi.Scheme.Devanagari, lipi.Scheme.Slp1)
cands = segment.segment_sentence(slp, KOSHA)
best = []
for i, p in enumerate(cands):
    try:
        ts = adapter.adapt(4, p, KOSHA)
        pred = run_chain.reader_pred(ts)
    except Exception:
        continue
    q = run_chain.judge(ts, pred, p)
    best.append((q, i, [k for k, _ in p]))
best.sort(key=lambda x: x[0], reverse=True)
for q, i, keys in best[:5]:
    print(q, "cand", i, keys)
