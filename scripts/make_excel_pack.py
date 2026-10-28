"""Build the Excel workbook for a Kazakh-speaking reviewer who does not use code.

    python3 scripts/make_excel_pack.py OUTPUT_DIR

Needs openpyxl (`pip install openpyxl`); the other scripts do not. Writes
OUTPUT_DIR/Alash_review.xlsx and a short read-me. Keep OUTPUT_DIR outside the repository.
The workbook is derived from data/question_pairs.csv; the interface is Kazakh with English glosses.
"""
import csv
import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Protection, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, str(Path(__file__).resolve().parent))
from excel_pack_common import *  # noqa: E402,F403

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / 'data' / 'question_pairs.csv'
FIELD_ORDER = list(FIELD_KK)
PILOT_POSITIONS = (4, 14)   # 5th and 15th item of each field -> 16 pilot items

HEADER_FILL = PatternFill('solid', fgColor='1F3864')
INPUT_FILL = PatternFill('solid', fgColor='FFF2CC')
KEY_FILL = PatternFill('solid', fgColor='E2EFDA')
PILOT_FILL = PatternFill('solid', fgColor='FCE4D6')
WRAP = Alignment(wrap_text=True, vertical='top')
THIN = Side(style='thin', color='BFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
UNLOCKED = Protection(locked=False)


def header(ws, labels, widths):
    ws.append(labels)
    for i, (label, width) in enumerate(zip(labels, widths), 1):
        c = ws.cell(row=1, column=i)
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = HEADER_FILL
        c.alignment = Alignment(wrap_text=True, vertical='center')
        ws.column_dimensions[c.column_letter].width = width
    ws.row_dimensions[1].height = 62
    ws.freeze_panes = 'C2'


def style_body(ws, input_cols):
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for c in row:
            c.alignment = WRAP
            c.border = BORDER
            if c.column_letter in input_cols:
                c.fill = INPUT_FILL
                c.protection = UNLOCKED


def protect(ws):
    ws.protection.sheet = True          # no password: stops accidental edits only
    ws.protection.formatColumns = False  # still allow resizing columns/rows and filtering
    ws.protection.formatRows = False
    ws.protection.autoFilter = False
    ws.protection.sort = False


def dropdown(ws, col, labels):
    dv = DataValidation(type='list', formula1='"' + ','.join(labels) + '"', allow_blank=True,
                        showErrorMessage=True, errorTitle='Тізімнен таңдаңыз',
                        error='Ашылмалы тізімнен таңдаңыз / Please pick from the list.')
    ws.add_data_validation(dv)
    dv.add(f'{col}2:{col}{LAST_ROW}')


def instructions(wb):
    ws = wb.active
    ws.title = SHEET_INSTR
    ws.column_dimensions['A'].width = 95
    ws.column_dimensions['B'].width = 75
    rows = [
        ('Алаш еңбектеріндегі ғылыми терминдер: сұрақтарды тексеру', 'Alash scientific terminology: question review', 'title'),
        ('', '', None),
        ('Тексерушінің аты-жөні (осы жерге жазыңыз) →', '', 'name'),
        ('', '', None),
        ('Бұл не?', 'What is this?', 'h'),
        ('Мұнда 1920–30 жылдардағы Алаш зиялыларының оқулықтары мен ғылыми еңбектерінен жасалған 160 сұрақ бар (8 сала, әр салада 20). Сұрақтарды жасанды интеллект жазып, басқа жасанды интеллект тексерген. Бірақ әзірге бірде-бір адам тексерген жоқ. Сіздің міндетіңіз — қазақ тілінің маманы ретінде әр сұрақтың сапасын бағалау.',
         '160 questions made from textbooks and scholarly works of Alash intellectuals of the 1920s–30s (8 fields, 20 each). One AI wrote the questions and another AI checked them, but no person has checked them yet. Your job is to judge the quality of each question as a Kazakh-language specialist.', None),
        ('', '', None),
        ('Қалай жұмыс істейсіз?', 'How to work', 'h'),
        ('1. «1 Сұрақтар» парағын ашыңыз. Әр сұрақты оқып, таңдау нұсқаларына қарамай, өз жауабыңызды қысқаша жазыңыз. Содан кейін A, B, C, D-ның бірін таңдаңыз. Дұрыс жауапты әлі қарамаңыз!',
         '1. Open sheet "1 Сұрақтар". Read each question and write your own short answer without looking at the options. Then pick A, B, C or D. Do not look at the key yet!', None),
        ('2. Одан кейін «2 Тексеру» парағына өтіңіз. Онда дұрыс жауап пен кітаптан алынған үзінді бар. Сары ұяшықтарды толтырыңыз: бәрі ашылмалы тізімнен таңдалады, тек соңғы баған — еркін жазу.',
         '2. Then go to sheet "2 Тексеру". It shows the key and the passage from the book. Fill the yellow cells: all are drop-down lists except the last column, which is free text.', None),
        ('3. Әр сұраққа «Шешім» беріңіз: Қалдыру — сұрақ жақсы; Түзету — аздап өзгерту керек (не өзгеретінін «Ескертпе» бағанына дәл жазыңыз); Ауыстыру — бұл факт сұраққа жарамайды.',
         '3. Give every question a "Шешім" (decision): Қалдыру = keep as is; Түзету = needs a small change (say exactly what in the notes column); Ауыстыру = this fact is unsuitable, replace it.', None),
        ('4. Әр жұмыс сеансында «Уақыт» парағына күнін, басталу және аяқталу уақытын жазыңыз (мысалы, 14:30 және 16:00).',
         '4. In each work session, write the date, start time and end time on sheet "Уақыт" (for example 14:30 and 16:00).', None),
        ('5. Алдымен «Пилот» бағанында P белгісі бар 16 сұрақты жасап, файлды маған жіберіңіз. Тек соларды көру үшін: «1 Сұрақтар» парағында «Пилот» бағанындағы сүзгі (сүзгі белгісі) арқылы P таңдаңыз. Содан кейін қалғанын жалғастыруға болады.',
         '5. First do only the 16 questions marked P in the "Пилот" column and send me the file. To see only those, use the filter arrow on the "Пилот" column and pick P. Then continue with the rest.', None),
        ('6. Бітіргенде файлды сақтап (Ctrl+S), өзгертпей мен берген атпен жіберіңіз.',
         '6. When you finish, save the file (Ctrl+S) and send it back under the same name.', None),
        ('', '', None),
        ('Бағандардағы сұрақтар (2 Тексеру парағы)', 'What each column asks (sheet 2)', 'h'),
        ('G. Үзінді дұрыс жауапты растай ма? Иә / Ішінара / Жоқ', 'G. Does the passage support the key? Yes / Partly / No', None),
        ('H. Төрт нұсқаның ішінде дұрыс жауап тек біреу ме? (басқа нұсқаны да қорғауға бола ма?)', 'H. Is exactly one option correct? (could another option also be defended?)', None),
        ('I. Қате нұсқалар сенімді ме? Иә / Әлсіз / Жоқ (әлсіз = тақырыпты білмей-ақ алып тастауға болады)', 'I. Are the wrong options plausible? Yes / Weak / No (weak = can be dismissed without knowing the topic)', None),
        ('J. Сұрақтағы сөз жауапты аңғартып тұр ма? Иә = аңғартады (мысалы, сұрақта жауаптың түбірі бар)', 'J. Does a word in the question give the answer away? Yes = it does (e.g. the question contains the root of the answer)', None),
        ('K. Осы кітаптарды оқымай, жалпы білімнен жауап беруге бола ма? Иә / Мүмкін / Жоқ', 'K. Could someone answer from general knowledge without these books? Yes / Maybe / No', None),
        ('L. Қазақша тұжырым табиғи әрі түсінікті ме?', 'L. Is the Kazakh wording natural and clear?', None),
        ('M. Үзіндідегі OCR қатесі жауапқа әсер ете ме? Иә / Жоқ / Білмеймін', 'M. Does an OCR error in the passage affect the answer? Yes / No / Not sure', None),
        ('', '', None),
        ('Назар аударыңыз', 'Please note', 'h'),
        ('• Үзінді — кітап бетінің компьютер таныған мәтіні (OCR). Тану қателері болады. Тарихи емле (мысалы, «пајдаланады», «тексерүтүн») сұрақтың қатесі емес. Тек қате жауапқа әсер ететін болса ғана M бағанына «Иә» деп белгілеңіз.',
         '• The passage is machine-recognised (OCR) text of a book page and has recognition errors. Historical spelling is not a flaw in the question. Mark M "Yes" only if an error changes what the answer should be.', None),
        ('• Сұрақ «автор осы еңбекте қалай дейді?» деп сұрайды. Қазіргі ғылым бойынша дұрыс-бұрыстығын емес, үзіндіге сәйкестігін және тіл сапасын бағалайсыз.',
         '• Each question asks "what does this author say in this work?". You judge fit to the passage and language quality, not whether it matches current science.', None),
        ('• Физика, химия, биология, геометрия, агрономия сұрақтарында ғылыми дәлдікті бағалай алмасаңыз — қиналмаңыз. Тіл мен үзіндіге сәйкестікті ғана бағалап, ескертпеге «маман керек» деп жазыңыз.',
         '• For physics, chemistry, biology, geometry and agronomy, if you cannot judge scientific accuracy, that is fine. Judge language and passage fit only, and write "specialist needed" in the notes.', None),
        ('• Келіспеушілік пен күмән маңызды: жасырмаңыз, ескертпеге жазыңыз. Сұрақ қате болса, ол — нәтиже.',
         '• Doubts and disagreements are valuable. Write them in the notes. A flawed question is a finding, not a failure.', None),
        ('• Сары емес ұяшықтар қорғалған (кездейсоқ өшіріп алмау үшін). Қажет болса, ұяшық енін өзгертуге болады.',
         '• Cells that are not yellow are locked so nothing is deleted by accident. You can still resize columns and rows.', None),
        ('', '', None),
        ('Жұмыс барысы', 'Progress', 'h'),
        (f'=\"1-қадам: жауап берілген сұрақ  \"&COUNTA(\'{SHEET_Q}\'!J2:J{LAST_ROW})&\" / 160\"', '', None),
        (f'=\"2-қадам: шешім берілген сұрақ  \"&COUNTA(\'{SHEET_CHECK}\'!N2:N{LAST_ROW})&\" / 160\"', '', None),
        (f'=\"Жұмсалған уақыт (сағат)  \"&ROUND(SUM(\'{SHEET_TIME}\'!D2:D200),1)', '', None),
    ]
    for kk, en, kind in rows:
        ws.append([kk, en])
        r = ws.max_row
        for c in ws[r]:
            c.alignment = WRAP
        if kind == 'title':
            ws.cell(r, 1).font = Font(bold=True, size=16)
            ws.cell(r, 2).font = Font(italic=True, size=12)
        elif kind == 'h':
            for c in ws[r]:
                c.font = Font(bold=True, size=12)
                c.fill = KEY_FILL
        elif kind == 'name':
            ws.cell(r, 1).font = Font(bold=True)
            ws.cell(r, 2).fill = INPUT_FILL
            ws.cell(r, 2).protection = UNLOCKED
            assert ws.cell(r, 2).coordinate == NAME_CELL, ws.cell(r, 2).coordinate
    protect(ws)
    return ws


def build(rows, out):
    wb = Workbook()
    instructions(wb)

    q = wb.create_sheet(SHEET_Q)
    header(q, ['ID', 'Сала\nField', 'Автор, еңбек\nAuthor, work', 'Сұрақ\nQuestion',
               'A', 'B', 'C', 'D',
               'Сіздің қысқа жауабыңыз\n(нұсқаларға қарамай)\nYour short answer',
               'Таңдауыңыз\nA / B / C / D', 'Пилот\nPilot'],
           [14, 20, 28, 60, 26, 26, 26, 26, 34, 13, 8])
    c = wb.create_sheet(SHEET_CHECK)
    header(c, ['ID', 'Сұрақ\nQuestion', 'Дұрыс жауап (кілт)\nKey', 'Қабылданатын баламалар\nAccepted variants',
               'Кітаптан үзінді (OCR)\nPassage from the book', 'Бет\nPage (OCR / printed)',
               'G. Үзінді кілтті растай ма?\nPassage supports key?', 'H. Дұрыс жауап тек біреу ме?\nExactly one correct?',
               'I. Қате нұсқалар сенімді ме?\nPlausible distractors?', 'J. Сұрақ жауапты аңғартып тұр ма?\nQuestion hints the answer?',
               'K. Кітапсыз жауап беруге бола ма?\nAnswerable without the book?', 'L. Қазақша тұжырым табиғи ма?\nWording natural?',
               'M. OCR қатесі жауапқа әсер ете ме?\nOCR error affects answer?', 'Шешім\nDecision',
               'Ескертпе: не өзгерту керек?\nNotes: what to change?'],
           [14, 45, 28, 24, 80, 13, 15, 15, 15, 15, 15, 15, 15, 14, 50])

    ordered = []
    for field in FIELD_ORDER:
        ordered += [r for r in rows if r['field'] == field]
    pilot = set()
    for field in FIELD_ORDER:
        items = [r for r in ordered if r['field'] == field]
        pilot |= {items[i]['id'] for i in PILOT_POSITIONS}
    assert len(ordered) == 160 and len(pilot) == 16

    for r in ordered:
        q.append([r['id'], FIELD_KK[r['field']], f"{r['author']}, «{r['work']}»", r['question'],
                  r['mc_answer1'], r['mc_answer2'], r['mc_answer3'], r['mc_answer4'], '', '',
                  'P' if r['id'] in pilot else ''])
        key = f"{r['answer_letter']}. {r['reference_answer']}"
        aliases = '; '.join(a for a in json.loads(r['accepted_answers_json']) if a != r['reference_answer'])
        page = f"OCR {r['source_page']}" + (f" / баспа {r['printed_page']}" if r['printed_page'] else '')
        c.append([r['id'], r['question'], key, aliases, r['passage'], page] + [''] * 9)
    style_body(q, {'I', 'J'})
    style_body(c, set('GHIJKLMN') | {'O'})
    for row in range(2, LAST_ROW + 1):
        if q.cell(row, 11).value == 'P':
            q.cell(row, 11).fill = PILOT_FILL
        c.cell(row, 3).fill = KEY_FILL
    dropdown(q, 'J', ['A', 'B', 'C', 'D'])
    for col, (_, mapping) in CHECK_CHOICES.items():
        dropdown(c, col, list(mapping))
    q.auto_filter.ref = f'A1:K{LAST_ROW}'
    c.auto_filter.ref = f'A1:O{LAST_ROW}'
    protect(q)
    protect(c)

    t = wb.create_sheet(SHEET_TIME)
    header(t, ['Күні\nDate', 'Басталуы\nStart (hh:mm)', 'Аяқталуы\nEnd (hh:mm)', 'Сағат\nHours', 'Не істелді?\nWhat was done?'],
           [14, 16, 16, 12, 60])
    t.freeze_panes = 'A2'
    for row in range(2, 201):
        t.cell(row, 4).value = f'=IF(AND(ISNUMBER(B{row}),ISNUMBER(C{row})),ROUND((C{row}-B{row})*24,2),"")'
        for col in (1, 2, 3, 5):
            t.cell(row, col).fill = INPUT_FILL
        t.cell(row, 1).number_format = 'dd.mm.yyyy'
        t.cell(row, 2).number_format = 'hh:mm'
        t.cell(row, 3).number_format = 'hh:mm'
        t.cell(row, 4).number_format = '0.00'
    wb.save(out)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    out_dir = Path(sys.argv[1])
    if ROOT in out_dir.resolve().parents or out_dir.resolve() == ROOT:
        raise SystemExit('Write the pack outside the repository.')
    out_dir.mkdir(parents=True, exist_ok=True)
    with CSV.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    build(rows, out_dir / 'Alash_review.xlsx')
    print('wrote', out_dir / 'Alash_review.xlsx')


if __name__ == '__main__':
    main()
