# Sanskrit Profile — Status (started 2026-11-19)

Director's standing order: "Let's do Sanskrit then" (2026-11-19). The spike
(SANSKRIT-SPIKE-2026-11-19) carries it: verdict TRUE about the language, NOT
YET about the tools. The profile's extractor is therefore NOT a statistical
parser: it is a front end (sandhi segmentation → morphological analysis)
feeding the spike's preserved rule reader (rule_reader.py).

Spike numbers carried in: gold = 29 relations (Pañcatantra, Kathāmukha);
rule reader over gold morphology, no-position mode 25/29 = 86.2%, anvaya
mode 29/29 = 100%; Stanza vedic end-to-end 6/29. English profile's published
bar: 86.9% (PR #171, merge 3158760b).

## STAGE 1 — THE GATE (in progress)

Candidates probed 2026-11-19 (evidence in probe_*.py + this file):
- **vidyut 0.4.0** (Ambuda; code MIT; data zip pinned: releases/download/
  py-0.4.0/data-0.4.0.zip, 78 MB) — OBTAINED, runs in the sandbox.
  - Chedaka (its statistical segmenter): REJECTED as the chain's segmenter —
    returns whole hard spans unsegmented (all three sandhi chains +
    the giant compound), mis-splits तत्र → तत्+र, and picks wrong single
    analyses (राजा → rāj, tṛtīyā). It is also a Markov model; the verdict's
    design wants rules.
  - **Kosha (its lexicon): ADOPTED as the analyzer.** Candidate sets are
    rich and carry what the reader needs: stems (Basic pratipadika /
    Krdanta dhātu + prefixes + kṛt), vibhakti, vacana, liṅga, puruṣa,
    lakāra. The absolutives are present as Krdanta entries with
    krt=ktvā (आलोक्य, आहूय both). राजा's correct rājan/praTamā/eka entry
    sits among its 23 candidates — disambiguation is the adapter's job.
    Kosha keys are citation forms with final visarga written 's'
    (putrAH → key 'putras'). Coverage of the fixture's 33 padas: all but
    वहुशक्तिः (edition variant; बहुशक्ति in other editions) and the two
    long compounds — those three fall to the ending-pattern fallback.
    Data provenance: kosha built from the Digital Corpus of Sanskrit +
    the sanskrit/data lexicon (licences named in the accuracy doc).
- **sanskrit_parser 0.2.6** (MIT, Heritage-derived forms DB): REJECTED —
  its forms DB has holes exactly at need (बभूवुः, आलोक्य, प्रोवाच,
  वहुशक्तिः all unlisted; visarga-final forms keyed under 's'), and its
  chain splits are wrong on 2 of 3 chains.
- **Chain design (all deterministic, every stage named in method stamps):**
  lipi transliteration (vidyut) → house DP sandhi segmenter (rules of the
  tradition; pieces validated against the kosha, ending-pattern fallback
  for unlisted compounds/names) → kosha candidate analyses → adapter
  (closed classes, absolutive/naming/proper flags, adjective conventions,
  candidate disambiguation by the sentence's own agreement) → the spike's
  rule_reader.py, anvaya mode, its rule names stamped on every edge.

- [x] Front-end candidate obtained + licence named + version pinned (vidyut 0.4.0)
- [x] Chain measured end-to-end on the fixture passage (raw printed text in)
- [x] Held-out passage hand-golded (different text, cited rules) + chain scored
- [x] GATE DECISION recorded here before any Stage 2 work

Gate: fixture end-to-end ≥ 86.9% AND a held-out score printable without
embarrassment. Fail → name back with evidence, preserve everything, NO PR.

## GATE DECISION (2026-11-20) — NAMED BACK, NO PR

**Fixture (spike passage, raw printed text, end-to-end): PASS.**
- STRICT (no position): 23/29 = 79.3% recovered, 0 structural misses.
- POSITIONAL (anvaya, the shipped reader mode): **29/29 = 100%**, 0
  structural misses. All four sentences segmented exactly as the
  hand gold; the front end loses nothing the anvaya conventions repair.
- Against hand-golded morphology the reader itself scores 25/29 strict:
  the chain's strict number is 2 lower (its candidate fixing differs
  from the hand derivation on two relations, both repaired positionally).
- Chain's own tests pass: segmenter pool carries the gold segmentation
  4/4 sentences; adapter over gold segmentations reproduces 29/29
  positional (chain/test_segment.py, chain/test_adapter.py).

**Held-out (Pañcatantra, Mitrabheda — different text, 38 relations
hand-golded with cited rules, chain/GOLD-HELDOUT.md): FAIL.**
- STRICT 10/38 = 26.3%; POSITIONAL **11/38 = 28.9%**; 4 structural
  misses (h14 gatvā, h15 tam, h16 sārthavāham — the H2 fusions; h33
  dūrāt — gender of the pattern ablative).
- A judge variant trading pattern-fragments differently reached
  15/38 = 39.5% positional here but cost the fixture (26/29, one
  structural miss) — no configuration found is strong on both.
- 28.9–39.5% on unseen text is not printable without embarrassment
  beside the English profile's 86.9%. The gate's second leg fails.

**Why (the measured flaw classes, all evidenced in chain/):**
1. **The kosha cannot separate fragments from forms.** Its form
   inventory lists fragment keys (pin, kad, dUr, smat, miTi) with
   real-looking case bundles alongside genuine padas, and no
   entry-level test distinguishes them. On unseen text the
   segmenter+judge cannot reliably refuse a shattered reading
   (piṅgalakaḥ → pin + galakaḥ; dūrādeva → dUr + ādevā) whose
   fragments the reader then relates as phantom substantives.
2. **Homonym and gender noise in candidate sets.** A form's
   candidates include other lexemes' analyses (sañjīvakam as a
   neuter (1,sg); dūrāt as a (1,sg,m) nominative; tān under stem
   'ta'). The adapter's agreement fixing disposes correctly when
   anchors are unambiguous (the fixture) and is pulled by
   self-reinforcing clusters on unseen text (the (2,sg,m) pull in
   H2/H4). Role economy (a second nominative must agree with the
   kartā) and gender repair fixed part of this, not all.
