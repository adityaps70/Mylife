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
    """12 month sheets + a year overview. Tick a day by picking ✓ from the cell's drop-down (or typing x, 1 or ✓;
    in Google Sheets you can also turn the grid into real checkboxes). Any mark counts as done; FALSE checkboxes don't."""
    from openpyxl.formatting.rule import ColorScaleRule, DataBarRule
    from openpyxl.styles import Alignment
    wb = Workbook()
    TICK = '✓'
    MUTED, ROWA, WEEKEND, LINE = '71717A', 'FAFAFA', 'EEF2E3', 'E4E4E7'
    line = Side(style='thin', color=LINE)
    grid = Border(left=line, right=line, top=line, bottom=line)
    YEAR = "'Start here'!$C$4"
    # ---------- Start here ----------
    st = wb.active; st.title = 'Start here'; st.sheet_view.showGridLines = False
    st.column_dimensions['A'].width = 3; st.column_dimensions['B'].width = 4; st.column_dimensions['C'].width = 10; st.column_dimensions['D'].width = 92
    st['B2'] = 'Habit tracker'; st['B2'].font = Font(bold=True, size=26, color=INK)
    st['B4'] = 'Year'; st['B4'].font = Font(bold=True, color=MUTED)
    st['C4'] = 2027; st['C4'].font = Font(bold=True, size=14); st['C4'].fill = DONE; st['C4'].alignment = CENTER
    st['D4'] = '← change the year and every month updates'; st['D4'].font = Font(italic=True, color=MUTED)
    steps = [('1', 'Open this month’s tab (Jan–Dec at the bottom) and write your habits in the “Habit” column. Start with 2 or 3.'),
             ('2', f'On a day you did a habit, click its box and pick {TICK} from the little arrow. Typing x or 1 works too.'),
             ('3', 'The box turns green. Done, % and streak update on their own. Leave a box empty on a day you missed.'),
             ('4', 'The bottom row shows how much of each day you completed. The Overview tab shows your whole year.'),
             ('5', 'Google Sheets: File → Import → Upload this file. For real tick boxes, select the grid and choose Insert → Checkbox.')]
    for i, (n, t) in enumerate(steps, start=7):
        st[f'B{i}'] = n; st[f'B{i}'].font = Font(bold=True, color=INK); st[f'B{i}'].fill = DONE; st[f'B{i}'].alignment = CENTER
        st.merge_cells(f'C{i}:D{i}'); st[f'C{i}'] = t; st[f'C{i}'].alignment = Alignment(vertical='center', wrap_text=True); st.row_dimensions[i].height = 30
    st['B13'] = 'Tips that make it stick'; st['B13'].font = Font(bold=True, size=13)
    for i, t in enumerate(['Tie each habit to something you already do: “after morning chai, read 10 pages”.',
                           'Missing one day is fine. Try never to miss two in a row.',
                           'New habits took a median of 66 days to feel automatic in a University College London study (Lally et al., 2010).'], start=14):
        st[f'C{i}'] = '• ' + t
    st['C18'] = FOOT; st['C18'].font = Font(color=GREY, italic=True)
    st['C4'].number_format = '0'
    # ---------- Overview ----------
    ov = wb.create_sheet('Overview'); ov.sheet_view.showGridLines = False
    ov['B2'] = f'=CONCATENATE("Your year: ",{YEAR})'; ov['B2'].font = Font(bold=True, size=22, color=INK)
    for c, h in zip('BCD', ('Month', 'Completion', 'Days ticked')):
        ov[f'{c}4'] = h; ov[f'{c}4'].fill = HEAD; ov[f'{c}4'].font = HEADF; ov[f'{c}4'].alignment = CENTER
    for i, name in enumerate(MONTHS, start=5):
        tab = name[:3]
        ov[f'B{i}'] = name; ov[f'C{i}'] = f"='{tab}'!$AJ$1"; ov[f'D{i}'] = f"='{tab}'!$AK$1"
        ov[f'C{i}'].number_format = '0%'
        for c in 'BCD': ov[f'{c}{i}'].border = grid; ov[f'{c}{i}'].alignment = CENTER
        ov.row_dimensions[i].height = 22
    ov.conditional_formatting.add('C5:C16', DataBarRule(start_type='num', start_value=0, end_type='num', end_value=1, color='A3C93A'))
    ov.column_dimensions['A'].width = 3; ov.column_dimensions['B'].width = 16; ov.column_dimensions['C'].width = 30; ov.column_dimensions['D'].width = 14
    ov['B18'] = FOOT; ov['B18'].font = Font(color=GREY, italic=True)
    # ---------- Month sheets ----------
    examples = ['Drink 8 glasses of water', 'Walk 8,000 steps', 'Read 10 pages', 'No sugar after 8 pm', 'Sleep by 11 pm']
    first, lastrow = 5, 16          # habit rows
    daysrow, wdrow, totrow = 4, 3, 18
    for m, name in enumerate(MONTHS, start=1):
        ws = wb.create_sheet(name[:3]); ws.sheet_view.showGridLines = False
        D = f'DATE({YEAR},{m},1)'
        ndays = f'DAY(EOMONTH({D},0))'
        ws['A1'] = f'=UPPER(TEXT({D},"mmmm yyyy"))'; ws['A1'].font = Font(bold=True, size=20, color=INK)
        ws['A2'] = f'Click a box and pick {TICK} (or type x). Empty = missed.'; ws['A2'].font = Font(italic=True, color=MUTED)
        # month score, top right
        ws['AH1'] = 'Month score'; ws['AH1'].font = Font(bold=True, color=MUTED); ws['AH1'].alignment = Alignment(horizontal='right', vertical='center')
        ws.merge_cells('AH1:AI1')
        ws['AJ1'] = f'=IF(COUNTA($A${first}:$A${lastrow})=0,"",AK1/(COUNTA($A${first}:$A${lastrow})*{ndays}))'
        ws['AJ1'].number_format = '0%'; ws['AJ1'].font = Font(bold=True, size=18, color=INK); ws['AJ1'].fill = DONE; ws['AJ1'].alignment = CENTER
        ws['AK1'] = f'=SUM(AH{first}:AH{lastrow})'; ws['AK1'].font = Font(color=MUTED); ws['AK1'].alignment = CENTER
        ws['AK2'] = 'ticks'; ws['AK2'].font = Font(color=MUTED, size=9); ws['AK2'].alignment = CENTER
        ws.row_dimensions[1].height = 34
        # header rows
        ws[f'A{daysrow}'] = 'Habit'; ws[f'A{daysrow}'].fill = HEAD; ws[f'A{daysrow}'].font = HEADF
        ws[f'A{daysrow}'].alignment = Alignment(vertical='center', indent=1)
        for d in range(1, 32):
            c = col(d + 1)
            ws[f'{c}{daysrow}'] = f'=IF({d}<={ndays},{d},"")'
            ws[f'{c}{wdrow}'] = f'=IF({c}${daysrow}="","",LEFT(TEXT(DATE({YEAR},{m},{c}${daysrow}),"ddd"),2))'
            ws[f'{c}{daysrow}'].fill = HEAD; ws[f'{c}{daysrow}'].font = HEADF; ws[f'{c}{daysrow}'].alignment = CENTER
            ws[f'{c}{wdrow}'].font = Font(size=9, color=MUTED); ws[f'{c}{wdrow}'].alignment = CENTER
            ws.column_dimensions[c].width = 4.4
        for c, label in (('AH', 'Done'), ('AI', 'Streak'), ('AJ', 'Progress')):
            ws[f'{c}{daysrow}'] = label; ws[f'{c}{daysrow}'].fill = HEAD; ws[f'{c}{daysrow}'].font = HEADF; ws[f'{c}{daysrow}'].alignment = CENTER
        ws.column_dimensions['A'].width = 30; ws.column_dimensions['AG'].width = 2
        ws.column_dimensions['AH'].width = 8; ws.column_dimensions['AI'].width = 8; ws.column_dimensions['AJ'].width = 16; ws.column_dimensions['AK'].width = 8
        ws.row_dimensions[daysrow].height = 24
        # habit rows
        for r in range(first, lastrow + 1):
            ws.row_dimensions[r].height = 24
            i = r - first
            a = ws[f'A{r}']; a.value = examples[i] if i < len(examples) else None
            a.border = grid; a.alignment = Alignment(vertical='center', indent=1)
            if i % 2: a.fill = PatternFill('solid', fgColor=ROWA)
            for d in range(1, 32):
                cell = ws[f'{col(d + 1)}{r}']; cell.border = grid; cell.alignment = CENTER; cell.font = Font(bold=True, size=13, color=INK)
            rng = f'B{r}:AF{r}'
            done = f'(LEN({rng})>0)*({rng}<>FALSE)'
            ws[f'AH{r}'] = f'=IF(A{r}="","",SUMPRODUCT({done}))'
            ws[f'AI{r}'] = ArrayFormula(f'AI{r}', f'=IF(A{r}="","",MAX(FREQUENCY(IF({done},COLUMN({rng})),IF({done}=0,COLUMN({rng})))))')
            ws[f'AJ{r}'] = f'=IF(A{r}="","",AH{r}/{ndays})'; ws[f'AJ{r}'].number_format = '0%'
            for c in ('AH', 'AI', 'AJ'):
                ws[f'{c}{r}'].alignment = CENTER; ws[f'{c}{r}'].border = grid; ws[f'{c}{r}'].font = Font(bold=True, color=INK)
        g = f'B{first}:AF{lastrow}'
        # Order matters: done (green) wins over weekend shading and days outside the month.
        ws.conditional_formatting.add(g, FormulaRule(formula=[f'AND(LEN(B{first})>0,B{first}<>FALSE)'], fill=DONE, stopIfTrue=True))
        ws.conditional_formatting.add(g, FormulaRule(formula=[f'B${daysrow}=""'], fill=PatternFill('solid', fgColor='D4D4D8'), stopIfTrue=True))
        ws.conditional_formatting.add(g, FormulaRule(formula=[f'WEEKDAY(DATE({YEAR},{m},B${daysrow}),2)>5'], fill=PatternFill('solid', fgColor=WEEKEND)))
        ws.conditional_formatting.add(f'AJ{first}:AJ{lastrow}', DataBarRule(start_type='num', start_value=0, end_type='num', end_value=1, color='A3C93A'))
        dv = DataValidation(type='list', formula1=f'"{TICK}"', allow_blank=True, showErrorMessage=False,
                            showInputMessage=True, promptTitle='Did it today?', prompt=f'Pick {TICK} from the arrow, or type x. Leave empty if missed.')
        ws.add_data_validation(dv); dv.add(g)
        # daily score row
        ws[f'A{totrow}'] = 'Day score'; ws[f'A{totrow}'].font = Font(bold=True, color=MUTED); ws[f'A{totrow}'].alignment = Alignment(vertical='center', indent=1)
        for d in range(1, 32):
            c = col(d + 1); rr = f'{c}{first}:{c}{lastrow}'
            ws[f'{c}{totrow}'] = f'=IF(OR({c}${daysrow}="",COUNTA($A${first}:$A${lastrow})=0),"",SUMPRODUCT((LEN({rr})>0)*({rr}<>FALSE)*(LEN($A${first}:$A${lastrow})>0))/COUNTA($A${first}:$A${lastrow}))'
            ws[f'{c}{totrow}'].number_format = '0%'; ws[f'{c}{totrow}'].font = Font(size=8, color=INK); ws[f'{c}{totrow}'].alignment = CENTER
        ws.conditional_formatting.add(f'B{totrow}:AF{totrow}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=1, end_color=LIME))
        ws.row_dimensions[totrow].height = 22
        ws[f'A{totrow + 2}'] = FOOT; ws[f'A{totrow + 2}'].font = Font(color=GREY, italic=True, size=9)
        ws.freeze_panes = f'B{first}'
        ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 1; ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_area = f'A1:AK{totrow}'
        ws.sheet_properties.tabColor = LIME if m % 2 else 'A3C93A'
    wb.active = 1
    from openpyxl.workbook.properties import CalcProperties
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
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
