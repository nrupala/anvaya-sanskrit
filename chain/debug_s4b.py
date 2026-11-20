import sys
sys.path.insert(0, ".")
from vidyut import lipi
import segment, adapter, run_chain

KOSHA = "../vidyut-data/kosha"
line = open("heldout-sentences.txt").read().splitlines()[3]
slp = lipi.transliterate(line, lipi.Scheme.Devanagari, lipi.Scheme.Slp1)
cands = segment.segment_sentence(slp, KOSHA)
pieces = cands[10]
toks = adapter.adapt(4, pieces, KOSHA)
pred = run_chain.reader_pred(toks)
for t in toks:
    rel = pred.get(t["id"])
    print(t["id"], t["cls"], t["form"], t.get("vibhakti"),
          t.get("vacana"), t.get("linga"), "prop", t["proper"],
          "->", rel)
