#!/usr/bin/env python3
"""DP sandhi segmenter: one orthographic span (SLP1, no spaces) -> padas.

The segmenter is a rule machine, not a model. It searches over split
points; at each boundary it UNDOES one external-sandhi join from a
finite rule table (the joins of the tradition: visarga, nasal
assimilation, guna/dirgha/glide vowel joins, avagraha elision). A
piece is valid only if its citation form is attested by the analyzer
(the vidyut kosha) as an inflected form, or matches a regular
inflection-ending pattern (the fallback for unlisted compounds and
names). The segmenter returns the K best segmentations under a plain
ranking (fewest pieces, then fewest pattern fallbacks); the rule
reader downstream judges which candidate yields a complete reading.

Citation forms ("keys") follow the kosha's convention: a final
visarga is written 's' (surface putrAH -> key 'putras').
"""
from vidyut import kosha as _vk

VOWELS = set("aAiIuUfeEoO")
VOICED = set("gGjJqQdDnbBmMNRYrlvhy")
END = "<END>"
MAXPIECE = 64

_kosha = None


def kosha(path):
    global _kosha
    if _kosha is None:
        _kosha = _vk.Kosha(path)
    return _kosha


_cache = {}


def entries(key, path):
    ck = (path, key)
    if ck not in _cache:
        _cache[ck] = kosha(path).get(key) or []
    return _cache[ck]


def _inflected(e):
    """An entry that makes its key an inflected pada form (not merely
    a stem): a verb form, an indeclinable, or a nominal in a real case.
    The kosha enters bare stems with sambodhana (vocative) entries
    only; those keys are compound members, not padas."""
    if getattr(e, "lakara", None) is not None:
        return True
    if getattr(e, "is_avyaya", False):
        return True
    vib = getattr(e, "vibhakti", None)
    return vib is not None and str(vib) != "samboDanam"


def in_kosha(key, path):
    return any(_inflected(e) for e in entries(key, path))


def is_avyaya(key, path):
    return any(getattr(e, "is_avyaya", False) for e in entries(key, path))


# ---------------------------------------------------------------- patterns
# Fallback inflection patterns for citation keys the kosha does not
# list (long compounds, coined names). Each returns candidate analyses
# as (stem, vibhakti, vacana, linga) with linga a set of options.
def pattern_candidates(key):
    out = []
    if len(key) < 3 or "'" in key:
        # An avagraha inside a key is an elided pada boundary by
        # definition; no single pada contains one.
        return out
    if key.endswith("as"):
        # -aH : a-stem nom sg masc (stem ends in 'a')
        stem = key[:-1]
        if stem.endswith("a"):
            out.append((stem, 1, "sg", {"m"}))
    if key.endswith("is"):
        stem = key[:-1]
        if stem.endswith("i"):
            out.append((stem, 1, "sg", {"m", "f"}))
    if key.endswith("us"):
        stem = key[:-1]
        if stem.endswith("u"):
            out.append((stem, 1, "sg", {"m", "f"}))
    if key.endswith("As"):
        stem = key[:-1]
        if stem.endswith("a"):
            out.append((stem, 1, "pl", {"m"}))
    if key.endswith("am"):
        stem = key[:-1]
        out.append((stem, 1, "sg", {"n"}))
        out.append((stem, 2, "sg", {"n", "m"}))
    if key.endswith("An"):
        stem = key[:-1]
        out.append((stem, 2, "pl", {"m"}))
    if key.endswith("e"):
        stem = key[:-1]
        out.append((stem, 7, "sg", {"m", "n"}))
    if key.endswith("I") and len(key) >= 4:
        # n-stem nominative singular (svAmin -> svAmI); feminine
        # I-stem nominative (nadI)
        out.append((key + "n", 1, "sg", {"m"}))
        out.append((key, 1, "sg", {"f"}))
    if key.endswith("At") and len(key) >= 4:
        # a-stem ablative singular (dUra -> dUrAt)
        out.append((key[:-2] + "a", 5, "sg", {"m", "n"}))
    return out


# Two-letter padas that are real words (the closed class). Shorter
# kosha keys are FST stem fragments, not forms.
CLOSED2 = {"ca", "tu", "hi", "nu", "no", "vA", "mA", "ha", "sa", "sA",
           "te", "me"}


