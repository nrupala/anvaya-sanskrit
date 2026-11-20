from vidyut import kosha as vk

k = vk.Kosha("../vidyut-data/kosha")
e = [x for x in k.get("rAjA") if getattr(x, "vibhakti", None) is not None][0]
print("vibhakti:", str(e.vibhakti), "| vacana:", str(e.vacana),
      "| linga:", str(e.linga))
t = k.get("baBUvus")[0]
print("purusha:", str(t.purusha), "| lakara:", str(t.lakara),
      "| prayoga:", str(t.prayoga), "| vacana:", str(t.vacana))
a = [x for x in k.get("Alokya")
     if getattr(getattr(x, "pratipadika_entry", None), "krt", None) is not None][0]
print("krt:", str(a.pratipadika_entry.krt))
g = [x for x in k.get("tasya") if getattr(x, "vibhakti", None) is not None][0]
print("tasya vib:", str(g.vibhakti), "stem:",
      g.pratipadika_entry.pratipadika.text)
