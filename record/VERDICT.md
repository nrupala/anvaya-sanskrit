# Verdict — Sanskrit in Codetopo, measured

**Spike, 2026-11-19.** Source: Pañcatantra, Kathāmukha, the four
opening narrative sentences (SOURCE.md). Gold: 29 relations derived
by hand from the grammar (GOLD.md). Rulers: (a) a deterministic rule
reader over the morphological analysis; (b) Stanza 1.15.1
`vedic_nocharlm`, end to end on the printed text. Graph: 38 nodes,
64 edges, restored into a database by Codetopo itself and queried
through its own surface (graph.db, query-output.txt, render-*.svg).
No repo changes; this is a spike.

## The head-to-head, on the same bar as English

| | Relations recovered | Character of the failures |
|---|---|---|
| English, spaCy end to end (raw text in) | 119/137 = **86.9%** | meaning inversions: a parenthetical destroys S4's subject, the main verb is demoted to an adjective |
| Sanskrit (a), rules over given morphology, position forbidden | 25/29 = **86.2%** | no type ever wrong, nothing inverted: 4 heads under-determined, each type certain |
| Sanskrit (a), rules + the anvaya positional conventions | 29/29 = **100%** | — |
| Sanskrit (b), Stanza Vedic end to end (raw text in) | 6/29 = **20.7%** (2/29 strict) | sandhi fusions erase 10 relations; roots crowned from adjectives and adverbs; the subject edge inverted |

The two 86% numbers look like a tie and are not. English's 86.9% is
the best machine reading obtainable, bought with a statistical model
trained on millions of words, and its misses corrupt meaning.
Sanskrit's 86.2% is what a small rule reader with NO statistics
and NO word order achieves from the endings alone — and its misses
corrupt nothing; they are four places where the case tells you the
relation's kind and leaves the head to a convention. Allow the
conventions every commentary already uses and the same reader is
flawless on this text. The information content of the two languages'
surfaces is measurably different, and it is different in the
direction the Director said it would be.

## Why: the relations are worn on the words

The Director's framing for English was noun / verb / action —
subject, object, predicate. Sanskrit has that triad and more: six
kāraka slots (agent, object, means, recipient, source, locus) plus
the genitive's relation, and each is marked on the word itself by
its vibhakti. That is why the STRICT reader never consults word
order and never misses a type: kartā is the prathamā word the verb's
own ending agrees with; karma is dvitīyā; the locus is saptamī; an
adjective finds its noun by matching case, number and gender; the
absolutive's very form (3.4.21) promises "same agent, earlier act".
Free word order costs this reader nothing, because the order was
never carrying the information — the endings were. English puts the
same information in position and intonation of phrasing, which is
why English needs a statistical reader and Sanskrit, in principle,
does not.

## The three-way verdict on the Director's hypothesis

**True about the language — measured, not admired.** On this text,
Sanskrit's grammatical relations are recoverable from morphology by
rule to a degree English's are not recoverable by any means we have:
the case system does carry the relations, the agreement system does
disambiguate the qualifiers, and the residue is four head-choices,
not a fog.

**Not yet true about the tools — also measured.** The one
statistical parser that could be obtained here is trained on Vedic
Sanskrit and scores 20.7% on classical prose; a third of the
relations die at tokenization, before parsing, because nothing in
the pipeline splits sandhi. Pointing today's off-the-shelf ruler at
Sanskrit gives a worse graph than pointing spaCy at English, and
the graph would lie with confidence (a vocative verb, an imperative
adverb) if its numbers were not printed beside it.

**And one limit on the claim itself:** N = 29, one passage, one
genre; karaṇa, sampradāna and apādāna never occur in it; and ruler
(a) was handed perfect morphology by hand. The verdict is about
where the information lives in Sanskrit. It is not yet a claim
about a finished machine, and this spike does not make it one.

## What a sanskrit profile would need — and why it could beat English's bar

