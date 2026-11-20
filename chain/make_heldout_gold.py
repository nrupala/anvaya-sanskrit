#!/usr/bin/env python3
"""Emit heldout-gold.json from the hand derivation in GOLD-HELDOUT.md."""
import json

T = []  # tokens
R = []  # relations


def tok(sent, n, cls, form, stem, v=None, vc=None, g=None, person=None,
        voice=None, subtype=None, proper=False, np=False, comp=False):
    T.append({"id": f"s{sent}t{n}", "sent": sent, "cls": cls,
              "form": form, "stem": stem, "vibhakti": v, "vacana": vc,
              "linga": g, "person": person, "voice": voice,
              "subtype": subtype, "proper": proper,
              "naming_predicate": np, "compound": comp})


def rel(i, sent, dep, head, r):
    R.append({"id": f"h{i}", "dep": f"s{sent}t{dep}",
              "head": f"s{sent}t{head}", "rel": r})


# H1
tok(1, 1, "AVYAYA", "तत्र", "tatra", subtype="locative-adverb")
tok(1, 2, "ADJ", "धर्मोपार्जितभूरिविभवः", "DarmopArjitaBUriviBava",
    1, "sg", "m", comp=True)
tok(1, 3, "NOUN", "वर्धमानकः", "varDamAnaka", 1, "sg", "m", proper=True)
tok(1, 4, "AVYAYA", "नाम", "nAma", subtype="nama-marker")
tok(1, 5, "NOUN", "वणिक्पुत्रः", "vaRikputra", 1, "sg", "m")
tok(1, 6, "FINVERB", "बभूव", "BU", vc="sg", person=3, voice="active")
rel(1, 1, 2, 5, "viśeṣaṇa")
rel(2, 1, 3, 5, "name-apposition")
rel(3, 1, 4, 3, "name-marker")
rel(4, 1, 5, 6, "kartā")
rel(5, 1, 1, 6, "adhikaraṇa")

# H2
tok(2, 1, "AVYAYA", "अथ", "aTa", subtype="discourse")
tok(2, 2, "NOUN", "रक्षापुरुषाः", "rakzApuruza", 1, "pl", "m")
tok(2, 3, "AVYAYA", "अपि", "api")
tok(2, 4, "ADJ", "बह्वपायम्", "bahvapAya", 2, "sg", "n", comp=True)
tok(2, 5, "PRON", "तत्", "tad", 2, "sg", "n")
tok(2, 6, "NOUN", "वनम्", "vana", 2, "sg", "n")
tok(2, 7, "ABSOL", "विदित्वा", "vid")
tok(2, 8, "NOUN", "संजीवकम्", "saYjIvaka", 2, "sg", "m", proper=True)
tok(2, 9, "ABSOL", "परित्यज्य", "tyaj")
tok(2, 10, "AVYAYA", "पृष्ठतः", "pfzWatas")
tok(2, 11, "ABSOL", "गत्वा", "gam")
tok(2, 12, "AVYAYA", "अन्येद्युः", "anyedyus")
tok(2, 13, "PRON", "तम्", "tad", 2, "sg", "m")
tok(2, 14, "NOUN", "सार्थवाहम्", "sArTavAha", 2, "sg", "m")
tok(2, 15, "AVYAYA", "मिथ्या", "miTyA")
tok(2, 16, "FINVERB", "आहुः", "brU", vc="pl", person=3, voice="active")
rel(6, 2, 1, 16, "discourse")
rel(7, 2, 2, 16, "kartā")
rel(8, 2, 4, 6, "viśeṣaṇa")
rel(9, 2, 5, 6, "viśeṣaṇa")
rel(10, 2, 6, 7, "karma")
rel(11, 2, 7, 16, "prior-action")
rel(12, 2, 8, 9, "karma")
rel(13, 2, 9, 16, "prior-action")
rel(14, 2, 11, 16, "prior-action")
rel(15, 2, 13, 14, "viśeṣaṇa")
rel(16, 2, 14, 16, "karma")

