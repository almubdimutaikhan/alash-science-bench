# Next steps for the Alash scholarly knowledge benchmark

Prepared 25 October 2026. Dataset construction and verification are complete at the AI-reviewed draft stage. **No model or benchmark has been run.**

## 1. Make the source evidence trustworthy

Start with 16 pairs: two from each field. Open the original scans and compare every character needed for the answer, check work boundaries and author/translator roles, and ask another Kazakh speaker to answer without seeing the key. Include a domain specialist for uncertain scientific mappings. Record disagreement reasons and adjudication rather than silently choosing a majority.

Then apply the refined annotation guide to all 160 records. Replace weak, ambiguous or poorly transcribed items while keeping 20 per field. Retain stable IDs for small corrections; assign a new ID when replacing the tested fact. Do not label the data human-verified until that work is actually done.

**Output:** a reviewed question set, corrected source transcription where needed, and an adjudication log. Original raw OCR stays immutable.

## 2. Define what a correct answer means

Write a short rubric with examples for:

- Historical-term recall: the requested term or a genuinely attested variant is present.
- Concept identification: an accepted scientific equivalent is sufficient.
- Explanation or argument: the essential proposition is present and no central contradiction is introduced.

Decide how to score extra unsupported claims. Record factual correctness and unsupported attribution separately if both matter. A correct term followed by an invented coinage story should not disappear into a single unexplained score.

Blind model identity during grading. Double-grade a sample and report agreement before adjudication. AI grading may assist later, but should be calibrated against those human judgments rather than acting as the sole gold authority.

**Output:** an annotation/rating guide and accepted-variant updates.

## 3. Freeze development and test policy

The current file has `split=unassigned_pilot`. Do not choose a random row split. Group related terms, reverse/paraphrased questions, shared evidence, translations and repeated works across volumes. The two formats of a pair always stay together.

Check whether a useful field-balanced split is possible with the small source pool. If not, keep this version as development data and curate a fresh independent test set from additional work sections. Do not force a misleading split merely to have files called train and test. A training split is not required for an evaluation-only resource.

Freeze the prompt, output parser, normalization, grading rubric and generation policy using development items. Record a version and dataset hash before formal model evaluation.

**Output:** documented split groups and a frozen protocol.

## 4. Implement the evaluation later

When authorized in a later task, add a separate runner for instruction/chat models. Keep the existing original-base versus adapted-base audit as a separate research comparison.

For every model use its supported chat template, record the exact revision, and make context access explicit:

| Condition | Model sees | Purpose |
|---|---|---|
| Short answer, no passage | Instruction and question | Historical recall or unassisted explanation |
| MCQ, no passage | Instruction, question and choices | Recognition among alternatives |
| Short answer, with passage | Same question and evidence | Source-supported generation |
| MCQ, with passage | Same MCQ and evidence | Source-supported selection |

Use a fresh conversation for each item and condition. Fix browsing/retrieval policy, decoding policy, reasoning mode, stop conditions and a sufficient output budget. Reasoning and final-answer tokens should be tracked separately when supported. A fixed token budget is not an equal word budget across different tokenizers; inspect truncation and report it.

Store rendered prompts, model outputs, parser decisions, timing and token counts separately from the question dataset. Never overwrite the original answer key with model predictions. Test answer extraction on a few development examples, including malformed answers, before a full run.

**Output:** a reproducible runner and a small development smoke check, only after separate authorization. This phase has not been executed.

## 5. Analyze where knowledge fails

Report each format/context condition separately. With 20 questions per field, a single changed answer moves that field's score by five percentage points. Avoid ranking models on tiny differences.

Report per-field counts and accuracy, macro averages, paired differences and source/concept-clustered uncertainty. Compare the same question with and without evidence to study context benefit; compare formats under the same evidence condition to study option support. These are diagnostic comparisons and do not prove that a particular memory mechanism caused the difference.

Inspect errors: historical name missing, scientific concept misunderstood, wrong scholar/work, OCR sensitivity, invented citation, ambiguous gold, and answer-format failure. Distinguish model errors from dataset defects. If test items are changed after seeing results, release a new version and document the change.

**Output:** tables, uncertainty, representative errors and limitations. Negative or mixed results are useful findings.

## 6. Prepare a credible contribution

Verify edition-specific rights before publishing source excerpts. Write a Hugging Face dataset card explaining authoring assistance, AI and human review, scripts, fields, splits, source coverage, known biases and intended uses. Do not claim all Alash scholarship, all of a scientific discipline, or unseen pretraining content is covered.

Release the evaluation code, frozen configuration, dataset version, reviewed annotation guide and reproducible results together. Keep a correction channel and version history. A reliable small resource with documented uncertainty is a useful contribution to Kazakh NLP and evidence of research judgment for an MSc application.

## A manageable learning sequence

1. Explain one pair and its source to another person.
2. Find and repair one weak distractor without changing the tested fact.
3. Write three new questions from a different source section; have someone else answer them.
4. Load the CSV and calculate field counts using Python's `csv` module.
5. Explain why 160 pairs create 320 prompts but do not double the independent sample size.
6. Read the learning guide's primary sources before implementing evaluation.

Use the verified outputs as research evidence in your project narrative. Describe what you built and checked personally, what agents assisted with, and what remains uncertain.