3. **Fusion vs compound is not decidable from the lexicon.**
   tat + vanam (two padas) and vahu + śaktis (one name) present
   identically as kosha+kosha splits; gatvā + anyedyuḥ + tam fuses
   into one pattern-shaped key. Rules that reject fusions also
   reject lexicalized words (kadācit = kadā + cit is one lexeme) —
   each anti-fusion rule tried broke a genuine word, and each
   anti-shattering rule broke a genuine fusion or a short word
   (rājā, tān are four and three letters).
4. What DID generalize: absolutive chains (3/3 in H2), the name
   device on new names (H1, H4), absolutive/avyaya recognition via
   the lexicon's indeclinable flag, the -cit avyaya supplement
   (kadācit), the ablative ending supplement (dūrāt's case, though
   not its gender), sampradāna (H5 arthāgamāya) and apādāna (H4)
   where segmentation held. Kāraka coverage across both passages:
   kartā, karma, adhikaraṇa, sambandha, apādāna, sampradāna.
   **karaṇa (tṛtīyā) remains unmeasured by either passage** — the
   one rich instrumental sentence available turns on oblique-case
   apposition, outside the reader's grammar; named in
   chain/GOLD-HELDOUT.md rather than silently skipped.

**Verdict:** the spike's finding is re-proven one level down — TRUE
about the language, NOT YET about the tools. The rule reader over
correct morphology is exact (29/29 anvaya on the fixture, both by
hand and through this front end); the obtainable front end
(vidyut kosha 0.4.0, MIT) cannot yet produce that morphology
reliably on text it has not seen. Per the brief, this is a success
of the process: **Stage 2 does not run, no repo PR is opened.**
Everything is preserved here: the chain (chain/), both golds
(spike gold.json + chain/heldout-gold.json with GOLD-HELDOUT.md),
the scorer (chain/score_chain.py — bundle+ordinal pairing,
structural misses counted before the reader runs), and the probe
record. Revisit condition: a Sanskrit morphological analyzer whose
form inventory marks stem-fragments as such (or a Heritage-class
analyzer that runs in this sandbox), or a kosha edition with
per-entry reliability marks — re-run chain/score_chain.py on both
passages; the gate stands at fixture ≥86.9% anvaya (already met)
AND held-out printable (≥ the English bar's neighbourhood).

Licence note: vidyut code MIT (repo Cargo.toml + README, verified).
Kosha data is built from the Digital Corpus of Sanskrit and the
sanskrit/data lexicon; their licences were NOT independently
re-verified from their own repos in this run — nothing shipped, so
no licence was relied on; the check is owed before any future use
of the data in a shipped artifact.

## STAGE 2 — THE BUILD (only through the gate) — DID NOT RUN

The gate's held-out leg failed (see GATE DECISION above). No repo
work was started; the boxes below stand as the preserved build plan
for the day the front end clears the gate.

- [ ] profiles/sanskrit.profile.json embedded beside english
- [ ] tools/sanskrit-ingest companion (pinned chain, Devanagari only)
- [ ] Render: sanskrit clustered layout + general non-Latin font fix, glyphs verified visually
- [ ] Fixture + docs/sanskrit-accuracy.md (both scores) + docs at par
- [ ] Full suites green, PR via gh.sh, merge on green CI, read back from main

Standing lines: Release gate NOT RUN · Guardian Mesh NOT RUN.
OpenSSF floor: codetopo 15421 Passing — no compliance artifacts touched.
