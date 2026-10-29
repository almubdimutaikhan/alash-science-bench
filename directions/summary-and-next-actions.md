# Summary and next actions (29 October 2026)

## Where things stand

- A 160-item pilot with strong item-level provenance. AI-written, AI-reviewed, **not human-reviewed**; no
  model evaluated; source-excerpt rights unresolved.
- Two independent outside views now agree on the verdict: the collaborator and the AI assessment in
  [sources/](sources/). Both say: good foundation, needs a clearer research question, validated items and a real
  evaluation before scale.
- One tension to resolve: the assessment says *validate before scaling*; the collaborator proposes *5,000 to 10,000
  items*. The plan below treats these as two phases of one path, not alternatives.

## Where the sources agree

| Point | Collaborator | AI assessment | Repo today |
|---|---|---|---|
| Needs LLM evaluation for a paper | Yes, Kazakh-specific and general models | Yes, several multilingual/Kazakh-adapted models, 25% chance baseline, human baseline if feasible | No runner, no results |
| Central hypothesis is a knowledge gap between modes of access | Passage vs recall; recognition vs production | Modern concept vs historical term; format, orthography, source context, model family | Format and passage are in the data; no modern-concept controls |
| Task design comes first | Fix methodology, task types and RQ before recruiting linguists | Distinct "terminology" and "scholarly understanding" tracks | 74% term recall |
| Human review needed | Linguists, students | Double-review 16 items, then all 160, with scans | Excel pilot ready, nothing returned yet |
| Rights | Asks about sources and license | Per-volume rights decision is a release prerequisite | RIGHTS.md: not assessed |
| Scale | 200 to 500 per task type | Not before the pilot is validated | 160 items |

## Proposed research question

> Do language models that know a modern scientific concept also know, and can they produce, the historically
> attested Kazakh term for it, and how does that depend on answer format, evidence access, spelling and model family?

This is the AI assessment's testable hypothesis merged with the collaborator's two. It is a hypothesis, not a
finding.

## Making the hypotheses testable

**H1, passage vs recall.** "Understands with the passage, cannot recall without it."
- The pilot's passage contains the answer verbatim, so a model can succeed by copying a span. A gain from the passage then
  shows reading, not understanding of the term.
- Add items whose evidence supports a paraphrased or applied answer (explain the term, choose the correct use, classify an
  example), and report the passage gain separately for extractive and non-extractive items.
- A small gain can also mean OCR noise, ambiguity or grading error; inspect errors before interpreting.

**H2, recognition vs production.** "Picks it from options, cannot produce it."
- Same stem, two formats: already in the data.
- Controls needed: an options-only run (no question) to measure what distractors give away; shuffled option order; the
  flagged stem-cue and easy items fixed first ([first-pass review](../docs/first-pass-review.md)); the 114 cross-item distractors
  handled by fresh conversations and kept in one split.
- Short-answer scoring must tolerate inflection and historical spelling, or the gap measures orthography. Pre-write the rubric,
  grade a sample by hand and blind to model identity, and calibrate any AI grader against it.

**H3, concept vs term (from the assessment).** For a set of concepts, build matched items: a modern-science question, a
historical-term recognition item, a historical-term production item, and a "what does this author say" item. The within-concept
gap separates missing terminology from missing science.

**H4, orthography (from the assessment).** Present the same term in original spelling, normalized Cyrillic and, where
justified, Latin script, labelled by how each variant was derived. Interpret only after a reader confirms equivalence.

**Models.** At least one Kazakh-adapted model and several general models, versions pinned at run time. Candidates to verify for
availability: the Kazakh-adapted models already audited in this project's sibling repository, a Kazakh instruction model such as
Sherkala-8B-Chat, and current open and closed general-purpose models. Include the 25% chance baseline for four-way MCQ.

## Task taxonomy (to settle before scaling)

The collaborator's target of 200 to 500 items per type implies 10 to 50 types. Candidate axes, to be reconciled with the tasks
in the photographed paper:

