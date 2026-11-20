from collections import Counter
from vidyut import kosha as vk

k = vk.Kosha("../vidyut-data/kosha")
es = k.get("ceti") or []
print("ceti n=", len(es))
sig = Counter()
for e in es:
    sig[(type(e).__name__, str(getattr(e, "vibhakti", None)),
         str(getattr(e, "lakara", None)))] += 1
for s, c in sig.items():
    print(" ", s, c)
print(repr(es[0])[:220])
for f in ("ca", "iti", "tatra", "aTa"):
    es = k.get(f) or []
    print(f, "n=", len(es), "avyaya:",
          sum(1 for e in es if getattr(e, "is_avyaya", False)))
