# Reviewing the Alash Science Bench pilot

Thank you for reviewing. This takes about **2 to 4 hours for one field (20 items)**, or a full pass over a
single field you know best. You do not need to run any code.

## Background in one minute

160 Kazakh questions about scientific terms and ideas in Alash-era books. An AI wrote each item and
a second AI checked it against the OCR text. No person has read them yet. That is your job. Read the
[README](README.md) status box and [RIGHTS.md](RIGHTS.md); this repository is public, but the passage rights
are unresolved, so please do not copy the passages elsewhere.

## Your steps

1. Pick a field in `review/items/` (for example [chemistry](review/items/chemistry.md)). Tell the maintainer
   which one so two people do not pick the same field unless you are deliberately double-reviewing.
2. **Blind first.** For each item read only the question and choices. Write your own short answer
   (without choices), then your choice letter. Do this before opening the fold.
3. Open **Key, evidence and AI-review notes**. Check:
   - Is the key actually supported by the evidence passage?
   - Is there exactly one correct answer among the choices? Could a reasonable expert defend another?
   - Are the distractors plausible, or can you eliminate them without knowing the topic?
   - Does the stem hint at the answer (a shared word root)?
   - Could someone answer it from general school science without these books?
   - Is the Kazakh natural and unambiguous? Is author, work and role (author, translator, compiler) right?
4. If you can reach the original scan or printed edition, compare the characters the answer depends
   on and note differences. Mark `checked_against_scan` accordingly.
5. Record one verdict per item: **keep**, **revise** (say what to change), or **replace** (fact is unsuitable).
6. Return your findings in one of two ways:
   - Copy `review/review_sheet.csv` to `review/human_reviews/<your-name>.csv`, fill it in, open a pull
     request. Columns are explained below. Edit it in Excel or Google Sheets; save as UTF-8 CSV.
   - Or open an *Item review* issue per problem item. Good for a few comments.
   - **Excel route (no code):** `python3 scripts/make_excel_pack.py OUTPUT_DIR` builds a Kazakh-language workbook with
     drop-downs, a pilot subset of 16 items and a time log. After it comes back,
     `python3 scripts/import_excel_reviews.py FILLED.xlsx` converts it into `review/human_reviews/<name>.csv`.
     Both need `pip install openpyxl`.

Please do not edit `data/`, `source/` or `review/items/` directly; they are generated or
hash-bound to earlier reviews. The maintainer applies accepted changes and re-runs the checks.

## Sheet columns

| Column | Fill with |
|---|---|
| `reviewer` | Your name or initials |
| `blind_short_answer`, `blind_mcq_letter` | Your answers before seeing the key |
| `answer_supported_by_passage` | `yes`, `partly`, `no` |
| `single_correct_answer` | `yes`, `no` (explain in notes) |
| `distractors_plausible` | `yes`, `weak`, `no` |
| `stem_hints_answer` | `yes`, `no` (a word in the question gives the answer away) |
| `answerable_without_the_book` | `yes`, `maybe`, `no` |
| `kazakh_wording_ok` | `yes`, `no` (explain) |
| `ocr_affects_answer` | `yes`, `no`, `unsure` (an OCR error in the passage changes what the answer should be) |
| `checked_against_scan` | `yes`, `no`, `na` |
| `verdict` | `keep`, `revise`, `replace` |
| `notes` | Anything else; quote the exact text you want changed |

## Where your time is best spent

The [first-pass findings](docs/first-pass-review.md) list known weak spots (stems that contain the
answer's root, easy items, boilerplate explanations, OCR artifacts inside passages). Confirm or reject
those first; then look for what the AI reviewers missed. Mixed-script Күдерин OCR and the historical
Latin-script passages deserve extra care. Disagreements are useful: record them, do not average them away.

## What happens next

The maintainer collects the sheets, adjudicates disagreements, fixes items in `source/drafts/`, gets a
fresh independent review (the checker rejects edits without one), rebuilds and re-runs the checks.
Only after human review, scan checks, a split policy and a rights decision should the dataset be
uploaded publicly; see [docs/next-steps.md](docs/next-steps.md) and the upload checklist below.

## Upload checklist (maintainer)

- [ ] Human review done for all 160 items; `human_review_status` updated from `pending`
- [ ] Scan comparison done for at least a sample; `scan_review_status` updated
- [ ] Rights decided for each cited volume ([RIGHTS.md](RIGHTS.md)); real `license` set in the card
- [ ] Decide whether `test` is the right split name once a dev/test policy exists
- [ ] Replace boilerplate `explanation` / `evidence_caveat`; trim OCR rule lines
- [ ] `python3 scripts/build_alash_science.py --check --sources-root PRIVATE_DIR`, `export_hf.py --check`, `make_review_pack.py --check`
- [ ] `hf auth login`, then a **private** repo first:
      `hf repo create alash-science-bench --repo-type dataset --private`
      `hf upload <user>/alash-science-bench . . --repo-type dataset --exclude ".git/*" ".github/*" "review/*" "source/*"`
- [ ] Open the Hub viewer, run `load_dataset("<user>/alash-science-bench", split="test")`, then decide visibility
