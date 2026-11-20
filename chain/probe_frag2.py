from vidyut import kosha as vk

k = vk.Kosha("../vidyut-data/kosha")
for f in ("prava", "kalApA", "apA", "raNgatas", "sakala", "vahu"):
    es = k.get(f) or []
    print(f, "n=", len(es))
    for e in es[:3]:
        pe = getattr(e, "pratipadika_entry", None)
        stem = None
        krt = None
        if pe is not None:
            p = getattr(pe, "pratipadika", None)
            stem = getattr(p, "text", None)
            krt = getattr(pe, "krt", None)
            if stem is None:
                de = getattr(pe, "dhatu_entry", None)
                stem = "dhatu:" + (getattr(de, "clean_text", "?") if de else "?")
        print("   stem=", stem, "krt=", krt,
              "vib=", getattr(e, "vibhakti", None),
              "lak=", getattr(e, "lakara", None),
              "avy=", getattr(e, "is_avyaya", None))