| Axis | Values |
|---|---|
| Direction | concept to term; term to concept |
| Access | closed book; with passage |
| Format | short answer; multiple choice |
| Depth | recall of a term; definition; explanation or argument; attribution or comparison; publication history |
| Orthography | original; normalized; Latin |
| Field | linguistics, psychology, pedagogy, biology, physics, geometry, chemistry, agronomy, others |

Not every cell needs 200 items. Choose a core of 6 to 10 task types for the paper, then expand.

## Phased action list

Effort is the maintainers' rough estimate; none of it is scheduled.

### Phase 0: decisions (1 to 2 weeks, no coding)
1. **Rights.** Read kazneb's terms of use; find out who produced the transcriptions and under what terms; decide per volume.
   Options: (a) keep sources private, publish questions with hashes and offsets but without `passage`; (b) seek permission from
   the library or edition holders; (c) publish only volumes with clear status. The closed-book track works without passages.
2. **Research question and hypotheses** in the form above; write them down before collecting more data.
3. **Identify the earlier paper** from the photos, extract its task types, map each to the Alash material.
4. **Authorship and roles** for the paper (who builds, who reviews, who evaluates), and how linguists and students are credited or paid.

### Phase 1: validate the pilot (2 to 4 weeks)
5. Linguist completes the 16-item Excel pilot; adjust instructions from what he finds confusing.
6. Fix the known issues: stem cues, easy items, boilerplate explanations, trimmed OCR rule lines. Re-review, rebuild.
7. Remaining 144 items reviewed; disagreements adjudicated and logged; statuses updated from `pending`.
8. Compare the answer-critical characters in a sample against original scan pages (needs the images, which are not in the supplied
   folders).
9. Release as v0.2 with a frozen version and hash.

### Phase 2: design the method (parallel with phase 1)
10. Write the dataset-creation methodology: how a term is selected from the workbook, how the passage is chosen, how distractors are
    built, how each task type is generated, who reviews what. This is the document the collaborator suggests settling before
    approaching more linguists.
11. Define the scoring rubric for short answers and for explanation tasks.
12. Define the split policy: group by work and concept family; keep the pilot as development data; plan a source-disjoint test set.

### Phase 3: evaluate (after phases 0 to 2)
13. Build a version-pinned runner: chat templates, fresh conversation per prompt, fixed decoding, raw outputs and parser decisions stored
    separately from the dataset.
14. Smoke test on development items with malformed answers, then the 2 x 2 plus the options-only control.
15. Analysis with paired comparisons and source-clustered intervals; error taxonomy distinguishing model errors from item defects.

### Phase 4: scale (only after phase 1 is clean)
16. Generate candidates semi-automatically from the term workbooks and passages (74,535 term rows across 39 volumes), using the validated
    methodology.
17. Tiered validation: full human review for the held-out test set; stratified sampling with an error-rate threshold for the rest;
    automatic checks for everything. Reviewing 5,000 to 10,000 items once at 6 to 8 minutes each would take roughly 500 to 1,300
    hours, which is why student reviewers and sampling matter.
18. Recruit linguists and students with a calibration set, a written guide in Kazakh and an agreement measure (for example Cohen's kappa on
    a shared subset).
19. Write the paper: hypotheses, dataset, validation, models, results, limitations. The collaborator's framing is more than a
    benchmark paper: findings about where models fail.

## Open questions

- What are the photographed paper and its tasks? (blocks step 3 and the taxonomy)
- Who produced the transcriptions, and what do kazneb's terms say? (blocks any further public release of passages)
- Is the target venue a benchmark/resource track or an analysis paper? It changes how much scale is required.
- Budget and recruitment channel for linguist reviewers; the pilot estimate was about 2 to 3 hours and 18 to 24 hours for the full 160.
- Whether the Excel pilot has been returned, and what it showed.

## What this summary does not establish

No model has been run. The statistics above are arithmetic from stated assumptions, not results. The AI assessment was not independently
checked beyond comparing its repository statements with the repository.
