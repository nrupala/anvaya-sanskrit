from vidyut import kosha as vk

k = vk.Kosha("../vidyut-data/kosha")
for f in ("v", "ahu", "ti", "sya", "ta"):
    es = k.get(f) or []
    print(f, "n=", len(es))
    for e in es[:3]:
        pe = getattr(e, "pratipadika_entry", None)
        stem = None
        if pe is not None:
            p = getattr(pe, "pratipadika", None)
            stem = getattr(p, "text", None)
            if stem is None:
                de = getattr(pe, "dhatu_entry", None)
                stem = "dhatu:" + (getattr(de, "clean_text", "?") if de else "?")
        print("   stem=", stem, "vib=", getattr(e, "vibhakti", None),
              "lak=", getattr(e, "lakara", None),
              "avy=", getattr(e, "is_avyaya", None),
              "lemma=", getattr(e, "lemma", None))