# H3
tok(3, 1, "AVYAYA", "अद्य", "adya")
tok(3, 2, "NOUN", "अस्मत्स्वामी", "asmatsvAmin", 1, "sg", "m", comp=True)
tok(3, 3, "NOUN", "पिंगलकः", "piNgalaka", 1, "sg", "m", proper=True)
tok(3, 4, "ADJ", "भीतः", "BIta", 1, "sg", "m")
tok(3, 5, "ADJ", "भीतपरिवारः", "BItaparivAra", 1, "sg", "m", comp=True)
tok(3, 6, "AVYAYA", "च", "ca", subtype="coordinator")
tok(3, 7, "FINVERB", "वर्तते", "vft", vc="sg", person=3, voice="active")
rel(17, 3, 2, 7, "kartā")
rel(18, 3, 3, 2, "name-apposition")
rel(19, 3, 4, 2, "viśeṣaṇa")
rel(20, 3, 5, 2, "viśeṣaṇa")
rel(21, 3, 6, 5, "coordinator")

# H4
tok(4, 1, "AVYAYA", "अथ", "aTa", subtype="discourse")
tok(4, 2, "AVYAYA", "कदाचित्", "kadAcit")
tok(4, 3, "NOUN", "पिंगलकः", "piNgalaka", 1, "sg", "m", proper=True)
tok(4, 4, "AVYAYA", "नाम", "nAma", subtype="nama-marker")
tok(4, 5, "NOUN", "सिंहः", "siMha", 1, "sg", "m")
tok(4, 6, "ADJ", "सर्वमृगपरिवृतः", "sarvamfgaparivfta", 1, "sg", "m",
    comp=True)
tok(4, 7, "ADJ", "पिपासाकुलः", "pipAsAkula", 1, "sg", "m", comp=True)
tok(4, 8, "NOUN", "उदकपानार्थम्", "udakapAnArTa", 2, "sg", "n")
tok(4, 9, "NOUN", "यमुनातटम्", "yamunAtawa", 2, "sg", "n")
tok(4, 10, "ADJ", "अवतीर्णः", "avatIrRa", 1, "sg", "m")
tok(4, 11, "NOUN", "संजीवकस्य", "saYjIvaka", 6, "sg", "m", proper=True)
tok(4, 12, "NOUN", "गंभीरतररावम्", "gamBIratararAva", 2, "sg", "m",
    comp=True)
tok(4, 13, "NOUN", "दूरात्", "dUra", 5, "sg", "n")
tok(4, 14, "AVYAYA", "एव", "eva")
tok(4, 15, "FINVERB", "अशृणोत्", "Sru", vc="sg", person=3, voice="active")
rel(22, 4, 1, 15, "discourse")
rel(23, 4, 3, 5, "name-apposition")
rel(24, 4, 4, 3, "name-marker")
rel(25, 4, 5, 15, "kartā")
rel(26, 4, 6, 5, "viśeṣaṇa")
rel(27, 4, 7, 5, "viśeṣaṇa")
rel(28, 4, 8, 15, "karma")
rel(29, 4, 9, 10, "karma")
rel(30, 4, 10, 5, "viśeṣaṇa")
rel(31, 4, 11, 12, "sambandha")
rel(32, 4, 12, 15, "karma")
rel(33, 4, 13, 15, "apādāna")

# H5
tok(5, 1, "PRON", "तत्", "tad", 1, "sg", "n")
tok(5, 2, "AVYAYA", "च", "ca", subtype="coordinator")
tok(5, 3, "NOUN", "वाणिज्यम्", "vARijya", 1, "sg", "n")
tok(5, 4, "ADJ", "सप्तविधम्", "saptaviDa", 1, "sg", "n", comp=True)
tok(5, 5, "NOUN", "अर्थागमाय", "arTAgama", 4, "sg", "m")
tok(5, 6, "FINVERB", "स्यात्", "as", vc="sg", person=3, voice="active")
rel(34, 5, 1, 3, "viśeṣaṇa")
rel(35, 5, 2, 1, "coordinator")
rel(36, 5, 3, 6, "kartā")
rel(37, 5, 4, 3, "viśeṣaṇa")
rel(38, 5, 5, 6, "sampradāna")

json.dump({"tokens": T, "relations": R}, open("heldout-gold.json", "w"),
          ensure_ascii=False, indent=1)
print(f"{len(T)} tokens, {len(R)} relations")
