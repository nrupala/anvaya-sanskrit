#!/usr/bin/env python3
"""Ruler (a): a simple rule reader over the gold morphological analysis.

Question it answers: given PERFECT morphology (pada-split, stem class,
vibhakti, vacana, linga, verb person/number/voice) - handed to it from
gold.json, because producing that morphology is a different machine's
job - how many of the 29 gold relations follow by RULE?

Two modes:
  STRICT     - vibhakti->karaka mapping + full agreement + verb-number
               agreement + closed-class lexical rules (nama, ca, iti,
               atha, tatra) + the absolutive form rule. No positional
               information is used at all.
  POSITIONAL - STRICT plus the three positional conventions of anvaya
               practice: a karma belongs to the nearest FOLLOWING
               predicate; a genitive hangs on the nearest following
               substantive; an ambiguous adjective takes its nearest
               agreeing substantive.

A relation counts recovered only if head AND relation kind both match
gold. Every failure prints its reason.
"""
import json, sys

gold = json.load(open("gold.json"))
tokens = {t["id"]: t for t in gold["tokens"]}
gold_rels = {r["dep"]: (r["head"], r["rel"], r["id"]) for r in gold["relations"]}

by_sent = {}
for t in gold["tokens"]:
    by_sent.setdefault(t["sent"], []).append(t)
for s in by_sent:
    # numeric sort on the token number: a plain string sort puts t10
    # before t2 and silently scrambles sentence order (caught by the
    # hand derivation disagreeing with the machine - see FLAW-AUDIT)
    by_sent[s].sort(key=lambda t: int(t["id"].split("t")[1]))

MODE = sys.argv[1] if len(sys.argv) > 1 else "STRICT"
positional = MODE == "POSITIONAL"

pred = {}   # dep_id -> (head_id, rel, rule_that_fired)

for sent, toks in sorted(by_sent.items()):
    root = next(t for t in toks if t["cls"] == "FINVERB")
    idx = {t["id"]: i for i, t in enumerate(toks)}

    def prev_tok(t):
        i = idx[t["id"]]
        return toks[i - 1] if i > 0 else None

    # -- closed-class lexical rules (avyaya) -------------------------------
    nama_flagged = set()
    for t in toks:
        if t["cls"] != "AVYAYA":
            continue
        st = t.get("subtype")
        if st == "nama-marker":
            p = prev_tok(t)
            pred[t["id"]] = (p["id"], "name-marker", "LEX-nama")
            nama_flagged.add(p["id"])
        elif st == "coordinator":
            p = prev_tok(t)
            pred[t["id"]] = (p["id"], "coordinator", "LEX-ca")
        elif st == "iti":
            np_ = next((x for x in toks if x.get("naming_predicate")), None)
            pred[t["id"]] = (np_["id"], "enumeration-closer", "LEX-iti")
        elif st == "discourse":
            pred[t["id"]] = (root["id"], "discourse", "LEX-atha")
        elif st == "locative-adverb":
            pred[t["id"]] = (root["id"], "adhikaraṇa", "LEX-locadv")

    # -- absolutives: the form itself carries the rule (3.4.21) ------------
    for t in toks:
        if t["cls"] == "ABSOL":
            pred[t["id"]] = (root["id"], "prior-action", "FORM-absolutive")

    # -- karta: prathama substantive, not a nama-flagged name, not the
    #    naming predicate, whose vacana matches the finite verb -----------
    karta = None
    for t in toks:
        if t["cls"] in ("NOUN", "PRON") and t.get("vibhakti") == 1 \
                and t["id"] not in nama_flagged \
                and not t.get("naming_predicate") \
                and t.get("vacana") == root.get("vacana"):
            karta = t
            break
    pred[karta["id"]] = (root["id"], "kartā", "CASE1+verb-agreement")

    # -- name apposition: nama-flagged names, and leftover prathama
    #    substantives that cannot be karta, hang on the karta -------------
    for t in toks:
        if t["cls"] in ("NOUN", "PRON") and t.get("vibhakti") == 1 \
                and t["id"] != karta["id"] and not t.get("naming_predicate") \
                and t["id"] not in pred:
            pred[t["id"]] = (karta["id"], "name-apposition", "CASE1-elimination")

    # -- naming predicate (namanah) hangs on the karta ---------------------
    for t in toks:
        if t.get("naming_predicate"):
            pred[t["id"]] = (karta["id"], "name-predicate", "LEX-naman")

    # -- adjectives / numerals: full agreement, unique head ----------------
    substantives = [t for t in toks if t["cls"] in ("NOUN", "PRON")
                    and not t.get("proper")]  # names do not head adjectives
    for t in toks:
        if t["cls"] not in ("ADJ", "NUM"):
            continue
        cands = [s for s in substantives
                 if s.get("vibhakti") == t.get("vibhakti")
                 and s.get("vacana") == t.get("vacana")
                 and s.get("linga") == t.get("linga")]
        if len(cands) == 1:
            pred[t["id"]] = (cands[0]["id"], "viseṣaṇa", "AGREEMENT-unique")
        elif len(cands) > 1 and positional:
            best = min(cands, key=lambda s: abs(idx[s["id"]] - idx[t["id"]]))
            pred[t["id"]] = (best["id"], "viseṣaṇa", "POS-adj-nearest")
        # else: unrecovered in this mode

    # -- remaining substantives: vibhakti -> karaka mapping ----------------
    KARAKA = {3: "karaṇa", 4: "sampradāna", 5: "apādāna", 7: "adhikaraṇa"}
    predicates = [t for t in toks if t["cls"] in ("ABSOL", "FINVERB")]
    for t in toks:
        if t["cls"] not in ("NOUN", "PRON") or t["id"] in pred:
            continue
        v = t.get("vibhakti")
        if v in KARAKA:
            pred[t["id"]] = (root["id"], KARAKA[v], f"CASE{v}-mapping")
        elif v == 2:
            if len(predicates) == 1:
                pred[t["id"]] = (root["id"], "karma", "CASE2-mapping")
            elif positional:
                following = [p for p in predicates if idx[p["id"]] > idx[t["id"]]]
                tgt = min(following, key=lambda p: idx[p["id"]])
                pred[t["id"]] = (tgt["id"], "karma", "POS-karma-next-predicate")
            # else: karma of SOME predicate is certain; the head is not
            # determinable from case alone -> unrecovered
        elif v == 6:
            if positional:
                subs = [s for s in substantives if idx[s["id"]] > idx[t["id"]]]
                tgt = min(subs, key=lambda s: idx[s["id"]])
                pred[t["id"]] = (tgt["id"], "sambandha", "POS-gen-next-substantive")
            # else: sambandha is certain; its head is not in the case

# -- score -------------------------------------------------------------------
ok, lines = 0, []
for dep, (ghead, grel, gid) in sorted(gold_rels.items(), key=lambda kv: kv[1][2]):
    p = pred.get(dep)
    form = tokens[dep]["form"]
    if p and p[0] == ghead and p[1] == grel:
        ok += 1
        lines.append(f"{gid} OK    {form:<28} {grel} -> {tokens[ghead]['form']}  [{p[2]}]")
    else:
        why = "no rule fired" if not p else f"reader said {p[1]} -> {tokens[p[0]]['form']} [{p[2]}]"
        lines.append(f"{gid} MISS  {form:<28} {grel} -> {tokens[ghead]['form']}  ({why})")
print(f"MODE={MODE}  recovered {ok}/{len(gold_rels)} = {100*ok/len(gold_rels):.1f}%")
print("\n".join(lines))
