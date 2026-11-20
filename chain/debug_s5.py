import sys
sys.path.insert(0, ".")
from vidyut import lipi
import segment, adapter, run_chain

KOSHA = "../vidyut-data/kosha"
line = open("heldout-sentences.txt").read().splitlines()[4]
slp = lipi.transliterate(line, lipi.Scheme.Devanagari, lipi.Scheme.Slp1)
print("SLP1:", slp)
for key in ["syAt", "arTAgamAya", "saptaviDam", "vARijyam", "tat",
            "dUrAt", "kadAcit"]:
    print(key, "validate:", segment.validate(key, KOSHA),
          "entries:", len(segment.entries(key, KOSHA)))
cands = segment.segment_sentence(slp, KOSHA)
print(f"{len(cands)} candidates")
for i, pieces in enumerate(cands[:10]):
    keys = [k for k, _ in pieces]
    try:
        toks = adapter.adapt(5, pieces, KOSHA)
        pred = run_chain.reader_pred(toks)
        q = run_chain.judge(toks, pred, pieces)
        print(i, "READS", q, keys)
    except adapter.Fail as e:
        print(i, "FAIL", e, keys)