English's ground floor is statistics all the way down; its accuracy
is whatever the model happens to score, printed on the profile's
face. Sanskrit offers a different build, every piece of it a known
craft rather than a hope:

1. **A sandhi segmenter in front.** This is the profile's true
   front door — the piece whose accuracy must be measured and
   printed on the profile's face, exactly as spaCy's 86.9% is
   printed on English's. Rule-based segmenters exist (the Sanskrit
   Heritage platform; the Digital Corpus of Sanskrit ecosystem);
   this spike did not test them, and names them as the next
   measurement rather than assuming them.
2. **A morphological analyzer** producing vibhakti, vacana, liṅga
   per word (the same Heritage/DCS class of tool). Given that
   output, **the extractor is ruler (a) itself** — deterministic,
   auditable, no model. The projected ground floor, IF the front
   end delivers morphology of the quality the gold used, sits above
   English's 86.9%, and its residual errors would be head-choice
   ambiguities rather than inversions. That sentence is a
   projection and is labelled as one.
3. **Samāsa analysis for depth.** At sentence level the compounds
   behaved as single adjectives and cost nothing; a profile that
   wants the INSIDE of सकलार्थिसार्थकल्पद्रुमः needs compound
   analysis, a further rule craft of the same tradition.
4. **The same two-storey honesty as English:** ground floor
   inference-class with the front end's measured accuracy on its
   face; coreference and essence above it as CLAIM edges with the
   reader named. Nothing about Sanskrit exempts it from the label
   discipline — its ground floor is stronger, its upper floor is
   the same interpretation as any language's.

## What Codetopo presents, today, from this graph

- **The query surface is the strong presentation, as with
  English.** `symbol` on राजा returns the king whole: his three
  compound qualifiers, his name in apposition, his verb, and S3's
  "his" pointing back at him across the sentence boundary. `rank`
  by fan-in puts **पुत्राः, the sons, first (7) and राजा second
  (5)** — the passage's two centres, measured; and it is the sons
  the whole book exists for, so the measurement and the meaning
  agree. The graph's holes are visible in the same surface:
  सचिवान्, the ministers, hang by containment alone — neither ruler
  could attach their summoning, and the graph says so by silence
  rather than inventing an edge.
- **The picture is not presentable, for two named reasons.** The
  full render is the same flat ribbon the English spike recorded
  (the structure scope draws the containment skeleton only, this
  graph having restored under the code profile, as the English one
  did). And the Devanagari labels draw as empty boxes in the
  SVG pipeline — the renderer's fonts carry no देवनागरी. A Sanskrit
  profile owes a font fix English never needed.

## The closing line

The Director said Sanskrit is logical, grammatical, deep — "but
only Codetopo can establish the truth." Codetopo's answer, from
measurement: the depth is real and it is located in the endings;
a ruler made of the language's own rules reads this text without a
single corrupted relation; the rulers currently on the shelf are
not worthy of the language yet. The doctrine survives intact and is
in fact sharpened by Sanskrit: **the agent thinks, the engine
measures** — and Sanskrit is the language that lets the engine
measure with rules where English forces it to measure with
statistics.

## Record

`SOURCE.md` (the passage, edition, sandhi inventory) · `GOLD.md` /
`gold.json` (the hand derivation, every mapping cited to its
Pāṇinian rule) · `rule_reader.py` / `rule-out-a.txt` /
`rule-out-b.txt` (ruler (a), both modes, per-relation output) ·
`parse_sa.py` / `parse-sa.json` / `parse-readable.txt` /
`parse-sa.log` (ruler (b), raw and readable) · `build_graph.py` /
`graph.json` / `graph.db` (the snapshot, restored by Codetopo) ·
`render-full.*`, `render-structure.*` (Codetopo's own renders) ·
`query-output.txt` (Codetopo answering questions about the passage)
· `flaw_audit.py` / `flaw-audit-counts.txt` / `FLAW-AUDIT.md`
(every miss, each with its reason).
