---
language:
- kk
license: other
license_name: rights-not-assessed
license_link: RIGHTS.md
pretty_name: Alash Science Bench (pilot)
task_categories:
- question-answering
- multiple-choice
tags:
- kazakh
- alash
- historical-terminology
- scientific-terminology
- evaluation
- benchmark
size_categories:
- n<1K
configs:
- config_name: default
  default: true
  data_files:
  - split: test
    path: data/test.jsonl
dataset_info:
  config_name: default
  features:
  - {name: id, dtype: string}
  - {name: concept_id, dtype: string}
  - {name: field, dtype: string}
  - {name: subfield, dtype: string}
  - {name: task_family, dtype: string}
  - {name: task_type, dtype: string}
  - {name: short_question, dtype: string}
  - {name: question, dtype: string}
  - {name: reference_answer, dtype: string}
  - {name: accepted_answers, list: string}
  - {name: mc_answer1, dtype: string}
  - {name: mc_answer2, dtype: string}
  - {name: mc_answer3, dtype: string}
  - {name: mc_answer4, dtype: string}
  - {name: correct_answer_num, dtype: int32}
  - {name: answer_letter, dtype: string}
  - {name: passage, dtype: string}
  - {name: explanation, dtype: string}
  - {name: author, dtype: string}
  - {name: work, dtype: string}
  - {name: original_year, dtype: int32}
  - {name: edition_year, dtype: int32}
  - {name: source_ocr, dtype: string}
  - {name: source_page, dtype: int32}
  - {name: printed_page, dtype: string}
  - {name: source_workbook, dtype: string}
  - {name: source_sheet, dtype: string}
  - {name: source_row, dtype: int32}
  - {name: source_page_sha256, dtype: string}
  - {name: evidence_start_char, dtype: int32}
  - {name: evidence_end_char, dtype: int32}
  - {name: source_group_id, dtype: string}
  - {name: review_status, dtype: string}
  - {name: reviewer, dtype: string}
  - {name: human_review_status, dtype: string}
  - {name: scan_review_status, dtype: string}
  - {name: evidence_caveat, dtype: string}
  - {name: language, dtype: string}
---

# Alash Science Bench (pilot)

Do language models know the scientific vocabulary and ideas that Alash-era Kazakh scholars wrote
down? 160 Kazakh questions about terms and concepts in textbooks and collected works by
Байтұрсынұлы, Аймауытов, Жұмабаев, Досмұхамедов, Омарұлы, Кемеңгерұлы, Шонанұлы and Күдерин, across
eight fields (20 each): linguistics and literary theory, psychology, pedagogy, biology and
anatomy, physics, geometry, chemistry, and agronomy and botany.

> **Status: pilot draft for human review. Not a validated benchmark.**
> Every item was written by an AI agent and checked against its OCR page by a *different* AI
> agent. **No human expert has reviewed it, no original scan has been compared, and no model has
> been evaluated.** Distribution rights for the source excerpts have not been cleared; see
> [RIGHTS.md](RIGHTS.md). Do not report scores on this set as a held-out result, and do not
> make the Hub repository public until [REVIEW.md](REVIEW.md) is done.

## What one row is

One row is one fact asked in two formats, so 160 rows give 320 prompts but only 160 facts, and
many rows share a book or page (160 rows, 12 volumes, 107 pages). Treat the formats as paired
measurements and cluster uncertainty by source.

| Format | Send the model | Never send |
|---|---|---|
| Short answer | instruction + `short_question` | choices, key, passage, explanation |
| Multiple choice | instruction + `question` + `mc_answer1`–`mc_answer4` | key, passage, explanation |

Use a fresh conversation for every prompt. The primary track is closed-book (no passage, no
retrieval). A later track repeats each format with `passage` added, with everything else fixed.
`correct_answer_num` is 1-based as in Belebele; each field has exactly five items per answer letter.
This is Belebele-*style*, not an extension of Belebele.

