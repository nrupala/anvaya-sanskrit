import sys
sys.path.insert(0, ".")
import adapter, run_chain

K = "../vidyut-data/kosha"
split = [("aTa", "kosha"), ("rAjan", "kosha"), ("tAn", "kosha"),
         ("SAstravimuKAn", "kosha"), ("Alokya", "kosha"),
         ("sacivAn", "kosha"), ("AhUya", "kosha"),
         ("provAca", "kosha")]
# find the real sources from the segmenter pool instead
import segment
from vidyut import lipi
line = open("fixture-sentences.txt").read().splitlines()[3]
slp = lipi.transliterate(line, lipi.Scheme.Devanagari, lipi.Scheme.Slp1)
for pieces in segment.segment_sentence(slp, K):
    keys = [k for k, _ in pieces]
    if "tAn" in keys or "tAYSAstravimuKAn" in keys:
        try:
            toks = adapter.adapt(4, pieces, K)
            pred = run_chain.reader_pred(toks)
            q = run_chain.judge(toks, pred, pieces)
            missing = [t["form"] for t in toks
                       if t["id"] not in pred
                       and t["cls"] != "FINVERB"
                       and not (t["cls"] == "AVYAYA"
                                and not t.get("subtype"))]
            print(q, keys, "unrelated:", missing)
        except Exception as e:
            print("FAIL", type(e).__name__, e, keys)
