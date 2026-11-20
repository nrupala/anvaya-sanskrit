#!/usr/bin/env python3
"""Adapter: candidate analyses -> the one reading the rule reader
consumes, in the spike gold's token shape.

Disambiguation is by the sentence's own agreement, in a fixed order:
closed classes, the finite verb, absolutives, then agreement-support
fixing of every substantive (a candidate bundle earns support from
every other token already fixed with it, or able to take it), then
the karta (the nominative the verb's number admits, once adjectives
and names are out of the way), then the adjective conventions on the
fixed bundles. A sentence the adapter cannot fix completely is a
failure, and the chain's judge rejects that segmentation.
"""
from vidyut import lipi

import analyze
import segment

S2D = lambda s: lipi.transliterate(s, lipi.Scheme.Slp1,
                                   lipi.Scheme.Devanagari)

# The reader's closed-class contract: cls AVYAYA + a subtype.
CLOSED = {"ca": "coordinator", "iti": "iti", "aTa": "discourse",
          "tatra": "locative-adverb", "eva": None, "api": None,
          "tu": None, "hi": None, "vA": None, "na": None,
          "sma": None, "kila": None, "miTyA": None, "adya": None}
NUMSTEMS = {"eka", "dvi", "tri", "catur", "paYca", "zaz", "sapta",
            "azwan", "nava", "daSa", "Sata"}
PRONSTEMS = {"tad", "etad", "idam", "adas", "yad", "kim", "sarva",
             "anya", "sva", "bhavat", "asmad", "yuzmad"}
ABSOL_KRT = {"ktvA", "lyap"}
PART_KRT = {"kta", "Satf", "SAnac", "tavya", "anIya", "yat"}


class Fail(Exception):
    pass


def _bundles(cands):
    out = set()
    for c in cands:
        if c["kind"] == "pattern":
            for lin in c["lingas"]:
                out.add((c["vibhakti"], c["vacana"], lin))
        elif c["kind"] == "subanta" and c["vibhakti"]:
            out.add((c["vibhakti"], c["vacana"], c["linga"]))
    return out


def _cand_bundles(c):
    if c["kind"] == "pattern":
        return {(c["vibhakti"], c["vacana"], l) for l in c["lingas"]}
    if c["kind"] == "subanta" and c["vibhakti"]:
        return {(c["vibhakti"], c["vacana"], c["linga"])}
    return set()


def _is_compound(stem, kosha_path):
    """The stem splits into 2+ members attested in the kosha (member
    forms count here: a compound's members are stems, not padas).
    Members are at least 3 letters, so saciva stays a simple noun."""
    if len(stem) < 6:
        return False

    def valid(key, path):
        return "stem" if segment.entries(key, path) else None

    cands = segment._segment_span(stem, kosha_path, frozenset(),
                                  valid=valid, minpiece=3)
    return any(len(c) >= 2 for c in cands)