def has_fused_site(key, path):
    """A pattern key with an internal sandhi site whose right-hand
    side is itself a valid pada is two padas fused, not one word.
    Sites checked: the visarga products -ir-/-ur- before a vowel
    (Saktir-ugra, Saktir-ananta). Long-vowel stems (pAraNgata) are
    not sites."""
    for i in range(1, len(key) - 2):
        if key[i] in "iu" and key[i + 1] == "r" and key[i + 2] in VOWELS:
            right = key[i + 2:]
            if validate(right, path) is not None:
                return True
    return False


def validate(key, path):
    """-> 'kosha' | 'pattern' | None"""
    if (len(key) >= 3 or key in CLOSED2) and in_kosha(key, path):
        return "kosha"
    if (pattern_candidates(key)
            or (key.endswith("cit") and len(key) >= 5)) \
            and not has_fused_site(key, path):
        return "pattern"
    return None


# ---------------------------------------------------------------- undo rules
def keyform(surface):
    """Citation key for a pause-form surface piece."""
    if surface.endswith("H"):
        return surface[:-1] + "s"
    return surface


def undos(chunk, nxt):
    """Yield (key, required_next, merged_next) for one surface chunk.

    nxt is the surface char following the chunk, or None at span end.
    required_next is the initial sound the NEXT citation must have
    (END if the span must close here); merged_next says that initial's
    surface was already absorbed into this chunk (vowel joins).
    """
    # R0: pause / identity join
    if nxt is None:
        yield (keyform(chunk), END, False)
    else:
        yield (keyform(chunk), nxt, False)
    if nxt is None:
        return
    # R1: -o before a voiced sound or a vowel other than a-  <- -aH
    if chunk.endswith("o") and (nxt in VOICED or (nxt in VOWELS and nxt != "a")):
        yield (chunk[:-1] + "as", nxt, False)
    # R2: -o' + a-  (avagraha: the a- is elided)
    if chunk.endswith("o'"):
        yield (chunk[:-2] + "as", "a", True)
    # R3: -r before a voiced sound or vowel  <- -iH/-uH/-aH
    if chunk.endswith("r") and (nxt in VOICED or nxt in VOWELS):
        yield (chunk[:-1] + "s", nxt, False)
    # R4: sibilant assimilation of visarga
    if chunk.endswith("S") and nxt in "cC":
        yield (chunk[:-1] + "s", nxt, False)
    if chunk.endswith("z") and nxt in "wW":
        yield (chunk[:-1] + "s", nxt, False)
    # R5: nasal assimilation at the join (citation ends -n or -m)
    if chunk[-1] in "YRMnm" and nxt not in VOWELS:
        for repl in ("n", "m"):
            yield (chunk[:-1] + repl, nxt, False)
    # R6: vowel joins — the next citation's initial is absorbed
    if chunk.endswith("e"):
        yield (chunk[:-1] + "a", "i", True)
    if chunk.endswith("o"):
        yield (chunk[:-1] + "a", "u", True)
    if chunk.endswith("E"):
        yield (chunk[:-1] + "a", "e", True)
    if chunk.endswith("O"):
        yield (chunk[:-1] + "a", "o", True)
    if chunk.endswith("A"):
        for a in ("a", "A"):
            for b in ("a", "A"):
                yield (chunk[:-1] + a, b, True)
    if chunk.endswith("I"):
        for a in ("i", "I"):
            for b in ("i", "I"):
                yield (chunk[:-1] + a, b, True)
    if chunk.endswith("U"):
        for a in ("u", "U"):
            for b in ("u", "U"):
                yield (chunk[:-1] + a, b, True)
    if chunk.endswith("ar"):
        yield (chunk[:-2] + "a", "f", True)
    # R7: glides — the next vowel surfaces intact after the glide
    if nxt in VOWELS:
        if chunk.endswith("y"):
            yield (chunk[:-1] + "i", nxt, False)
        if chunk.endswith("v"):
            yield (chunk[:-1] + "u", nxt, False)
        if chunk.endswith("ay"):
            yield (chunk[:-2] + "e", nxt, False)
        if chunk.endswith("av"):
            yield (chunk[:-2] + "o", nxt, False)
    # R8: -aH before a vowel surfaces as bare -a (visarga elided);
    # the plural -AH likewise surfaces as bare -A
    if chunk.endswith("a") and nxt in VOWELS:
        yield (chunk + "s", nxt, False)
    if chunk.endswith("A") and nxt in VOWELS:
        yield (chunk + "s", nxt, False)
    # R9: final stop voicing — a citation-final voiceless stop
    # surfaces voiced before a voiced sound (tat + vanam -> tadvanam,
    # durat + eva -> duradeva)
    VOICING = {"g": "k", "j": "c", "q": "w", "d": "t", "b": "p"}
    if chunk[-1] in VOICING and (nxt in VOICED or nxt in VOWELS):
        yield (chunk[:-1] + VOICING[chunk[-1]], nxt, False)
    # R10: t + s -> cch (tat + sruta -> tacchruta): the left stop
    # surfaces as c, and the next citation's initial is S though its
    # surface will be C. The plain palatal case is t + c -> cc
    # (tat + ca -> tacca) and t + j -> jj.
    if chunk.endswith("c") and nxt == "C":
        yield (chunk[:-1] + "t", "S", False)
    if chunk.endswith("c") and nxt == "c":
        yield (chunk[:-1] + "t", "c", False)
    if chunk.endswith("j") and nxt == "J":
        yield (chunk[:-1] + "t", "J", False)
    if chunk.endswith("j") and nxt == "j":
        yield (chunk[:-1] + "t", "j", False)


