# First-pass review of the pilot (28 October 2026)

Done by Claude (an AI agent) for the maintainer before sharing the repo. This is a data-quality
screen, **not** a human review and not a substitute for [REVIEW.md](../REVIEW.md). No model was
evaluated.

## What I ran

- `build_alash_science.py --check` against the private sources: passed (160 pairs, 12 volumes,
  107 pages, passages verbatim in OCR). The rebuilt CSV is byte-identical to the original export.
- The same check offline (as a colleague would run it): passed.
- Descriptive statistics on the CSV, and a hand read of 7 evenly spaced items plus 14 items flagged by
  the overlap scan below. That is a sample of about 13% of the items, not a read of all 160.

## Findings

| # | Finding | Evidence | Suggested action |
|---|---|---|---|
| 1 | **Task mix is lopsided.** 118 of 160 items (74%) are term recall; linguistics and psychology are 100% term recall. | `task_family` counts | Report field scores per task family, or rebalance in v0.2 |
| 2 | **Fields are confounded with authors.** Physics and geometry are entirely Елдес Омарұлы (40 items, 25% of the set); linguistics is entirely Байтұрсынұлы. | `author` by `field` | Add other authors/works per field before reading field gaps as discipline gaps |
| 3 | **Some stems contain a root of the answer.** 50 of 160 answers share a 5-letter prefix with the stem. Many are harmless (`есімше`, `психология`), but some are real morphological cues: LING02 `жалғау` → `Жалғамалы тіл`; LING07 `ниеттеніп` → `Ниетті көсемше`; PSY02 `қабілетінен` → `Қабілеттер қисыны`. | Prefix scan, 14 inspected | Reviewer to judge each flagged stem; reword or accept |
| 4 | **Distractors reuse other items' answers.** In 114 option slots a distractor is another item's correct answer (for example the three linguistic typology terms LING01 to LING03). Within one test session, solving a few items narrows the rest by elimination. | Exact string match across items | Fine with fresh conversations per prompt, but items are not independent; keep them together in any split |
| 5 | **Some items are easy without the book.** MAT01 asks which modern science `пішіндеме ілімі` corresponds to, among Алгебра, Тригонометрия, Арифметика and Геометрия. CHE06 `Тотығу` is school chemistry. | Hand read | Add ordinary-science control items; consider dropping or hardening these |
| 6 | **No answer-length shortcut found.** The correct option is the unique longest in 31 and the unique shortest in 32 of 160 rows. | Option lengths | None |
| 7 | **Answer keys are balanced.** Exactly five A, B, C, D per field. | Manifest | None |
| 8 | **Metadata is thin.** `original_year` known for 39 rows; `printed_page` missing for PED06, PED08, MAT12; 21 rows have no workbook row. | Blank counts | Fill from title pages during scan check |
| 9 | **Boilerplate text.** 79 distinct `explanation` strings; two sentences cover 69 rows. `evidence_caveat` has five variants, in English and Kazakh. | Counts | Replace with item-specific explanations; one language |
| 10 | **OCR artifacts inside evidence.** 4 passages contain rule lines (for example MAT01 ends with a row of dashes); 19 contain Latin-script words. | Regex | Trim rule lines (offsets then change, so rebuild); keep Latin text but note it |
| 11 | **Review independence is agent-to-agent.** `biology_physics` reviewed `math_chemistry` and vice versa; `math_chemistry` reviewed 80 items. All reviewers are AI. | `reviewer` counts | This is the main reason for REVIEW.md |

## What I did not check

Whether the Kazakh is natural, whether any term mapping is scientifically right, whether an OCR
character differs from the scan, whether the authors really coined or only used a term, and whether
any item is answerable by a model without the book. Those need people, scans, and later a model run.
