# Data dictionary and grading notes

> Moved from the original local pilot. `split` is dropped from the Hugging Face export (`data/test.jsonl`) to avoid confusion with the Hub split; `accepted_answers_json` becomes the list `accepted_answers`; blank years, `printed_page` and `source_row` become `null`.

This dataset asks whether language models can recall and recognize scientific terminology and ideas in the supplied Kazakh scholarly texts. Questions and reference answers are in Kazakh. General political knowledge is outside this pilot.

**Status: AI-authored and independently AI-reviewed. Human disciplinary review and comparison against original scans are pending. This is a local research draft, not a validated public benchmark. No benchmark or model inference has been run.**

## What is one pair?

`question_pairs.csv` contains **160 rows: 20 per field**. Each row has one factual target and two question formats:

- `short_question`: answer without seeing choices.
- `question` plus `mc_answer1`–`mc_answer4`: the same question with four choices.

This gives 320 prompts across two formats, based on 160 concept/fact records. Some records share passages and works, so they are not 160 statistically independent observations. Treat the two formats as paired measurements, and retain source grouping when estimating uncertainty.

The eight fields are linguistics/literary theory, psychology, pedagogy/education, biology/anatomy/physiology, physics, mathematics/geometry, chemistry, and agronomy/botany. Mathematics currently covers geometry, not calculus or all mathematics. Other fields are also selected slices of the supplied books, not exhaustive disciplinary coverage.

## Primary evaluation: without passage

The question specifies the scholar or work when its historical usage matters. It does not supply the evidence passage. No browsing or retrieval is allowed in this condition.

For short answers send only the instruction and `short_question`. **Do not send choices, reference answers, explanations, passages, accepted answers or source metadata.**

For MCQ send the instruction, `question` and four choices. Do not include the answer key, passage or explanation. Use a fresh independent conversation for every prompt, including the companion format; otherwise one answer can reveal information to the next.

Later, repeat each format with `passage` supplied to evaluate understanding with evidence. Keep the question stem, model and generation policy fixed within that comparison. Do not interpret a comparison that changes both format and passage access as the isolated effect of passage access.

## Column guide

| Column(s) | Meaning |
|---|---|
| `id`, `concept_id` | Stable item and pairing identifiers |
| `field`, `subfield`, `task_family`, `task_type` | Discipline, normalized task family, and the author's more specific task wording |
| `short_question`, `question` | Same question stem in this version; answer format changes |
| `reference_answer` | Canonical concise answer |
| `accepted_answers_json` | JSON array of reviewed spelling/equivalence variants; it is not an exhaustive semantic grading rubric |
| `mc_answer1`–`mc_answer4` | Four answer choices |
| `correct_answer_num` | **1-based** correct choice, as in Belebele |
| `answer_letter` | Equivalent A/B/C/D key |
| `passage` | Verbatim contiguous excerpt of the supplied raw OCR; evidence for graders |
| `explanation` | Why the answer is supported or how the historical framing should be read |
| `author`, `work` | Attribution; translator and compiler roles are retained where relevant |
| `original_year`, `edition_year` | Year metadata only where supported; empty means unestablished, not zero |
| `source_ocr`, `source_page`, `printed_page` | Local OCR file, actual JSON page ID, and printed footer when identifiable |
| `source_workbook`, `source_sheet`, `source_row` | Discovery pointer to a terminology annotation, where known; OCR is the actual evidence |
| `source_page_sha256`, `evidence_start_char`, `evidence_end_char` | Source-page integrity and Python character offsets; `page[start:end] == passage` |
| `source_group_id` | Conservative grouping by supplied volume for later splitting and analysis |
| `split` | `unassigned_pilot`; no train/dev/test separation is claimed |
| `review_status`, `reviewer` | Independent agent review, distinct from authoring |
| `human_review_status`, `scan_review_status`, `evidence_caveat` | Outstanding verification and transcription limits |
| `language` | `kk` |

The names `question`, `passage`, `mc_answer1`–`mc_answer4`, `correct_answer_num` resemble Belebele. The additional columns preserve short-answer evaluation and historical provenance. This is not a copy of the Belebele dataset or an official extension of it.

## Construction and verification