# ---------------------------------------------------------------- DP
def segment_span(text, path, boundaries=frozenset()):
    """Segment one span -> up to K candidate segmentations."""
    return _segment_span(text, path, boundaries)


def _segment_span(text, path, boundaries=frozenset(), valid=None,
                  minpiece=2):
    """boundaries: positions in text where a printed space stood — a
    piece may end there but never cross one. The join at a boundary
    still undoes against the following span's first char."""
    n = len(text)
    # state: (pos, required, merged) -> up to K best (cost, pieces).
    # Every transition strictly increases pos, so sweeping pos in
    # order is exact. Cost is (pieces, pattern fallbacks): the plain
    # segmentation ranking. Choosing among the K best segmentations
    # is the reader's job downstream, not the segmenter's.
    K = 48
    best = {(0, None, False): [((0, 0), [])]}
    for pos in range(0, n):
        states = [s for s in list(best) if s[0] == pos]
        for state in states:
            _, required, merged = state
            for cost, pieces in list(best[state]):
                for j in range(pos + minpiece,
                               min(n, pos + MAXPIECE) + 1):
                    if any(pos < b < j for b in boundaries):
                        break
                    chunk = text[pos:j]
                    nxt = text[j] if j < n else None
                    if not merged and required is not None \
                            and chunk[0] != required \
                            and not (required == "S" and chunk[0] == "C") \
                            and not (required == "J" and chunk[0] == "j"):
                        continue
                    for key0, req, mrg in undos(chunk, nxt):
                        key = (required + key0) if merged else key0
                        if "'" in key:
                            # an avagraha inside a piece is an elided
                            # pada boundary, whatever the source
                            continue
                        if not merged and required == "S" \
                                and key[0] == "C":
                            key = "S" + key[1:]
                        if not merged and required == "J" \
                                and key[0] == "j":
                            key = "J" + key[1:]
                        if not merged and required is not None \
                                and key[0] != required:
                            continue
                        src = (valid or validate)(key, path)
                        if src is None:
                            continue
                        ncost = (cost[0] + 1,
                                 cost[1] + (1 if src == "pattern" else 0))
                        if req == END:
                            if j != n:
                                continue
                            nstate = (n, END, False)
                        else:
                            nstate = (j, req, mrg)
                        cand = best.setdefault(nstate, [])
                        cand.append((ncost, pieces + [(key, src)]))
                        cand.sort(key=lambda cp: cp[0])
                        seen = set()
                        keep = []
                        for c in cand:
                            sig = tuple(k for k, _ in c[1])
                            if sig not in seen:
                                seen.add(sig)
                                keep.append(c)
                        best[nstate] = keep[:K]
    return [pieces for _, pieces in best.get((n, END, False), [])]


def segment_sentence(slp1_text, path):
    """Segment a full sentence -> up to K candidate segmentations,
    best first. Printed spaces are pada boundaries, but sandhi joins
    across them are undone like any other join."""
    spans = [s.strip(".|।॥") for s in slp1_text.split()]
    spans = [s for s in spans if s]
    text = "".join(spans)
    bounds = set()
    acc = 0
    for s in spans[:-1]:
        acc += len(s)
        bounds.add(acc)
    return segment_span(text, path, frozenset(bounds))
