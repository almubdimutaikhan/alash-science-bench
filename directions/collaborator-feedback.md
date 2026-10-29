# Collaborator feedback, 29 October 2026

Source: chat messages from a research collaborator, paraphrased. Context after each point is added by
the maintainers and checked against the repository.

## 1. Sources, rights and license

**Said.** The dataset gives page numbers and other metadata but no source files. Will we provide them?
Under what license are we working? The sources were obtained by parsing the National Digital Library
of Kazakhstan (kazneb).

**What the repo has.**
- Per row: author, work, OCR page ID, printed page, workbook row, page SHA-256, character offsets, and the
  verbatim passage. The OCR books themselves (about 69 MB, 39 volumes) are not included.
- [RIGHTS.md](../RIGHTS.md): "not assessed"; the Hub card says `license: other`.
- Kazneb as the origin is the collaborator's statement. It is not recorded anywhere in the repo yet and has
  not been checked by us.

**Gap.** No decision on (a) whether kazneb's terms permit redistribution or text mining of the scans, (b) who
holds rights in the transcriptions, (c) what license applies to our own questions. Two further observations:
- The 17 raw-OCR records containing English messages such as "I am sorry" ([corpus review](../docs/corpus-review.md))
  suggest that the transcription was produced by a vision-language model rather than classical OCR. If so, it is a
  derivative of the scans and its accuracy is also unverified.
- Without the sources, nobody outside the project can reproduce the passage check; they can only trust the stored
  hashes.

## 2. Evaluate state-of-the-art Kazakh-specific and general LLMs (paper prospect)

**Said.** For a paper, test SOTA Kazakh and general models. Two hypotheses:
1. A model may understand a historical term **when shown the passage** but fail to **recall** it unaided.
2. A model may **identify** the term among multiple choices without being able to **produce** it.

**What the repo has.** The data already supports both contrasts: every row has a short-answer and a multiple-choice
format, and a passage that can be supplied or withheld. That gives the 2 x 2 (format x context) in
[docs/next-steps.md](../docs/next-steps.md). No runner exists and no model has been evaluated.

**Gaps.** See [summary-and-next-actions.md](summary-and-next-actions.md), section "Making the hypotheses testable".
In short: supplying a passage that contains the answer verbatim tests extraction, not understanding; and MCQ
vs short-answer gaps are confounded by option leakage and by spelling-tolerant scoring.

## 3. Task types

**Said.** Some tasks in an earlier paper looked very interesting (two photos, not available to the maintainers' tooling).
Establish dataset-creation methodology, exact task types and the research question first.

**What the repo has.** Four task families (term recall 118, concept identification 21, scientific explanation 11,
scholarly discourse 10), concentrated in term recall.

**Gap.** A deliberate task taxonomy. Needs the photographed paper identified and its tasks mapped to Alash material.

## 4. Linguist help

**Said.** After methodology, task types and research question are settled, ask linguists, and possibly the students of a
linguistics professor, to help.

**What the repo has.** A Kazakh-language Excel workbook and importer for one linguist reviewer; pilot of 16 items; time log
([REVIEW.md](../REVIEW.md)).

**Gap.** A reviewer protocol that scales to several part-time students (training, calibration items, agreement statistics,
payment or credit).

## 5. Scale

**Said.** Benchmarks work best with at least 200 to 500 questions per task type, so roughly 5,000 to 10,000 QA in total.
Then test LLMs on scientific questions and write a research paper, not only a benchmark paper.

**What the repo has.** 160 factual targets (320 prompts), 20 per field, from 12 of the 39 supplied volumes.

**Gap and arithmetic.**
- 5,000 to 10,000 items at 200 to 500 per type implies about 10 to 50 task types; there are 4 families today.
- 95% interval half-width for an accuracy near 50%: about 22 points at n=20 (today, per field), 7 points at n=200,
  4.4 points at n=500, before accounting for shared sources.
- Human review at 6 to 8 minutes per item is 500 to 1,300 reviewer-hours for 5,000 to 10,000 items, per pass. Full
  double review at that size is not realistic, so scaling needs a tiered validation plan.
- Supply of candidate material is not the bottleneck: the corpus inventory lists 74,535 term rows from 39 volumes, 7,915 with
  an annotation, against 12 volumes used so far.

## 6. The collaborator's endorsement of the outside assessment

The collaborator passed on an AI-written assessment unchanged and agrees with it: "the idea is very good and the
foundation is established; it needs improvement". The PDF is in [sources/](sources/). Its main points are summarized
and compared with the collaborator's in [summary-and-next-actions.md](summary-and-next-actions.md).
