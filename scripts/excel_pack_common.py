"""Shared labels for the Excel review workbook and its importer (Kazakh UI, English codes)."""

SHEET_INSTR = 'Нұсқаулық'
SHEET_Q = '1 Сұрақтар'
SHEET_CHECK = '2 Тексеру'
SHEET_TIME = 'Уақыт'
NAME_CELL = 'B3'   # reviewer name on the instruction sheet
LAST_ROW = 161     # 160 items + header

FIELD_KK = {
    'linguistics_and_literary_theory': 'Тілтану және әдебиеттану',
    'psychology': 'Психология',
    'pedagogy_education': 'Педагогика',
    'biology_anatomy_physiology': 'Биология, анатомия, физиология',
    'physics': 'Физика',
    'mathematics_geometry': 'Математика (геометрия)',
    'chemistry': 'Химия',
    'agronomy_botany': 'Агрономия және ботаника',
}

YES, NO = 'Иә', 'Жоқ'
# column letter on sheet 2 -> (CSV column, {Kazakh label: English code})
CHECK_CHOICES = {
    'G': ('answer_supported_by_passage', {YES: 'yes', 'Ішінара': 'partly', NO: 'no'}),
    'H': ('single_correct_answer', {YES: 'yes', NO: 'no'}),
    'I': ('distractors_plausible', {YES: 'yes', 'Әлсіз': 'weak', NO: 'no'}),
    'J': ('stem_hints_answer', {YES: 'yes', NO: 'no'}),
    'K': ('answerable_without_the_book', {YES: 'yes', 'Мүмкін': 'maybe', NO: 'no'}),
    'L': ('kazakh_wording_ok', {YES: 'yes', NO: 'no'}),
    'M': ('ocr_affects_answer', {YES: 'yes', NO: 'no', 'Білмеймін': 'unsure'}),
    'N': ('verdict', {'Қалдыру': 'keep', 'Түзету': 'revise', 'Ауыстыру': 'replace'}),
}
