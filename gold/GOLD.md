# Gold derivation — SANSKRIT-SPIKE-2026-11-19

The gold standard is derived BY HAND from the grammar, word by word.
Each content word gets: stem, vibhakti (case), vacana (number), liṅga
(gender) where the form carries them, and its relation to its head.
The relation set is dependency-shaped, exactly as the English audit
was: every token except the finite verb (the root) carries exactly
one relation to a head. **N = 29 relations** (S1: 5, S2: 7, S3: 10,
S4: 7).

## The case→relation mapping, with its authority

The kāraka mapping is Pāṇini's, cited so any reader can check the
gold rather than trust it:

| Relation | Definition | Vibhakti rule |
|---|---|---|
| kartā (agent) | 1.4.54 स्वतन्त्रः कर्ता — the independent one | prathamā with an active verb (2.3.46) |
| karma (object) | 1.4.49 कर्तुरीप्सिततमं कर्म — what the agent most seeks to reach | dvitīyā (2.3.2 कर्मणि द्वितीया) |
| karaṇa (means) | 1.4.42 साधकतमं करणम् | tṛtīyā (2.3.18) — *not present in this passage* |
| sampradāna (recipient) | 1.4.32 कर्मणा यमभिप्रैति स सम्प्रदानम् | caturthī (2.3.13) — *not present* |
| apādāna (source) | 1.4.24 ध्रुवमपायेऽपादानम् | pañcamī (2.3.28) — *not present* |
| adhikaraṇa (locus) | 1.4.45 आधारोऽधिकरणम् — the support/locus | saptamī (2.3.36 सप्तम्यधिकरणे च) |
| sambandha (relation/possession) | the residual relation | ṣaṣṭhī (2.3.50 षष्ठी शेषे) |
| prior action, same agent | absolutive (ktvā/lyap) | 3.4.21 समानकर्तृकयोः पूर्वकाले |
| viśeṣaṇa (qualifier) | adjective in sāmānādhikaraṇya — same vibhakti, vacana and liṅga as its substantive | agreement |
| name apposition | a proper name in prathamā standing in sāmānādhikaraṇya with a common noun, flagged by the avyaya नाम | agreement + नाम |

## S1 — अस्ति दाक्षिणात्ये जनपदे महिलारोप्यं नाम नगरम्

| # | Word | Analysis | Relation |
|---|---|---|---|
| 1 | अस्ति | धातु अस्, laṭ, 3rd sg., active — ROOT | — |
| 2 | दाक्षिणात्ये | adjective (taddhita from दक्षिणा), neut., saptamī, sg. | **viśeṣaṇa → जनपदे** (agreement: saptamī sg. neut.) |
| 3 | जनपदे | noun जनपद, neut., saptamī, sg. | **adhikaraṇa → अस्ति** (the locus in which the city exists; 1.4.45) |
| 4 | महिलारोप्यम् | proper noun, neut., prathamā, sg. | **name-apposition → नगरम्** (sāmānādhikaraṇya, flagged by नाम) |
| 5 | नाम | avyaya, naming particle | **name-marker → महिलारोप्यम्** |
| 6 | नगरम् | noun नगर, neut., prathamā, sg. | **kartā → अस्ति** (the existent; with अस् the thing that is stands as kartā) |

S1 relations: 5.

## S2 — तत्र … राजा बभूव

| # | Word | Analysis | Relation |
|---|---|---|---|
| 1 | तत्र | avyaya, locative adverb (frozen saptamī of तद्) | **adhikaraṇa → बभूव** (place: "there") |
| 2 | सकलार्थिसार्थकल्पद्रुमः | bahuvrīhi compound, one pada ("a wish-tree for every company of seekers"), masc., prathamā, sg. | **viśeṣaṇa → राजा** |
| 3 | प्रवरमुकुटमणिमरीचिमञ्जरीचर्चितचरणयुगलः | bahuvrīhi compound, one pada ("whose foot-pair is honoured by the ray-clusters of the crest-jewels of the foremost kings"), masc., prathamā, sg. | **viśeṣaṇa → राजा** |
| 4 | सकलकलापारङ्गतः | tatpuruṣa ("gone to the far shore of all the arts"), masc., prathamā, sg. | **viśeṣaṇa → राजा** |
| 5 | अमरशक्तिः | proper noun, masc., prathamā, sg. | **name-apposition → राजा** (flagged by नाम) |
| 6 | नाम | avyaya | **name-marker → अमरशक्तिः** |
| 7 | राजा | noun राजन्, masc., prathamā, sg. | **kartā → बभूव** (verb is 3rd sg.; agreement) |
| 8 | बभूव | धातु भू, liṭ, 3rd sg., active — ROOT | — |

