import sys
sys.path.insert(0, ".")
import segment

K = "../vidyut-data/kosha"
for key in ["miTyA", "gatvA", "pra", "sarva", "sarvam", "mahi",
            "para", "param", "anyedyus", "eva", "ca"]:
    es = segment.entries(key, K)
    kinds = set()
    for e in es:
        if getattr(e, "is_avyaya", False):
            kinds.add("avyaya")
        elif getattr(e, "lakara", None) is not None:
            kinds.add("tinanta")
        else:
            pe = getattr(e, "pratipadika_entry", None)
            krt = str(getattr(pe, "krt", "")) if pe is not None else ""
            kinds.add(f"subanta/krt={krt}" if krt else "subanta")
    print(key, len(es), sorted(kinds)[:6])
