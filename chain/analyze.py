#!/usr/bin/env python3
"""Morphological analysis: a citation key -> ALL candidate analyses.

The analyzer is the vidyut kosha (a lexicon, not a parser): for each
key it returns every analysis the lexicon attests. Disambiguation is
not done here; the adapter disposes by agreement. Pattern-sourced
pieces (unlisted compounds and names) get their analyses from the
segmenter's ending-pattern table.
"""
import segment

VIB = {"praTamA": 1, "dvitIyA": 2, "tftIyA": 3, "caturTI": 4,
       "paYcamI": 5, "zazWI": 6, "saptamI": 7, "samboDanam": 8}
VAC = {"eka": "sg", "dvi": "du", "bahu": "pl"}
LIN = {"puM": "m", "strI": "f", "napuMsaka": "n"}
PUR = {"praTama": 3, "maDyama": 2, "uttama": 1}
PRAY = {"kartari": "active", "karmaNi": "passive"}


def _enum(x):
    return str(x) if x is not None else None


def candidates(key, source, kosha_path):
    if source == "pattern":
        if key.endswith("cit") and len(key) >= 5:
            # the -cit indefinites (kadAcit, kvacit) are avyayas;
            # the kosha does not list them
            return [{"kind": "subanta", "stem": key, "vibhakti": None,
                     "vacana": None, "linga": None, "stem_lingas": [],
                     "krt": None, "avyaya": True}]
        return [{"kind": "pattern", "stem": st, "vibhakti": v,
                 "vacana": vc, "lingas": sorted(ls)}
                for (st, v, vc, ls) in segment.pattern_candidates(key)]
    out = []
    if key.endswith("At") and len(key) >= 4:
        # -At is the a-stem ablative's shape; where the lexicon's
        # readings for the key are other lexemes' homonyms, the
        # ending's own evidence is added as a candidate
        for (st, v, vc, ls) in segment.pattern_candidates(key):
            if v == 5:
                out.append({"kind": "pattern", "stem": st,
                            "vibhakti": v, "vacana": vc,
                            "lingas": sorted(ls)})
    for e in segment.entries(key, kosha_path):
        lak = getattr(e, "lakara", None)
        if lak is not None:
            de = e.dhatu_entry
            out.append({"kind": "tinanta", "stem": de.clean_text,
                        "person": PUR[_enum(e.purusha)],
                        "vacana": VAC[_enum(e.vacana)],
                        "lakara": _enum(lak),
                        "voice": PRAY.get(_enum(e.prayoga), "active")})
            continue
        pe = getattr(e, "pratipadika_entry", None)
        krt = getattr(pe, "krt", None) if pe is not None else None
        if krt is not None:
            stem = pe.dhatu_entry.clean_text
        elif pe is not None and getattr(pe, "pratipadika", None) is not None:
            stem = pe.pratipadika.text
        else:
            stem = getattr(e, "lemma", key)
        vib = getattr(e, "vibhakti", None)
        stem_lingas = []
        if pe is not None:
            for l in getattr(pe, "lingas", []) or []:
                g = LIN.get(_enum(l))
                if g:
                    stem_lingas.append(g)
        out.append({
            "kind": "subanta", "stem": stem,
            "vibhakti": VIB.get(_enum(vib)) if vib is not None else None,
            "vacana": VAC.get(_enum(getattr(e, "vacana", None))),
            "linga": LIN.get(_enum(getattr(e, "linga", None))),
            "stem_lingas": stem_lingas,
            "krt": str(krt) if krt is not None else None,
            "avyaya": bool(getattr(e, "is_avyaya", False)),
        })
    # gender repair: where the lexicon's form entries contradict the
    # stem's own lexical gender (namanaH listed as masculine though
    # naman is neuter), add the gender-corrected reading; the form of
    # a fixed-gender stem can only carry that gender
    extra = []
    seen = {(c["stem"], c["vibhakti"], c["vacana"], c["linga"])
            for c in out if c["kind"] == "subanta"}
    for c in out:
        if c["kind"] == "subanta" and len(c["stem_lingas"]) == 1 \
                and c["linga"] != c["stem_lingas"][0]:
            key = (c["stem"], c["vibhakti"], c["vacana"],
                   c["stem_lingas"][0])
            if key not in seen:
                seen.add(key)
                fixed = dict(c)
                fixed["linga"] = c["stem_lingas"][0]
                extra.append(fixed)
    return out + extra