S2 relations: 7. Note for the audit: words 2–4 are adjectives of राजा,
NOT of अमरशक्तिः, though अमरशक्तिः matches them in case, number and
gender — the commentary tradition (Abhinavarājalakṣmī ṭīkā ad loc.)
glosses all three as the king's qualities. What saves the rule reader
is the नाम flag: a name in apposition does not head adjectives; the
common noun it names does.

## S3 — तस्य त्रयः पुत्राः … बभूवुः

| # | Word | Analysis | Relation |
|---|---|---|---|
| 1 | तस्य | pronoun तद्, masc., ṣaṣṭhī, sg. | **sambandha → पुत्राः** ("his sons"; 2.3.50) |
| 2 | त्रयः | numeral त्रि, masc., prathamā, pl. | **viśeṣaṇa → पुत्राः** (agreement) |
| 3 | पुत्राः | noun पुत्र, masc., prathamā, pl. | **kartā → बभूवुः** (verb is 3rd pl.; agreement) |
| 4 | परमदुर्मेधसः | bahuvrīhi adjective ("whose wit is utterly dull"), masc., prathamā, pl. (the -aḥ plural is the masculine form; a neuter plural would end -आंसि, so gender is on the word) | **viśeṣaṇa → पुत्राः** |
| 5 | वहुशक्तिः | proper noun, masc., prathamā, sg. | **name-apposition → पुत्राः** |
| 6 | उग्रशक्तिः | proper noun, masc., prathamā, sg. | **name-apposition → पुत्राः** |
| 7 | अनन्तशक्तिः | proper noun, masc., prathamā, sg. | **name-apposition → पुत्राः** |
| 8 | च | avyaya, coordinator (enclitic, stands after the last conjunct in this chain) | **coordinator → अनन्तशक्तिः** |
| 9 | इति | avyaya, closes the naming enumeration | **enumeration-closer → नामानः** |
| 10 | नामानः | noun नामन्, neut., prathamā, pl., used as the naming predicate ("named") | **name-predicate → पुत्राः** |
| 11 | बभूवुः | धातु भू, liṭ, 3rd pl., active — ROOT | — |

S3 relations: 10. The kartā is fixed by the verb's plural ending:
बभूवुः can only take पुत्राः. The three singular names, unable to be
kartā, fall to apposition by elimination — a rule, not a reading.
नामानः is the plural counterpart of the नाम device in S1/S2.

## S4 — अथ राजा तान् शास्त्रविमुखान् आलोक्य सचिवान् आहूय प्रोवाच

| # | Word | Analysis | Relation |
|---|---|---|---|
| 1 | अथ | avyaya, sequence particle ("then") | **discourse → प्रोवाच** |
| 2 | राजा | noun राजन्, masc., prathamā, sg. | **kartā → प्रोवाच** |
| 3 | तान् | pronoun तद्, masc., dvitīyā, pl. ("them" — the sons) | **karma → आलोक्य** (he saw THEM; 1.4.49) |
| 4 | शास्त्रविमुखान् | bahuvrīhi adjective ("face turned from learning"), masc., dvitīyā, pl. | **viśeṣaṇa → तान्** (agreement) |
| 5 | आलोक्य | absolutive, आ + लोक् with lyap ("having seen") | **prior-action → प्रोवाच** (3.4.21: same kartā, earlier act) |
| 6 | सचिवान् | noun सचिव, masc., dvitīyā, pl. | **karma → आहूय** (he summoned the ministers) |
| 7 | आहूय | absolutive, आ + ह्वे with lyap ("having summoned") | **prior-action → प्रोवाच** |
| 8 | प्रोवाच | धातु प्र + वच्, liṭ, 3rd sg., active — ROOT ("said") | — |

S4 relations: 7. The two dvitīyā words belong to two different
predicates: तान् to आलोक्य, सचिवान् to आहूय. Case alone says "karma"
for both; WHICH predicate governs each is the audit's key question.

## Gold totals

**N = 29 relations.** By kind: kartā 4 · karma 2 · adhikaraṇa 2 ·
sambandha 1 · viśeṣaṇa 6 · name-apposition 5 · name-marker 2 ·
name-predicate 1 · prior-action 2 · coordinator 1 ·
enumeration-closer 1 · discourse 1 · (plus S1's name-apposition
counted in the 5). Convention-flagged relations — where the gold
rests on annotation convention for particles rather than on case:
च (g19), इति (g20), नामानः (g21). Everything else is fixed by case,
agreement, verb agreement, or the absolutive form itself.