## Loading

```python
from datasets import load_dataset

ds = load_dataset("json", data_files="data/test.jsonl", split="train")   # local checkout
# ds = load_dataset("<hf-username>/alash-science-bench", split="test")     # after upload

row = ds[0]
choices = [row[f"mc_answer{i}"] for i in range(1, 5)]
gold = choices[row["correct_answer_num"] - 1]
```

The Hub split is called `test` because the set is evaluation-only. That is a naming convention,
not a claim: nothing is held out (`unassigned_pilot` in the CSV) and any prompt tuning on these items
makes them development data. Full column meanings are in [docs/data-dictionary.md](docs/data-dictionary.md).

## Composition, and what it implies

| | |
|---|---|
| Task family | 118 term recall, 21 concept identification, 11 scientific explanation, 10 scholarly discourse |
| Author concentration | Елдес Омарұлы wrote 40 of 160 items (all physics and geometry) |
| Years | `original_year` is established for only 39 rows; blank means unknown, not zero |

Field scores are therefore confounded with task type and author, and cannot be read as
"model is better at physics than pedagogy". Linguistics and psychology are 100% term recall;
pedagogy is the most explanatory field. Some author-conditioned questions can be answered from
ordinary science knowledge, so correct answers do not prove exposure to these books.

## How it was built and checked

1. Candidate terms were found in terminology workbooks and OCR of 39 supplied volumes.
2. An authoring agent chose a verbatim OCR passage and wrote the question, reference answer, accepted
   variants and three distractors.
3. A different agent reviewed each item against the passage: 116 passed, 44 were revised.
4. The exporter re-verifies, for every row: passage is verbatim in the cited OCR page (character
   offsets and page hash recorded), page IDs exist, workbook rows exist, stems match across formats,
   options and aliases are consistent, answer positions balance, and each review is bound to a hash
   of the item it reviewed. Details: [docs/validation-record.md](docs/validation-record.md).

None of that substitutes for a Kazakh-speaking domain reader or the original scans.

## Reproducing

```bash
python3 scripts/build_alash_science.py --check          # offline; standard library only
python3 scripts/build_alash_science.py --check --sources-root PRIVATE_DIR   # also re-verify OCR evidence
python3 scripts/export_hf.py --check                    # data/test.jsonl is in sync with the CSV
python3 scripts/make_review_pack.py --check             # review/ is in sync
```

The OCR books and workbooks (about 69 MB) are **not** in this repository. Without them the checker
runs offline and trusts the page hash and offsets stored in the CSV. Editing flow: change
`source/drafts/*.jsonl`, get a fresh independent review in `source/reviews/`, rebuild with the
sources, then run `export_hf.py` and `make_review_pack.py`. Do not hand-edit generated files.

## Repository map

| Path | Contents |
|---|---|
| `data/test.jsonl` | Typed export for Hugging Face (generated) |
| `data/question_pairs.csv`, `data/manifest.json` | Canonical CSV and counts/hashes (generated) |
| `source/drafts`, `source/reviews` | Editable items and the per-item AI review records |
| `review/` | Human-review pack for colleagues (generated); start at [REVIEW.md](REVIEW.md) |
| `docs/` | Data dictionary, validation record, first-pass review findings, next steps, corpus review, learning guide |
| `scripts/` | Builder/validator, HF exporter, review-pack generator. No model inference |

## Intended use and limits

Intended: closed-book probing of instruction/chat models for Kazakh historical-scientific
terminology, after human review and a frozen protocol ([docs/next-steps.md](docs/next-steps.md)).
Not intended: a public leaderboard, ranking models on a few points, or inferring training-data
membership. A passage in a book is evidence of usage, not of first coinage. Descriptions are
historical and may differ from current science. The source OCR contains recognition errors, mixed
scripts and Latin-script text. With 20 items per field, one answer moves a field score by 5 points.
