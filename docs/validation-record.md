# Independent review and validation record
Reviewed 25 October 2026. The dataset remains a local AI-reviewed draft. No model inference or benchmark was run.
The final export contains 160 concept/fact pairs, 320 prompts across two formats, eight fields with 20 pairs each, 12 supplied volumes and 107 cited OCR pages.
## Review coverage
Each file was reviewed by an agent who did not author its items. Review logs contain one record per concept. These are agent judgments against the supplied OCR, not human expert or original-scan verification.
| File | Records | Passed | Revised | Independent reviewer |
|---|---:|---:|---:|---|
| biology_physics_review.jsonl | 40 | 29 | 11 | linguistics_psychology |
| linguistics_psychology_review.jsonl | 40 | 40 | 0 | math_chemistry |
| math_chemistry_review.jsonl | 40 | 31 | 9 | biology_physics |
| pedagogy_agronomy_review.jsonl | 40 | 16 | 24 | math_chemistry |

**Total: 160 reviewed, 116 passed without revision, 44 revised.** All item-specific semantic `unresolved` lists are empty after revision. Standard pending human/scan checks are retained separately in statuses and limitations.
## Substantive corrections
- PED02: removed the book title that leaked the requested answer, «Педагогика».
- PED14: replaced an unsupported framing as a newly named lesson category with the source-supported teaching-purpose question.
- PED15: removed a yes/no polarity cue and asked directly about the educational purpose.
- AGR02: included the actual cropping/fallow definition in the evidence rather than starting after it.
- AGR15: accepts either «Қаз мойын суы» or «Күл суы» as well as a combined answer.
- BIO18: added source qualifiers to distinguish the lens from another transparent anatomical structure.
- BIO02: corrected the direct terminology discovery pointer to workbook row 967.
- BIO15: explicitly framed a historical notochord description and retained specialist-review limitations.
- CHE10: removed a circular accepted answer when the question requests composition.
- CHE19: removed a modern-only synonym when the question requests the historical name.
- Several records: improved option plausibility, comparable answer length, wording, case variants and exact evidence boundaries.

See `source/reviews/*_review.jsonl` for the per-concept records.
## Automated checks
The standard-library exporter checks exactly 20 pairs per field, unique IDs/questions, identical factual stems across formats, four distinct options, answer/alias consistency, independent review coverage, absence of unresolved content errors, actual source files/page IDs, verbatim evidence, source-page hashes and excerpt offsets, physical workbook row existence, CSV parser round-trip, deterministic shuffle, and five correct A/B/C/D answers per field. It does not call model APIs or load weights.

A supplementary scan found no canonical or accepted answer string of at least five characters directly embedded in a question stem. This is a limited string check, not proof that all semantic clues are eliminated. No formula-like cells beginning with =, @ or + were found. The CSV was also re-imported using the spreadsheet reader.
## Remaining limits
- Human language/disciplinary review and original-scan checks are pending for all records. Mixed-script Күдерин OCR needs particular attention.
- No train/dev/test split is assigned. Do not call the present pilot held out after using it to tune prompts.
- Twenty pairs per field give coarse field-level estimates; sources and paired formats create dependencies.
- Task mix and difficulty differ across fields. Geometry is the entire current mathematics slice.
- Some author-conditioned questions can be answered using general scientific knowledge. Source verification does not prove knowledge uniquely attributable to Alash exposure.
- No source-excerpt redistribution license or absence from pretraining has been established.

No claim is made that the question set is error-free or ready for a public leaderboard. The review record makes the present verification level explicit.

## Final artifact audit, 26 October 2026

A further independent agent checked the final CSV, exporter, manifest, documentation and representative content. Counts, local links and the guide's BIO01 example agreed with the data. Each of the 160 reviews was then bound to a canonical SHA-256 hash of its reviewed draft item; the exporter rejects subsequent content changes until a fresh review updates that binding. This protects against stale review records, not against an originally mistaken judgment.

The learning guide passed a headless-browser check of all four format/context modes, initial hiding of evidence and answer, answer reveal/hide, all three quiz interactions, JavaScript errors, and horizontal overflow at narrow mobile widths. Desktop and dark-mode mobile screenshots were visually inspected. Dataset export and source checks were revalidated. No benchmark or evaluation-model inference was executed.
