#!/usr/bin/env python3
"""Free downloadable spreadsheets for /habit-tracker-template and /budget-template-india.

    python3 -m venv /tmp/ss-venv && /tmp/ss-venv/bin/pip install openpyxl
    /tmp/ss-venv/bin/python scripts/make-templates.py

Writes public/templates/*.xlsx. They open in Excel, Google Sheets (File > Import) and Numbers.
Formulas only, no macros, so nothing in them can run code.
"""
import os
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as col
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.formula import ArrayFormula

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'templates')
LIME, INK, GREY, LIGHT = 'D7F64A', '10120A', '9CA3AF', 'F4F4F5'
B = Font(bold=True)
thin = Side(style='thin', color='E4E4E7')
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
CENTER = Alignment(horizontal='center', vertical='center')
HEAD = PatternFill('solid', fgColor=INK)
HEADF = Font(bold=True, color='FFFFFF')
DONE = PatternFill('solid', fgColor=LIME)
SOFT = PatternFill('solid', fgColor=LIGHT)
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
FOOT = 'Free template from selfstreak.com. Prefer reminders and automatic streaks on your phone? Try the Self Streak app, free for 7 days.'

def habit_tracker():
    wb = Workbook()
    st = wb.active; st.title = 'Start here'
    st['A1'] = 'Habit tracker 2027'; st['A1'].font = Font(bold=True, size=18)
    st['A3'] = 'Year'; st['B3'] = 2027; st['A3'].font = B; st['B3'].fill = DONE; st['B3'].font = B
    rows = ['How to use it',
            '1. Change the year in the lime cell above if you want a different year. Every month sheet updates its dates.',
            '2. Open this month’s sheet and write your habits in column A (up to 12). Start with 2 or 3, not 12.',
            '3. Each day you do a habit, type 1 in that day’s box. The box turns lime.',
            '4. Columns AH to AJ count the days done, your completion rate and your longest streak this month.',
            '5. Copy your habits to the next month’s sheet on the 1st.',
            '',
            'Tips that make it stick',
            '• Tie each habit to something you already do: “after morning chai, read 10 pages”.',
            '• Missing one day is fine. Never miss two in a row.',
            '• A study at University College London found new habits took a median of 66 days to feel automatic (Lally et al., 2010).',
            '',
            FOOT]
    for i, t in enumerate(rows, start=5):
        st[f'A{i}'] = t
        if t in ('How to use it', 'Tips that make it stick'): st[f'A{i}'].font = Font(bold=True, size=13)
    st.column_dimensions['A'].width = 110
    examples = ['Drink 8 glasses of water', 'Walk 8,000 steps', 'Read 10 pages', 'No sugar after 8 pm', 'Sleep by 11 pm']
    for m, name in enumerate(MONTHS, start=1):
        ws = wb.create_sheet(name[:3])
        ws['A1'] = f'=TEXT(DATE(\'Start here\'!$B$3,{m},1),"mmmm yyyy")'; ws['A1'].font = Font(bold=True, size=16)
        ws['A2'] = 'Type 1 on each day you did the habit.'; ws['A2'].font = Font(color=GREY, italic=True)
        ws['A3'] = 'Habit'; ws['A3'].fill = HEAD; ws['A3'].font = HEADF
        last = 32  # columns B..AF are days 1..31
        for d in range(1, 32):
            c = col(d + 1)
            ws[f'{c}3'] = f'=IF({d}<=DAY(EOMONTH(DATE(\'Start here\'!$B$3,{m},1),0)),{d},"")'
            ws[f'{c}3'].fill = HEAD; ws[f'{c}3'].font = HEADF; ws[f'{c}3'].alignment = CENTER
            ws.column_dimensions[c].width = 3.6
        for h, label in ((34, 'Done'), (35, '%'), (36, 'Best streak')):
            c = col(h); ws[f'{c}3'] = label; ws[f'{c}3'].fill = HEAD; ws[f'{c}3'].font = HEADF; ws[f'{c}3'].alignment = CENTER
        ws.column_dimensions['A'].width = 30
        for h in (34, 35, 36): ws.column_dimensions[col(h)].width = 11
        for r in range(4, 16):
            ws[f'A{r}'] = examples[r - 4] if r - 4 < len(examples) else ''
            ws[f'A{r}'].border = BOX
            for d in range(1, 32):
                cell = ws[f'{col(d + 1)}{r}']; cell.border = BOX; cell.alignment = CENTER
            rng = f'B{r}:AF{r}'
            ws[f'AH{r}'] = f'=IF(A{r}="","",COUNTIF({rng},1))'
            ws[f'AI{r}'] = f'=IF(A{r}="","",COUNTIF({rng},1)/DAY(EOMONTH(DATE(\'Start here\'!$B$3,{m},1),0)))'
            ws[f'AI{r}'].number_format = '0%'
            # Longest run of consecutive 1s in the row (array formula; works in Excel, Google Sheets and Numbers).
            ws[f'AJ{r}'] = ArrayFormula(f'AJ{r}', f'=IF(A{r}="","",MAX(FREQUENCY(IF({rng}=1,COLUMN({rng})),IF({rng}<>1,COLUMN({rng})))))')
            for c in ('AH', 'AI', 'AJ'): ws[f'{c}{r}'].alignment = CENTER; ws[f'{c}{r}'].border = BOX; ws[f'{c}{r}'].fill = SOFT
        ws.conditional_formatting.add('B4:AF15', CellIsRule(operator='equal', formula=['1'], fill=DONE))
        ws.conditional_formatting.add('B4:AF15', FormulaRule(formula=['B$3=""'], fill=PatternFill('solid', fgColor='E4E4E7')))
        dv = DataValidation(type='whole', operator='between', formula1='0', formula2='1', allow_blank=True,
                            error='Type 1 for done, or leave it empty.', errorTitle='Habit tracker', showErrorMessage=True)
        ws.add_data_validation(dv); dv.add('B4:AF15')
        ws['A17'] = FOOT; ws['A17'].font = Font(color=GREY, italic=True)
        ws.freeze_panes = 'B4'
        ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 1; ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.sheet_view.showGridLines = False
    return wb

