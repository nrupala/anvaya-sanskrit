# Anvaya Sanskrit

**Anvaya** — अन्वय, the joining of words into meaning.

**State: IN PROVING. No release. Nothing for sale.**

Anvaya Sanskrit is intended to be the Sanskrit language edition of the Codetopo family: the measured map of a Sanskrit text for agents — who does what to whom, what rests on what — read the way Sanskrit itself offers to be read. In Sanskrit the relations are worn on the words: the vibhakti (case) endings mark the kāraka relations — kartā (the doer), karma (the object), and the rest — which is why Sanskrit word order can be free. A rule reader, not a statistical guesser, is the right in<MASKED_USER_ID_001>ument for this language. That is the design. What follows is the measurement of how far the available tools carry it.

## The measurement

Gold standard: the opening of the Pañcatantra (Kathāmukha), four sentences, 29 relations derived by hand from the grammar, every case-to-relation mapping cited to its Pāṇinian rule.

- **The rule reader over correct morphology** (vibhakti → kāraka mapping, agreement, verb-number agreement; no word position used): **25/29 <MASKED_USER_ID_001>ict (86.2%)** — zero relation-type errors, zero inversions; the four misses are head-choice only, where the relation type is certain from the case alone. With the standard anvaya reading conventions: **29/29 (100%)**.
- **The full chain, end-to-end from raw printed text** (sandhi segmentation → lexicon analysis → the rule reader): on the fixture passage, **29/29**; on a passage it had never seen (Pañcatantra, Mitrabheda; 38 relations, hand-golded the same way): **11/38 (28.9%)**.

## The gate verdict

Anvaya Sanskrit was **named back at its Stage 1 gate on 2026-11-20**. The reader over correct morphology is exact; the obtainable front end cannot yet produce that morphology on unseen text. The lexicon available to the chain (vidyut kosha 0.4.0) cannot separate fragments of words from whole word forms — on new text, names shatter into phantom words (the lion Piṅgalakaḥ cut into pieces), and an exact reader then faithfully relates phantoms. No tuning of the chain was <MASKED_USER_ID_001>ong on both passages, and a 29% score is not one this house prints beside a product.

What is missing, named: **a lexicon that marks stem-fragments as fragments, or a Heritage-class morphological analyzer that runs in our environment.** The day either exists, the preserved chain and both gold passages re-run the gate as they stand.

## The rewatch

A monthly rewatch (sanskrit-frontend-rewatch) checks for a new lexicon release or a runnable Heritage-class analyzer and re-runs the gate on both passages. It reports only when something has been tested. Revisit condition: fixture end-to-end at or above the English edition's published bar (86.9%) **and** a held-out score printable beside it.

Work records (titles, kept in the house work archive): *Sanskrit spike — VERDICT / FLAW-AUDIT / GOLD* (2026-11-19) and *Sanskrit profile — STATUS* (2026-11-20). The numbers above are the public summary of those records.

## State

**IN PROVING — no release, nothing for sale. Release gate: NOT RUN. Guardian Mesh: NOT RUN.**

## Licence

AGPL-3.0. © 2026 2351485 ALBERTA INC. / AIMLDS.