1. Candidate terminology was located in the local Excel sheets and OCR.
2. Authors selected source passages and wrote questions, reference answers and distractors.
3. A different agent checked each record against its cited OCR, looking for entailment, ambiguous answers, incorrect attribution, answer cues and unsuitable aliases.
4. Findings and revisions were recorded in `source/reviews/*_review.jsonl`. A final independent artifact audit bound each review to a hash of the reviewed item, so later content edits cannot silently inherit an old review.
5. The exporter checked exact evidence, actual page IDs, physical workbook row existence, paired stems, answer/alias alignment, duplicate questions, quotas, review independence and CSV round-trip integrity.
6. Choices were shuffled deterministically, with exactly five correct A/B/C/D answers in each 20-item field.

The draft JSONL files in `source/drafts/` are the editable inputs. `question_pairs.csv` and `manifest.json` are generated exports. Edit an item, have another reviewer recheck it and update its review record and `reviewed_item_sha256`, then rebuild. The exporter rejects stale review hashes. Do not hand-edit the exported CSV as the sole source of truth.

```bash
python3 scripts/build_alash_science.py --check    # offline: no private sources needed
python3 scripts/build_alash_science.py --sources-root /path/to/private/sources   # rebuild; also re-verifies the OCR evidence
```

These commands use the Python standard library and only build/check the dataset. They do not import model inference libraries, download weights, call model APIs, or run a benchmark.

`manifest.json` records counts, review totals, input hashes, the export hash and shuffle seed. A matching hash establishes file identity; it does not establish factual correctness or absence from model pretraining.

## Read the CSV safely

Use a CSV parser: source passages contain real newlines, commas and quotation marks. A physical line count is not the number of records. The encoding is UTF-8.

```python
import csv
import json

with open('data/question_pairs.csv', encoding='utf-8', newline='') as f:
    items = list(csv.DictReader(f))

item = items[0]
choices = [item[f'mc_answer{i}'] for i in range(1, 5)]
answer = choices[int(item['correct_answer_num']) - 1]
aliases = json.loads(item['accepted_answers_json'])
```

## Grading and limits

For MCQ, score the generated final choice using a documented parser. For instruction/chat models use the official chat template and record reasoning mode, output budget, decoding settings and exact model revision. The existing base-model letter-logit audit is a different evaluation protocol.

For short answers, exact matching is a useful first pass for a narrowly requested historical term. Accept harmless inflection, case and spelling variants when they preserve the target. Concept explanations require semantic human grading with the source and rubric. A model should receive concept credit for a valid equivalent only when the question asks for the concept; a modern equivalent alone does not satisfy a question explicitly asking for the historical expression.

An AI reviewer is not an independent human expert. Raw OCR can contain recognition mistakes, mixed scripts, lost diagrams and outdated descriptions. A question asking what a historical author wrote is not a claim that the description is current scientific consensus. Usage in a book is not evidence of first coinage. Author-conditioned textbook questions can sometimes be answered from general scientific knowledge; add difficulty and ordinary-science controls in a later version.

Task composition and difficulty are not matched across fields: linguistic items are mainly historical-term recall, while pedagogy includes more explanatory questions. Field score differences therefore cannot be attributed to scientific discipline alone. This pilot does not yet provide a dedicated publication-history or historical-events track.

Do not tune prompts or thresholds on all these items and then describe their score as a held-out result. All records are currently a public-to-the-user pilot. Before formal evaluation define development/test groups at original-work/concept-family level, manually reconcile repeated works across collections, and check that fields are represented. A volume ID is a conservative helper, not a complete deduplication system.

No license or redistribution permission for source excerpts is asserted. Keep this draft private until edition-specific rights and attribution are checked. Source scans are not included. New question writing and OCR do not prove the underlying content was absent from pretraining.

## Learn and plan

- [Learning guide](learning-guide.html): a worked example, reveal controls and self-check exercises.
- [Next-step plan](next-steps.md): human review, split design and a future evaluation protocol.
- [Corpus review](corpus-review.md): inventory and source-quality findings.

Methodological references: [KazMMLU](https://aclanthology.org/2025.acl-long.701/), [answer-position sensitivity](https://aclanthology.org/2024.findings-naacl.130/), [generated answers versus first-token scores](https://aclanthology.org/2024.findings-acl.441/), [paired bootstrap foundations](https://aclanthology.org/W04-3250/), and [Hugging Face dataset cards](https://huggingface.co/docs/hub/datasets-cards).