def adapt(sent_no, pieces, kosha_path):
    toks = []
    for i, (key, src) in enumerate(pieces):
        cands = analyze.candidates(key, src, kosha_path)
        if not cands:
            raise Fail(f"no candidates for {key}")
        # a substantive reading without a gender is the lexicon's
        # silence, not an option: where the key offers gendered
        # candidates, the genderless ones are dropped
        if any(c["kind"] in ("subanta", "pattern")
               and c.get("linga") for c in cands):
            cands = [c for c in cands
                     if c["kind"] not in ("subanta", "pattern")
                     or c.get("linga")]
        toks.append({"i": i, "key": key, "src": src, "cands": cands,
                     "cls": None, "subtype": None, "fixed": None,
                     "proper": False, "compound": False,
                     "naming_predicate": False})
    subs = lambda: [t for t in toks if t["cls"] is None]

    # 1. closed classes (the nama device marks its neighbour proper)
    for t in toks:
        if t["key"] == "nAma" and t["i"] > 0:
            t["cls"] = "AVYAYA"
            t["subtype"] = "nama-marker"
            toks[t["i"] - 1]["proper"] = True
        elif t["key"] in CLOSED:
            t["cls"] = "AVYAYA"
            t["subtype"] = CLOSED[t["key"]]

    # 1b. a token whose substantive candidates are ALL flagged
    # indeclinable in the lexicon is an avyaya (its listed case
    # bundle is a lexicon artifact, not an analysis); indeclinables
    # in absolutive form (-tva, or -ya on a prefixed root) are
    # absolutives
    for t in subs():
        subs_c = [c for c in t["cands"] if c["kind"] == "subanta"]
        if subs_c and all(c.get("avyaya") for c in subs_c) \
                and not any(c["kind"] == "tinanta" for c in t["cands"]):
            t["fixed"] = subs_c[0]
            if any(c.get("krt") in ABSOL_KRT for c in subs_c) \
                    or t["key"].endswith("tvA") or \
                    (t["key"].endswith("ya") and len(t["key"]) >= 6):
                t["cls"] = "ABSOL"
            else:
                t["cls"] = "AVYAYA"

    # 2. the finite verb (token only; its candidate is fixed with the
    # karta, whose number it must match)
    vib1_vac = set()
    for t in toks:
        for (v, vc, _l) in _bundles(t["cands"]):
            if v == 1:
                vib1_vac.add(vc)

    def verb_score(t):
        tin = [c for c in t["cands"] if c["kind"] == "tinanta"]
        if not tin:
            return -1
        s = 2 if len(tin) == len(t["cands"]) else 1
        p3 = [c for c in tin if c["person"] == 3]
        if p3:
            s += 1
        if any(c["vacana"] in vib1_vac for c in p3):
            s += 1
        return s

    scored = sorted(((verb_score(t), t) for t in toks),
                    key=lambda x: -x[0])
    if scored[0][0] < 2 or (len(scored) > 1
                            and scored[1][0] == scored[0][0]):
        raise Fail("no unique finite verb")
    verb = scored[0][1]
    verb["cls"] = "FINVERB"
    verb_p3 = [c for c in verb["cands"] if c["kind"] == "tinanta"
               and c["person"] == 3] or \
              [c for c in verb["cands"] if c["kind"] == "tinanta"]
    verb_vac = {c["vacana"] for c in verb_p3}

    # 3. absolutives
    for t in subs():
        ab = [c for c in t["cands"] if c["kind"] == "subanta"
              and c.get("krt") in ABSOL_KRT]
        if ab:
            t["cls"] = "ABSOL"
            t["fixed"] = ab[0]

    # compound flags on the remaining substantives
    for t in subs():
        stems = {c["stem"] for c in t["cands"] if c["kind"] != "tinanta"}
        t["compound"] = any(_is_compound(s, kosha_path) for s in stems)

    # a naming predicate makes unlisted nominatives names
    naming = any(c["stem"] == "nAman" and c.get("vibhakti") == 1
                 for t in subs() for c in t["cands"]
                 if c["kind"] in ("subanta", "pattern"))
    if naming:
        for t in subs():
            if t["src"] == "pattern" and \
                    any(v == 1 for (v, _vc, _l) in _bundles(t["cands"])):
                t["proper"] = True

    # 4. agreement-support fixing. The karta is fixed FIRST, out of
    # the nominatives the verb's number admits (names last), because
    # it is the anchor every other agreement hangs from.
    def support(t, c, use_fixed=True):
        mine = _cand_bundles(c)
        s = 0
        for o in toks:
            if o is t or o["cls"] == "ABSOL":
                continue
            if o["fixed"] is not None and use_fixed:
                ob = _cand_bundles(o["fixed"])
            elif o["cls"] in (None, "ADJ"):
                ob = set()
                for oc in o["cands"]:
                    ob |= _cand_bundles(oc)
            else:
                continue
            # per other token, only its BEST-matching bundle counts:
            # a paradigm's whole spread must not spray support onto
            # every common bundle in the sentence
            best_o = 0
            for (v, vc, l) in mine:
                for (ov, ovc, ol) in ob:
                    best_o = max(best_o,
                                 (2 if v == ov else 0)
                                 + (1 if vc == ovc else 0)
                                 + (1 if l == ol else 0))
            s += best_o
        # markedness prior: the dual is rare in prose, the vocative
        # is not a clause role
        if c.get("vacana") == "du":
            s -= 3
        if c.get("vibhakti") == 8:
            s -= 100
        # a stem's lexical gender binds its forms: a reading whose
        # gender is not among the stem's own genders is a homonym
        # artifact of the lexicon, not an analysis of this word
        if c["kind"] == "subanta" and c.get("stem_lingas") \
                and c.get("linga") not in c["stem_lingas"]:
            s -= 50
        return s

    elig = []
    for t in subs():
        for c in t["cands"]:
            if c["kind"] in ("subanta", "pattern") \
                    and c.get("vibhakti") == 1 \
                    and c.get("vacana") in verb_vac:
                elig.append((t, c))
    if not elig:
        raise Fail("no karta candidate")
    elig.sort(key=lambda tc: (tc[0]["proper"], tc[0]["compound"],
                              tc[1]["stem"] in NUMSTEMS,
                              -support(tc[0], tc[1], use_fixed=False),
                              tc[1].get("krt") is not None,
                              -len(tc[1]["stem"]), tc[0]["i"]))
    karta, kcand = elig[0]
    karta["fixed"] = kcand
    karta["cls"] = "NUM" if kcand["stem"] in NUMSTEMS else \
        ("PRON" if kcand["stem"] in PRONSTEMS else "NOUN")
    vc = [c for c in verb_p3 if c["vacana"] == kcand["vacana"]]
    verb["fixed"] = (vc or verb_p3)[0]

    # numerals are a closed class: a numeral candidate that agrees
    # with the karta is fixed at once (trayah qualifies the sons)
    kb = (kcand["vibhakti"], kcand["vacana"], kcand.get("linga"))
    for t in subs():
        num = [c for c in t["cands"] if c["kind"] == "subanta"
               and c["stem"] in NUMSTEMS
               and (c["vibhakti"], c["vacana"], c["linga"]) == kb]
        if num:
            t["fixed"] = num[0]
            t["cls"] = "NUM"

    todo = [x for x in toks if x["fixed"] is None
            and x["cls"] in (None, "ADJ")]
    for t in todo:
        if not any(c["kind"] in ("subanta", "pattern") for c in t["cands"]):
            raise Fail(f"no substantive candidate for {t['key']}")

    def role_pool(t):
        """Role economy: a second nominative has a role only if it
        agrees with the karta in number and gender (a qualifier or a
        name apposed to it). A nominative candidate that does not
        agree is not an analysis of this word in this sentence."""
        pool = [c for c in t["cands"]
                if c["kind"] in ("subanta", "pattern")]

        def agrees(c):
            if c.get("vibhakti") != 1:
                return True
            if c["kind"] == "pattern":
                return c["vacana"] == kb[1] and kb[2] in c["lingas"]
            return (c["vacana"], c.get("linga")) == (kb[1], kb[2])

        kept = [c for c in pool if agrees(c)]
        return kept or pool

    while todo:
        # unambiguous tokens first (one vibhakti across candidates)
        unamb = [t for t in todo
                 if len({c["vibhakti"] for c in role_pool(t)}) == 1]
        if unamb:
            t = unamb[0]
            t["fixed"] = max(role_pool(t),
                             key=lambda c: support(t, c))
            todo.remove(t)
            continue
        best_pair = None
        for t in todo:
            for c in role_pool(t):
                s = support(t, c)
                if best_pair is None or s > best_pair[0]:
                    best_pair = (s, t, c)
        if best_pair is None:
            raise Fail("fixing stalled")
        best_pair[1]["fixed"] = best_pair[2]
        todo.remove(best_pair[1])

    # 5. adjective conventions on the fixed bundles
    def fixed_bundle(t):
        f = t["fixed"]
        if f is None or f["kind"] == "tinanta":
            return None
        if f["kind"] == "pattern":
            kl = karta["fixed"].get("linga")
            lin = kl if kl in f["lingas"] else \
                ("m" if "m" in f["lingas"] else sorted(f["lingas"])[0])
            return (f["vibhakti"], f["vacana"], lin)
        return (f["vibhakti"], f["vacana"], f["linga"])

    # under a naming predicate, compound nominatives are names --
    # unless they agree fully with the karta, which makes them its
    # qualifiers (paramadurmedhasah qualifies the sons; the names
    # it introduces do not agree with them)
    if naming:
        kb = fixed_bundle(karta)
        for t in subs():
            if t["compound"] and t["fixed"] is not None \
                    and t["fixed"].get("vibhakti") == 1 \
                    and fixed_bundle(t) != kb:
                t["proper"] = True
    fixed_toks = [o for o in toks if o["fixed"] is not None]
    for t in subs():
        if t["compound"] and not t["proper"]:
            fb = fixed_bundle(t)
            if any(o is not t and not o["proper"]
                   and o["cls"] != "ADJ"
                   and not o.get("naming_predicate")
                   and fixed_bundle(o) == fb for o in fixed_toks):
                t["cls"] = "ADJ"
    # a case role is filled once per predicate: if more substantives
    # carry a case than there are predicates to govern it, the
    # earlier of two fully agreeing ones is the qualifier
    npred = 1 + sum(1 for t in toks if t["cls"] == "ABSOL")
    rest = subs()
    for a in range(len(rest)):
        ta = rest[a]
        if ta["cls"] is not None:
            continue
        fb = fixed_bundle(ta)
        if fb is None or fb[0] == 1:
            continue
        same_case = [o for o in fixed_toks
                     if o["fixed"].get("vibhakti") == fb[0]]
        if len(same_case) <= npred:
            continue
        for b in range(a + 1, len(rest)):
            tb = rest[b]
            tbb = fixed_bundle(tb)
            if tb["cls"] is None and tbb is not None \
                    and tbb[:2] == fb[:2] \
                    and not any(toks[k].get("subtype") == "coordinator"
                                for k in range(ta["i"], tb["i"])):
                ta["cls"] = "ADJ"
                # an adjective takes its head's gender: re-fix to the
                # head's bundle where the lexicon offers it
                pool = [c for c in ta["cands"]
                        if c["kind"] in ("subanta", "pattern")
                        and (c["vibhakti"], c["vacana"],
                             c.get("linga")) == tbb]
                if pool:
                    ta["fixed"] = pool[0]
                break
    for t in subs():
        f = t["fixed"]
        if f is not None and f.get("krt") in PART_KRT \
                and not t["proper"]:
            fb = fixed_bundle(t)
            if any(o is not t and fixed_bundle(o) == fb
                   for o in fixed_toks):
                t["cls"] = "ADJ"

    # 7. classes for the rest; the naming-predicate flag
    for t in subs():
        st = t["fixed"]["stem"]
        t["cls"] = "NUM" if st in NUMSTEMS else \
            ("PRON" if st in PRONSTEMS else "NOUN")
    for t in toks:
        if t["fixed"] is not None \
                and t["fixed"]["stem"] == "nAman" \
                and t["fixed"].get("vibhakti") == 1:
            t["naming_predicate"] = True

    # 8. assemble reader tokens
    out = []
    for t in toks:
        f = t["fixed"]
        form_slp = t["key"][:-1] + "H" if t["key"].endswith("s") \
            else t["key"]
        tok = {"id": f"s{sent_no}t{t['i'] + 1}", "sent": sent_no,
               "cls": t["cls"], "form": S2D(form_slp),
               "stem": f["stem"] if f else t["key"],
               "vibhakti": None, "vacana": None, "linga": None,
               "person": None, "voice": None, "subtype": t["subtype"],
               "proper": t["proper"],
               "naming_predicate": t["naming_predicate"],
               "compound": t["compound"]}
        if t["cls"] == "FINVERB":
            tok["person"] = f["person"]
            tok["vacana"] = f["vacana"]
            tok["voice"] = f["voice"]
        elif f is not None and f["kind"] in ("subanta", "pattern") \
                and t["cls"] in ("NOUN", "PRON", "ADJ", "NUM"):
            fb = fixed_bundle(t) if t is not karta else \
                (f["vibhakti"], f["vacana"], f.get("linga"))
            tok["vibhakti"] = fb[0]
            tok["vacana"] = fb[1]
            tok["linga"] = fb[2] if f["kind"] == "pattern" \
                else f["linga"]
        out.append(tok)
    return out
