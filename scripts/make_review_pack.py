"""Generate the human-review pack from data/question_pairs.csv.

    python3 scripts/make_review_pack.py            # write review/
    python3 scripts/make_review_pack.py --check    # fail if review/ is stale

Outputs:
  review/review_sheet.csv   blank worksheet, one row per concept; the answer key is NOT in it
  review/items/<field>.md   readable pages: question and choices visible, key/evidence/AI-review
                            notes folded under <details>

Standard library only. The pack is derived data: edit source/drafts, not these files.
"""
import argparse
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / 'data' / 'question_pairs.csv'
REVIEWS = ROOT / 'source' / 'reviews'
OUT = ROOT / 'review'
SHEET_COLUMNS = [
    'id', 'field', 'author', 'work', 'question', 'choice_A', 'choice_B', 'choice_C', 'choice_D',
    # Reviewer fills these. Do the two blind answers before opening the key.
    'reviewer', 'blind_short_answer', 'blind_mcq_letter',
    'answer_supported_by_passage', 'single_correct_answer', 'distractors_plausible',
    'stem_hints_answer', 'answerable_without_the_book', 'kazakh_wording_ok',
    'ocr_affects_answer', 'checked_against_scan',
    'verdict', 'notes',
]
FIELD_TITLES = {
    'linguistics_and_literary_theory': 'Linguistics and literary theory', 'psychology': 'Psychology',
    'pedagogy_education': 'Pedagogy and education', 'biology_anatomy_physiology': 'Biology, anatomy, physiology',
    'physics': 'Physics', 'mathematics_geometry': 'Mathematics (geometry)', 'chemistry': 'Chemistry',
    'agronomy_botany': 'Agronomy and botany',
}


def load():
    with CSV.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    reviews = {}
    for path in sorted(REVIEWS.glob('*_review.jsonl')):
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.strip():
                r = json.loads(line)
                reviews[r['concept_id']] = r
    return rows, reviews


def sheet(rows):
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=SHEET_COLUMNS, lineterminator='\n')
    writer.writeheader()
    for r in rows:
        row = {c: '' for c in SHEET_COLUMNS}
        row.update({k: r[k] for k in ('id', 'field', 'author', 'work', 'question')})
        for i, letter in enumerate('ABCD', 1):
            row[f'choice_{letter}'] = r[f'mc_answer{i}']
        writer.writerow(row)
    return buffer.getvalue()


def quote(text):
    return '\n'.join('> ' + line if line.strip() else '>' for line in text.splitlines())


def page(field, rows, reviews):
    lines = [f'# {FIELD_TITLES[field]}', '',
             f'{len(rows)} concepts. Answer the question yourself first (short answer, then the choices), '
             'then open the fold to compare with the key and the evidence. Record findings in '
             '`review/review_sheet.csv`, or open an issue using the *Item review* template.', '']
    for r in rows:
        rev = reviews[r['concept_id']]
        lines += [f"## {r['concept_id']} · {r['task_type']}", '',
                  f"**{r['author']}, «{r['work']}»**", '', r['question'], '']
        lines += [f'- **{l}.** {r[f"mc_answer{i}"]}' for i, l in enumerate('ABCD', 1)]
        lines += ['', '<details><summary>Key, evidence and AI-review notes</summary>', '',
                  f"**Key:** {r['answer_letter']}. {r['reference_answer']}", '',
                  f"**Accepted answers:** {', '.join(json.loads(r['accepted_answers_json']))}", '',
                  f"**Explanation:** {r['explanation']}", '',
                  f"**Evidence** (OCR page ID {r['source_page']}, printed page {r['printed_page'] or 'unknown'}; "
                  f"verbatim, characters {r['evidence_start_char']}–{r['evidence_end_char']}):", '',
                  quote(r['passage']), '',
                  f"**Caveat:** {r['evidence_caveat']}", '',
                  f"**AI peer review:** `{rev['decision']}` by `{rev['reviewer']}`."]
        for key in ('issues', 'changes'):
            for item in rev.get(key) or []:
                lines.append(f'- {key[:-1]}: {item}')
        lines += ['', '</details>', '']
    return '\n'.join(lines).rstrip() + '\n'


def render():
    rows, reviews = load()
    files = {'review_sheet.csv': sheet(rows)}
    for field, title in FIELD_TITLES.items():
        files[f'items/{field}.md'] = page(field, [r for r in rows if r['field'] == field], reviews)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = render()
    if args.check:
        for name, text in files.items():
            path = OUT / name
            if not path.is_file() or path.read_text(encoding='utf-8') != text:
                raise SystemExit(f'review/{name} is stale; run scripts/make_review_pack.py')
        print(f'PASS: review pack matches data ({len(files)} files)')
        return
    (OUT / 'items').mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (OUT / name).write_text(text, encoding='utf-8', newline='')
    print(f'wrote {len(files)} files to review/')


if __name__ == '__main__':
    main()
