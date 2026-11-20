# Anvaya Sanskrit — state of record

- **Product:** Anvaya Sanskrit, the Sanskrit language edition of the Codetopo family. Family name ruled by the Director 2026-11-20 (products register entry 29). This repo stood up 2026-11-20 as the product's home **in proving**.
- **Spike (2026-11-19):** rule reader over hand-derived morphology — 25/29 <MASKED_USER_ID_001>ict, 29/29 with anvaya conventions; the only obtainable statistical parser (Stanza, Vedic model) scored 6/29. Verdict: true about the language, not yet about the tools.
- **Stage 1 gate (2026-11-20):** the deterministic chain (vidyut lipi → house sandhi segmenter → vidyut kosha 0.4.0 → adapter → preserved rule reader) scored fixture 29/29 positional end-to-end from raw print; held-out 11/38 positional. **Gate: FAILED on the held-out leg. Named back. No release built.**
- **Root cause:** the kosha lexicon cannot separate stem-fragments from word forms; homonym/gender candidate noise; fusion-versus-compound undecidable from that lexicon. Karaṇa (tṛtīyā) remains unmeasured across both passages — named, not skipped.
- **Revisit condition:** a lexicon that marks stem-fragments as such, or a Heritage-class analyzer runnable in our environment; then the preserved gate re-runs on both golds (fixture ≥ 86.9% end-to-end and a printable held-out score).
- **Rewatch:** sanskrit-frontend-rewatch, monthly (1st), reports only on a tested change.
- **Release gate:** NOT RUN. **Guardian Mesh:** NOT RUN. Nothing for sale; no price set.
