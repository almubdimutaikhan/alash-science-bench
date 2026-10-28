"""Export data/question_pairs.csv to the typed JSONL that the Hugging Face card loads.

    python3 scripts/export_hf.py            # write data/test.jsonl
    python3 scripts/export_hf.py --check    # fail if data/test.jsonl is stale

The CSV stays the canonical export. The JSONL only adds types (integers, null for
unestablished years, accepted answers as a list) so `datasets.load_dataset` does not have to
guess them. The `split` column is dropped because it would be confused with the Hub split.
Standard library only; no model inference.
"""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / 'data' / 'question_pairs.csv'
OUT = ROOT / 'data' / 'test.jsonl'
INT_COLUMNS = ['correct_answer_num', 'source_page', 'evidence_start_char', 'evidence_end_char']
NULLABLE_INT = ['original_year', 'edition_year', 'source_row']
NULLABLE_STR = ['printed_page']
DROPPED = ['split']


def convert(row):
    out = {}
    for key, value in row.items():
        if key in DROPPED:
            continue
        if key == 'accepted_answers_json':
            out['accepted_answers'] = json.loads(value)
        elif key in INT_COLUMNS:
            out[key] = int(value)
        elif key in NULLABLE_INT:
            out[key] = int(value) if value else None
        elif key in NULLABLE_STR:
            out[key] = value or None
        else:
            out[key] = value
    return out


def render():
    with CSV.open(encoding='utf-8', newline='') as f:
        rows = [convert(r) for r in csv.DictReader(f)]
    for r in rows:
        assert 1 <= r['correct_answer_num'] <= 4
        assert r['answer_letter'] == 'ABCD'[r['correct_answer_num'] - 1]
        assert r['reference_answer'] in r['accepted_answers']
        assert r[f"mc_answer{r['correct_answer_num']}"] in r['accepted_answers']
        assert r['evidence_end_char'] - r['evidence_start_char'] == len(r['passage'])
    return ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = render()
    if args.check:
        if not OUT.is_file() or OUT.read_text(encoding='utf-8') != text:
            raise SystemExit('data/test.jsonl is stale; run scripts/export_hf.py')
        print('PASS: data/test.jsonl matches data/question_pairs.csv')
    else:
        OUT.write_text(text, encoding='utf-8', newline='')
        print(f'wrote {OUT.relative_to(ROOT)} ({text.count(chr(10))} rows)')


if __name__ == '__main__':
    main()
