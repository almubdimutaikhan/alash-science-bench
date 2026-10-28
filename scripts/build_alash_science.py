"""Build and validate the Alash science question dataset. No model inference.

    python3 scripts/build_alash_science.py --check
    python3 scripts/build_alash_science.py --check --sources-root /path/to/private/sources
    python3 scripts/build_alash_science.py --sources-root /path/to/private/sources

Draft JSONL items (source/drafts) are the editable source. Independent review records
(source/reviews) are required for every item. data/question_pairs.csv is a deterministic
export, not a model benchmark result.

The OCR books and terminology workbooks are not redistributed. Without --sources-root the
script runs in offline mode: every check that needs only the repository still runs, and the
page-derived columns (page hash and evidence offsets) are taken from the committed CSV and
cross-checked against the passage length. Rebuilding (no --check) requires the sources,
because page hashes and offsets cannot be recomputed without them.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import random
import re
import unicodedata
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / 'source' / 'drafts'
REVIEWS = ROOT / 'source' / 'reviews'
CSV = ROOT / 'data' / 'question_pairs.csv'
MANIFEST = ROOT / 'data' / 'manifest.json'
SEED = 20261025
FIELD_ORDER = [
    'linguistics_and_literary_theory', 'psychology', 'pedagogy_education',
    'biology_anatomy_physiology', 'physics', 'mathematics_geometry',
    'chemistry', 'agronomy_botany',
]
AUTHORS = {
    'linguistics_psychology': 'linguistics_psychology',
    'biology_physics': 'biology_physics',
    'math_chemistry': 'math_chemistry',
    'pedagogy_agronomy': 'root',
}
COLUMNS = [
    'id', 'concept_id', 'field', 'subfield', 'task_family', 'task_type', 'short_question',
    'question', 'reference_answer', 'accepted_answers_json',
    'mc_answer1', 'mc_answer2', 'mc_answer3', 'mc_answer4',
    'correct_answer_num', 'answer_letter', 'passage', 'explanation',
    'author', 'work', 'original_year', 'edition_year',
    'source_ocr', 'source_page', 'printed_page', 'source_workbook',
    'source_sheet', 'source_row', 'source_page_sha256',
    'evidence_start_char', 'evidence_end_char', 'source_group_id',
    'split', 'review_status', 'reviewer', 'human_review_status',
    'scan_review_status', 'evidence_caveat', 'language',
]
TASK_FAMILIES = {
    'historical_term_recall': 'term_recall', 'concept_to_term': 'term_recall',
    'term_to_concept': 'concept_identification', 'historical_term_meaning': 'concept_identification',
    'historical_concept_definition': 'concept_identification',
    'historical_concept_explanation': 'scientific_explanation',
    'concept_properties': 'scientific_explanation', 'term_to_function': 'scientific_explanation',
    'historical_classification': 'scientific_explanation', 'term_composition': 'scientific_explanation',
    'scholarly_argument': 'scholarly_discourse', 'teaching_method': 'scholarly_discourse',
    'source_understanding': 'scholarly_discourse', 'source_claim': 'scholarly_discourse',
}
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def item_sha(item):
    content = {k: v for k, v in item.items() if k != 'review_status' and not k.startswith('_')}
    return sha(json.dumps(content, ensure_ascii=False, sort_keys=True, separators=(',', ':')))


def norm(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text).casefold()).strip()


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_sources():
    items, reviews, source_files = [], {}, []
    for path in sorted(DRAFTS.glob('*.jsonl')):
        source_files.append(path)
        for item in read_jsonl(path):
            item['_author_agent'] = AUTHORS[path.stem]
            items.append(item)
    for path in sorted(REVIEWS.glob('*_review.jsonl')):
        source_files.append(path)
        for review in read_jsonl(path):
            cid = review['concept_id']
            require(cid not in reviews, f'Duplicate peer review: {cid}')
            reviews[cid] = review
    return items, reviews, source_files


def workbook_row_numbers(path):
    """Read row identifiers only; scientific evidence is verified in the OCR."""
    with zipfile.ZipFile(path) as z:
        names = [s.get('name') for s in ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet', NS)]
        files = sorted(n for n in z.namelist() if re.fullmatch(r'xl/worksheets/sheet\d+\.xml', n))
        return {name: {int(r.get('r')) for r in ET.fromstring(z.read(f)).findall('m:sheetData/m:row', NS)} for name, f in zip(names, files)}


def compile_rows(items, reviews, sources_root=None, committed=None):
    counts = Counter(r['field'] for r in items)
    require(set(counts) == set(FIELD_ORDER), f'Unexpected fields: {counts}')
    require(all(counts[f] == 20 for f in FIELD_ORDER), f'Expected 20 concepts per field: {counts}')
    require(len(items) == 160, f'Expected 160 pairs, got {len(items)}')
    ids = [r['concept_id'] for r in items]
    require(len(ids) == len(set(ids)), 'Duplicate concept IDs')
    require(set(ids) == set(reviews), 'Every concept must have exactly one independent peer review')
    page_cache, workbook_cache, rows = {}, {}, []
    committed = committed or {}
    question_seen, by_field = set(), defaultdict(list)
    for item in items:
        by_field[item['field']].append(item)
    for field in FIELD_ORDER:
        rng = random.Random(f'{SEED}:{field}')
        positions = list(range(4)) * 5
        rng.shuffle(positions)
        for item, target in zip(sorted(by_field[field], key=lambda r: r['concept_id']), positions):
            cid = item['concept_id']
            review = reviews[cid]
            require(review['reviewer'] != item['_author_agent'], f'{cid}: self-review is not independent')
            require(review['decision'] in ('pass', 'revised'), f'{cid}: peer review not passed')
            require(not review.get('unresolved'), f'{cid}: unresolved peer review findings')
            require(review.get('reviewed_item_sha256') == item_sha(item), f'{cid}: content changed since review; obtain a fresh review')
            require(item['review_status'] == 'ai_peer_reviewed', f'{cid}: item not marked peer reviewed')
            for key in ['short_question', 'mcq_question', 'reference_answer', 'evidence_passage', 'author', 'work']:
                require(isinstance(item.get(key), str) and item[key].strip(), f'{cid}: missing {key}')
            require(norm(item['short_question']) == norm(item['mcq_question']), f'{cid}: formats must use the same question stem')
            qkey = norm(item['short_question'])
            require(qkey not in question_seen, f'{cid}: duplicate question')
            question_seen.add(qkey)
            choices = item['choices']
            require(len(choices) == 4 and len({norm(s) for s in choices}) == 4, f'{cid}: four unique options required')
            correct = item['correct_choice']
            require(isinstance(correct, int) and 0 <= correct < 4, f'{cid}: invalid answer index')
            aliases = item['accepted_answers']
            require(isinstance(aliases, list) and aliases and all(isinstance(a, str) and a.strip() for a in aliases), f'{cid}: invalid accepted answers')
            require(item['reference_answer'] in aliases, f'{cid}: canonical answer absent from accepted answers')
            require(choices[correct] in aliases, f'{cid}: correct MCQ option absent from accepted answers')
            require(sum(norm(c) in {norm(a) for a in aliases} for c in choices) == 1, f'{cid}: alias collides with a distractor')
            row_num = item.get('source_row')
            if sources_root is not None:
                path = sources_root / item['source_ocr']
                require(path.is_file(), f'{cid}: missing OCR source')
                if path not in page_cache:
                    records = json.loads(path.read_text())
                    require(len({r['page'] for r in records}) == len(records), f'{cid}: duplicate page IDs')
                    page_cache[path] = {r['page']: r['text'] for r in records}
                require(item['source_page'] in page_cache[path], f'{cid}: missing page ID')
                page = page_cache[path][item['source_page']]
                passage = item['evidence_passage']
                require(passage in page, f'{cid}: passage not verbatim in original OCR page')
                start = page.index(passage)
                page_hash, start_char = sha(page), start
                wp = sources_root / item['source_workbook']
                require(wp.is_file(), f'{cid}: missing workbook')
                if row_num is not None:
                    if wp not in workbook_cache:
                        workbook_cache[wp] = workbook_row_numbers(wp)
                    require(int(row_num) in workbook_cache[wp].get(item['source_sheet'], set()), f'{cid}: missing worksheet row')
            else:
                old = committed.get(f'ALASH_{cid}')
                require(old is not None, f'{cid}: offline mode needs the committed CSV row (rebuild with --sources-root)')
                passage = item['evidence_passage']
                page_hash, start_char = old['source_page_sha256'], int(old['evidence_start_char'])
                require(int(old['evidence_end_char']) - start_char == len(passage), f'{cid}: evidence offsets disagree with passage length')
                require(old['passage'] == passage, f'{cid}: passage differs from committed export')
            require(40 <= len(passage) <= 6000, f'{cid}: suspicious evidence length {len(passage)}')
            require(not re.search(r"I (am sorry|cannot)|I'm sorry|no discernible text", passage, re.I), f'{cid}: OCR processing artifact')
            start = start_char
            answer = choices[correct]
            others = [v for i, v in enumerate(choices) if i != correct]
            rng.shuffle(others)
            options = others[:target] + [answer] + others[target:]
            # Group the whole supplied volume conservatively; no split is assigned yet.
            group = 'SRC_' + sha(item['source_ocr'])[:12]
            row = {
                'id': 'ALASH_' + cid, 'concept_id': cid, 'field': field,
                'subfield': item.get('subfield', ''),
                'task_family': TASK_FAMILIES[item['task_type']], 'task_type': item['task_type'],
                'short_question': item['short_question'], 'question': item['mcq_question'],
                'reference_answer': item['reference_answer'],
                'accepted_answers_json': json.dumps(aliases, ensure_ascii=False),
                **{f'mc_answer{i+1}': v for i, v in enumerate(options)},
                'correct_answer_num': str(target + 1), 'answer_letter': 'ABCD'[target],
                'passage': passage, 'explanation': item['explanation'],
                'author': item['author'], 'work': item['work'],
                'original_year': str(item.get('original_year') or ''),
                'edition_year': str(item.get('edition_year') or ''),
                'source_ocr': item['source_ocr'], 'source_page': str(item['source_page']),
                'printed_page': str(item.get('printed_page') or ''),
                'source_workbook': item['source_workbook'], 'source_sheet': item['source_sheet'],
                'source_row': str(row_num) if row_num is not None else '',
                'source_page_sha256': page_hash, 'evidence_start_char': str(start),
                'evidence_end_char': str(start + len(passage)), 'source_group_id': group,
                'split': 'unassigned_pilot', 'review_status': 'ai_peer_reviewed_needs_human',
                'reviewer': review['reviewer'], 'human_review_status': 'pending',
                'scan_review_status': 'pending_original_scans',
                'evidence_caveat': item['evidence_caveat'], 'language': 'kk',
            }
            require(set(row) == set(COLUMNS), f'{cid}: CSV schema drift')
            rows.append(row)
    return rows


def csv_string(rows):
    import io
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=COLUMNS, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    value = buffer.getvalue()
    require(list(csv.DictReader(io.StringIO(value))) == rows, 'CSV round-trip changed data')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='validate committed export without writing files')
    parser.add_argument('--sources-root', type=Path, help='folder containing the private OCR books and workbooks (paths in source_ocr are relative to it)')
    args = parser.parse_args()
    sources_root = args.sources_root.resolve() if args.sources_root else None
    require(sources_root is not None or args.check, 'Rebuilding needs --sources-root; use --check for offline validation')
    items, reviews, source_files = load_sources()
    committed = {r['id']: r for r in csv.DictReader(CSV.open(encoding='utf-8', newline=''))} if CSV.is_file() else {}
    rows = compile_rows(items, reviews, sources_root, committed)
    output = csv_string(rows)
    counts = Counter(r['field'] for r in rows)
    positions = {field: dict(Counter(r['answer_letter'] for r in rows if r['field'] == field)) for field in FIELD_ORDER}
    require(all(set(c) == set('ABCD') and set(c.values()) == {5} for c in positions.values()), 'Unbalanced answer positions')
    stats = {
        'dataset_version': '0.1.0-local-draft', 'created_date': '2026-10-25',
        'pairs': len(rows), 'question_prompts': 2 * len(rows), 'fields': dict(counts),
        'csv_columns': COLUMNS, 'csv_sha256': sha(output), 'shuffle_seed': SEED,
        'answer_positions_by_field': positions,
        'source_volumes': len({r['source_ocr'] for r in rows}),
        'source_pages': len({(r['source_ocr'], r['source_page']) for r in rows}),
        'task_families': dict(Counter(r['task_family'] for r in rows)),
        'peer_reviewed_items': len(reviews),
        'peer_review_revised_items': sum(r['decision'] == 'revised' for r in reviews.values()),
        'human_review_status': 'pending', 'scan_review_status': 'pending_original_scans',
        'distribution_rights': 'not_assessed_do_not_publish_as_licensed',
        'benchmark_executed': False, 'model_inference_executed': False,
        'source_files_sha256': {str(p.relative_to(ROOT)): sha(p.read_text()) for p in source_files},
    }
    if args.check:
        require(CSV.read_text() == output, 'CSV differs from current reviewed sources; rebuild')
        require(json.loads(MANIFEST.read_text()) == stats, 'Manifest differs; rebuild')
    else:
        CSV.write_text(output, encoding='utf-8', newline='')
        MANIFEST.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: stats[k] for k in ['pairs', 'question_prompts', 'fields', 'source_volumes', 'source_pages', 'peer_reviewed_items', 'peer_review_revised_items', 'benchmark_executed']}, ensure_ascii=False, indent=2))
    scope = 'exact source evidence against OCR' if sources_root else 'OFFLINE mode, OCR evidence not re-verified'
    print(f'PASS ({scope}): schema, independent reviews, CSV round-trip, balanced keys, deterministic export.')


if __name__ == '__main__':
    main()
