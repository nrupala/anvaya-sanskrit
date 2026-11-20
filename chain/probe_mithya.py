import sys
sys.path.insert(0, ".")
import segment

K = "../vidyut-data/kosha"
for span in ["miTyAhuH", "kadAcit", "pfzWatas", "parityajya"]:
    cands = segment.segment_span(span, K, frozenset())
    print(f"== {span}: {len(cands)} segmentations")
    for c in cands[:8]:
        print("   ", c)