NEEDS = ['Rent / home loan EMI', 'Groceries & household', 'Electricity, water, gas', 'Mobile & internet', 'Other EMIs', 'Transport & fuel', 'Insurance', 'School / college fees', 'Medicines & doctor']
WANTS = ['Eating out & Swiggy/Zomato', 'Shopping & clothes', 'Movies & outings', 'Subscriptions (OTT, apps)', 'Travel', 'Gifts & festivals']
SAVE = ['SIP / mutual funds', 'Emergency fund', 'PPF / EPF top-up', 'Extra loan or card payment']

def budget_india():
    wb = Workbook()
    ws = wb.active; ws.title = 'Budget'
    ws['A1'] = 'Monthly budget (₹)'; ws['A1'].font = Font(bold=True, size=18)
    ws['A2'] = 'Fill the lime cells. Actuals fill in from the Expenses sheet.'; ws['A2'].font = Font(color=GREY, italic=True)
    ws['A4'] = 'Take-home salary'; ws['A5'] = 'Other income'; ws['A6'] = 'Total income'
    ws['B4'] = 75000; ws['B5'] = 0; ws['B6'] = '=B4+B5'
    for r in (4, 5): ws[f'B{r}'].fill = DONE
    ws['A6'].font = B; ws['B6'].font = B
    for r in (4, 5, 6): ws[f'B{r}'].number_format = '₹#,##,##0'
    # 50/30/20 summary
    ws['D3'] = 'Bucket'; ws['E3'] = 'Target (50/30/20)'; ws['F3'] = 'Budgeted'; ws['G3'] = 'Spent'; ws['H3'] = 'Share of income'
    for c in 'DEFGH': ws[f'{c}3'].fill = HEAD; ws[f'{c}3'].font = HEADF
    r0 = 10
    sections = [('Needs', NEEDS, 0.5), ('Wants', WANTS, 0.3), ('Savings & extra debt payments', SAVE, 0.2)]
    r = r0
    ws[f'A{r - 1}'] = 'Category'; ws[f'B{r - 1}'] = 'Budget'; ws[f'C{r - 1}'] = 'Spent'
    for c in 'ABC': ws[f'{c}{r - 1}'].fill = HEAD; ws[f'{c}{r - 1}'].font = HEADF
    summary = []
    for name, items, pct in sections:
        ws[f'A{r}'] = name; ws[f'A{r}'].font = Font(bold=True, size=12); r += 1
        start = r
        for it in items:
            ws[f'A{r}'] = it; ws[f'B{r}'].fill = DONE
            ws[f'C{r}'] = f"=SUMIF(Expenses!$C:$C,A{r},Expenses!$D:$D)"
            for c in 'BC': ws[f'{c}{r}'].number_format = '₹#,##,##0'
            for c in 'ABC': ws[f'{c}{r}'].border = BOX
            r += 1
        summary.append((name, pct, start, r - 1)); r += 1
    defaults = {'Rent / home loan EMI': 18000, 'Groceries & household': 7000, 'Electricity, water, gas': 2000, 'Mobile & internet': 1000,
                'Other EMIs': 5000, 'Transport & fuel': 3000, 'Insurance': 1500, 'Eating out & Swiggy/Zomato': 4000, 'Shopping & clothes': 3000,
                'Movies & outings': 1500, 'Subscriptions (OTT, apps)': 700, 'Travel': 2000, 'Gifts & festivals': 1500,
                'SIP / mutual funds': 8000, 'Emergency fund': 4000, 'PPF / EPF top-up': 1000, 'Extra loan or card payment': 2000}
    for row in ws.iter_rows(min_row=r0, max_row=r, max_col=2):
        a, b = row
        if a.value in defaults: b.value = defaults[a.value]
    for i, (name, pct, s, e) in enumerate(summary, start=4):
        ws[f'D{i}'] = name.split(' &')[0]; ws[f'E{i}'] = f'=$B$6*{pct}'; ws[f'F{i}'] = f'=SUM(B{s}:B{e})'; ws[f'G{i}'] = f'=SUM(C{s}:C{e})'
        ws[f'H{i}'] = f'=IF($B$6=0,"",G{i}/$B$6)'; ws[f'H{i}'].number_format = '0%'
        for c in 'EFG': ws[f'{c}{i}'].number_format = '₹#,##,##0'
        for c in 'DEFGH': ws[f'{c}{i}'].border = BOX
    ws['D7'] = 'Left to spend'; ws['D7'].font = B; ws['G7'] = '=B6-SUM(G4:G6)'; ws['G7'].number_format = '₹#,##,##0'; ws['G7'].font = B
    ws.conditional_formatting.add('G4:G5', FormulaRule(formula=['G4>F4'], font=Font(color='DC2626', bold=True)))
    ws.conditional_formatting.add(f'C{r0}:C{r}', FormulaRule(formula=[f'AND(B{r0}>0,C{r0}>B{r0})'], font=Font(color='DC2626', bold=True)))
    ws[f'A{r + 1}'] = FOOT; ws[f'A{r + 1}'].font = Font(color=GREY, italic=True)
    for c, w in zip('ABCDEFGH', (32, 13, 13, 4 + 14, 18, 13, 13, 15)): ws.column_dimensions[c].width = w
    ws.sheet_view.showGridLines = False
    # Expenses log
    ex = wb.create_sheet('Expenses')
    for c, h, w in zip('ABCDE', ('Date', 'What', 'Category', 'Amount (₹)', 'Paid by'), (12, 30, 30, 13, 12)):
        ex[f'{c}1'] = h; ex[f'{c}1'].fill = HEAD; ex[f'{c}1'].font = HEADF; ex.column_dimensions[c].width = w
    lists = wb.create_sheet('Lists'); lists.sheet_state = 'hidden'
    cats = NEEDS + WANTS + SAVE
    for i, c in enumerate(cats, start=1): lists[f'A{i}'] = c
    for i, m in enumerate(['UPI', 'Card', 'Cash', 'Net banking', 'Auto-debit'], start=1): lists[f'B{i}'] = m
    dv = DataValidation(type='list', formula1=f'=Lists!$A$1:$A${len(cats)}', allow_blank=True); ex.add_data_validation(dv); dv.add('C2:C1000')
    dv2 = DataValidation(type='list', formula1='=Lists!$B$1:$B$5', allow_blank=True); ex.add_data_validation(dv2); dv2.add('E2:E1000')
    sample = [('Groceries & household', 'Big Basket order', 2140, 'UPI'), ('Eating out & Swiggy/Zomato', 'Swiggy dinner', 450, 'UPI'),
              ('Transport & fuel', 'Petrol', 600, 'Card'), ('Mobile & internet', 'Mobile recharge', 349, 'UPI')]
    for i, (cat, what, amt, how) in enumerate(sample, start=2):
        ex[f'A{i}'] = f'=DATE(2027,1,{i - 1})'; ex[f'A{i}'].number_format = 'dd mmm'
        ex[f'B{i}'] = what; ex[f'C{i}'] = cat; ex[f'D{i}'] = amt; ex[f'E{i}'] = how
    for i in range(2, 1001): ex[f'D{i}'].number_format = '₹#,##,##0'
    ex['G1'] = 'Delete the 4 sample rows and add your own. Pick the category from the list so it adds up on the Budget sheet.'
    ex['G1'].font = Font(color=GREY, italic=True)
    ex.freeze_panes = 'A2'
    return wb

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('self-streak-habit-tracker-2027.xlsx', habit_tracker), ('self-streak-monthly-budget-india.xlsx', budget_india)):
        p = os.path.join(OUT, name); fn().save(p); print(f'templates/{name}  {os.path.getsize(p):,} bytes')
