#!/usr/bin/env python3
"""Free downloadable spreadsheets for the /*-template pages (habit, budget, EMI and credit card trackers, debt payoff plan).

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

LOAN_TYPES = ['Home loan', 'Car loan', 'Personal loan', 'Education loan', 'Two-wheeler loan', 'Gold loan', 'Consumer durable / no-cost EMI', 'Credit card EMI', 'Other']

def emi_tracker():
    """Every loan on one sheet: EMI, EMIs paid, outstanding today, interest paid, last EMI date, and a debt-free month.
    A Schedule sheet shows month-by-month interest and principal for one loan, with a column for prepayments."""
    wb = Workbook()
    ws = wb.active; ws.title = 'Loans'
    MONEY = '₹#,##,##0'
    ws['A1'] = 'EMI tracker: all your loans'; ws['A1'].font = Font(bold=True, size=18)
    ws['A2'] = 'Fill the lime columns for each loan (the 3 rows below are examples; overwrite them). Everything else works itself out as of today.'
    ws['A2'].font = Font(color=GREY, italic=True)
    # summary block
    labels = [('A4', 'Take-home salary (monthly)'), ('A5', 'Total monthly EMIs (loans not yet closed)'), ('A6', 'EMIs as % of salary'),
              ('A7', 'Total outstanding today'), ('A8', 'Interest still to pay'), ('A9', 'Debt-free after (last EMI)')]
    for ref, t in labels: ws[ref] = t; ws[ref].font = B
    H0, H1 = 12, 41   # loan rows 12..41 (30 loans)
    rng = lambda c: f'{c}{H0}:{c}{H1}'
    ws['C4'] = 150000; ws['C4'].fill = DONE
    ws['C5'] = f'=SUMIFS({rng("H")},{rng("M")},">0")'
    ws['C6'] = '=IF(C4>0,C5/C4,"")'; ws['C6'].number_format = '0%'
    ws['C7'] = f'=SUM({rng("J")})'
    ws['C8'] = f'=SUM({rng("N")})'
    ws['C9'] = f'=IF(COUNT({rng("L")})=0,"",MAX({rng("L")}))'; ws['C9'].number_format = 'mmm yyyy'
    for r in (4, 5, 7, 8): ws[f'C{r}'].number_format = MONEY
    for r in range(4, 10):
        for c in 'ABC': ws[f'{c}{r}'].border = BOX
    ws['E5'] = 'Lenders look at your EMIs as a share of income (FOIR) before a new loan. Lower is safer.'
    ws['E5'].font = Font(color=GREY, italic=True)
    heads = [('A', 'Loan', 22), ('B', 'Lender', 16), ('C', 'Type', 20), ('D', 'Loan amount', 13), ('E', 'Rate % (yearly)', 10),
             ('F', 'Tenure (months)', 10), ('G', 'First EMI date', 13), ('H', 'EMI', 11), ('I', 'EMIs paid', 9),
             ('J', 'Outstanding today', 14), ('K', 'Interest paid so far', 14), ('L', 'Last EMI', 11), ('M', 'EMIs left', 9), ('N', 'Interest still to pay', 14)]
    hr = H0 - 1
    for c, h, w in heads:
        ws[f'{c}{hr}'] = h; ws[f'{c}{hr}'].fill = HEAD; ws[f'{c}{hr}'].font = HEADF
        ws[f'{c}{hr}'].alignment = Alignment(wrap_text=True, vertical='center'); ws.column_dimensions[c].width = w
    ws.row_dimensions[hr].height = 32
    for r in range(H0, H1 + 1):
        ws[f'H{r}'] = f'=IF(OR(D{r}="",F{r}=""),"",ROUND(PMT(N(E{r})/1200,F{r},-D{r}),0))'
        ws[f'I{r}'] = (f'=IF(OR(G{r}="",F{r}=""),"",MIN(F{r},MAX(0,(YEAR(TODAY())-YEAR(G{r}))*12+MONTH(TODAY())-MONTH(G{r})'
                       f'+IF(DAY(TODAY())>=DAY(G{r}),1,0))))')
        ws[f'J{r}'] = f'=IF(I{r}="","",IF(I{r}>=F{r},0,ROUND(PV(N(E{r})/1200,F{r}-I{r},-PMT(N(E{r})/1200,F{r},-D{r})),0)))'
        ws[f'K{r}'] = f'=IF(J{r}="","",MAX(0,H{r}*I{r}-(D{r}-J{r})))'
        ws[f'L{r}'] = f'=IF(OR(G{r}="",F{r}=""),"",EDATE(G{r},F{r}-1))'
        ws[f'M{r}'] = f'=IF(I{r}="","",F{r}-I{r})'
        ws[f'N{r}'] = f'=IF(M{r}="","",MAX(0,H{r}*M{r}-J{r}))'
        for c in 'ABCDEFG': ws[f'{c}{r}'].fill = DONE if r < H0 + 3 else PatternFill('solid', fgColor='F7FBDF')
        for c in 'DHJKN': ws[f'{c}{r}'].number_format = MONEY
        ws[f'G{r}'].number_format = 'dd mmm yyyy'; ws[f'L{r}'].number_format = 'mmm yyyy'
        for c in 'ABCDEFGHIJKLMN': ws[f'{c}{r}'].border = BOX
    sample = [('Home loan', 'Example Bank', 'Home loan', 4000000, 8.5, 240, (2024, 5, 5)),
              ('Car loan', 'Example Bank', 'Car loan', 600000, 9.5, 60, (2025, 1, 10)),
              ('Phone on no-cost EMI', 'Card EMI', 'Consumer durable / no-cost EMI', 60000, 0, 6, (2026, 9, 15))]
    import datetime
    for i, (a, b, c, d, e, f, g) in enumerate(sample):
        r = H0 + i
        ws[f'A{r}'], ws[f'B{r}'], ws[f'C{r}'], ws[f'D{r}'], ws[f'E{r}'], ws[f'F{r}'] = a, b, c, d, e, f
        ws[f'G{r}'] = datetime.date(*g)
    lists = wb.create_sheet('Lists'); lists.sheet_state = 'hidden'
    for i, t in enumerate(LOAN_TYPES, start=1): lists[f'A{i}'] = t
    dv = DataValidation(type='list', formula1=f'=Lists!$A$1:$A${len(LOAN_TYPES)}', allow_blank=True); ws.add_data_validation(dv); dv.add(rng('C'))
    ws.conditional_formatting.add(rng('M'), CellIsRule(operator='equal', formula=['0'], font=Font(color=GREY)))
    ws.conditional_formatting.add('C6', CellIsRule(operator='greaterThan', formula=['0.5'], font=Font(color='DC2626', bold=True)))
    ws[f'A{H1 + 2}'] = ('EMI uses the standard reducing-balance formula. Your bank\'s figure can differ by a few rupees (rounding, '
                        'broken-period interest) or more if a floating rate changed. If so, type the bank\'s numbers into a new row as a fresh loan from today.')
    ws[f'A{H1 + 2}'].font = Font(color=GREY, italic=True)
    ws[f'A{H1 + 3}'] = FOOT; ws[f'A{H1 + 3}'].font = Font(color=GREY, italic=True)
    ws.freeze_panes = f'B{H0}'; ws.sheet_view.showGridLines = False
    # schedule for one loan, with prepayments
    sc = wb.create_sheet('Schedule')
    sc['A1'] = 'Repayment schedule for one loan'; sc['A1'].font = Font(bold=True, size=18)
    sc['A3'] = 'Pick a loan'; sc['A3'].font = B; sc['C3'] = 'Home loan'; sc['C3'].fill = DONE
    dv2 = DataValidation(type='list', formula1=f'=Loans!$A${H0}:$A${H1}', allow_blank=False); sc.add_data_validation(dv2); dv2.add('C3')
    row = f'MATCH($C$3,Loans!$A${H0}:$A${H1},0)'
    pick = lambda c: f'INDEX(Loans!${c}${H0}:${c}${H1},{row})'
    info = [('A4', 'Loan amount', 'C4', f'=IFERROR({pick("D")},0)', MONEY), ('A5', 'Rate % (yearly)', 'C5', f'=IFERROR(N({pick("E")}),0)', '0.00'),
            ('A6', 'EMI', 'C6', f'=IFERROR({pick("H")},0)', MONEY), ('A7', 'First EMI date', 'C7', f'=IFERROR({pick("G")},"")', 'dd mmm yyyy'),
            ('A8', 'Total interest', 'C8', '=SUM(E13:E372)', MONEY), ('A9', 'EMIs needed', 'C9', '=COUNTIF(D13:D372,">0")', '0'),
            ('A10', 'Loan closes', 'C10', '=IF(C9=0,"",EDATE(C7,C9-1))', 'mmm yyyy')]
    for a, t, c, f, fmt in info:
        sc[a] = t; sc[c] = f; sc[c].number_format = fmt
        for x in (a, c): sc[x].border = BOX
    sc['E4'] = 'Type any extra payment (prepayment) in the lime column for that month. The EMI stays the same, so the loan closes earlier; see "EMIs needed" and "Total interest" change.'
    sc['E4'].font = Font(color=GREY, italic=True)
    for c, h, w in zip('ABCDEFGH', ('No.', 'Month', 'Opening balance', 'EMI paid', 'Interest', 'Principal', 'Extra payment', 'Closing balance'), (6, 12, 16, 12, 12, 12, 14, 16)):
        sc[f'{c}12'] = h; sc[f'{c}12'].fill = HEAD; sc[f'{c}12'].font = HEADF; sc.column_dimensions[c].width = w
    for r in range(13, 373):
        n = r - 12
        prev = '$C$4' if r == 13 else f'H{r - 1}'
        sc[f'A{r}'] = n
        sc[f'B{r}'] = f'=IF(OR($C$7="",C{r}<=0),"",EDATE($C$7,{n - 1}))'
        sc[f'C{r}'] = f'=IF({prev}="",0,N({prev}))' if r > 13 else '=$C$4'
        sc[f'E{r}'] = f'=IF(C{r}<=0,0,ROUND(C{r}*$C$5/1200,0))'
        sc[f'D{r}'] = f'=IF(C{r}<=0,0,MIN($C$6,C{r}+E{r}))'
        sc[f'F{r}'] = f'=D{r}-E{r}'
        sc[f'G{r}'].fill = DONE
        sc[f'H{r}'] = f'=IF(C{r}<=0,0,MAX(0,C{r}-F{r}-MIN(N(G{r}),C{r}-F{r})))'
        for c in 'CDEFGH': sc[f'{c}{r}'].number_format = MONEY
        sc[f'B{r}'].number_format = 'mmm yyyy'
    sc.conditional_formatting.add('A13:H372', FormulaRule(formula=['$C13<=0'], font=Font(color='D4D4D8')))
    sc.freeze_panes = 'A13'; sc.sheet_view.showGridLines = False
    from openpyxl.workbook.properties import CalcProperties
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    return wb

def stmt_on_or_after(d, S):
    """Excel formula: the first statement date on or after date d, for a card whose statement day is S (29-31 clamp to month end)."""
    a = f'EOMONTH({d},-1)+MIN({S},DAY(EOMONTH({d},0)))'
    return f'IF({d}<={a},{a},EOMONTH({d},0)+MIN({S},DAY(EOMONTH({d},1))))'

def due_after(s, D):
    """Excel formula: the first date after statement s that falls on due day D."""
    a = f'EOMONTH({s},-1)+MIN({D},DAY(EOMONTH({s},0)))'
    return f'IF({a}>{s},{a},EOMONTH({s},0)+MIN({D},DAY(EOMONTH({s},1))))'

def credit_card_tracker():
    """Every credit card on one sheet: last bill and its due date, what's on the next bill so far, days of interest-free
    credit if you buy today, limit used. A Spends sheet puts each purchase on the right statement, like the bank does."""
    import datetime
    from openpyxl.workbook.properties import CalcProperties
    wb = Workbook()
    ws = wb.active; ws.title = 'Cards'
    MONEY = '₹#,##,##0'; DATE = 'dd mmm yyyy'
    C0, C1 = 12, 21            # card rows (10 cards)
    S0, S1 = 5, 504            # spend rows (500 spends)
    rng = lambda c: f'${c}${C0}:${c}${C1}'
    ws['A1'] = 'Credit card tracker: every card, every bill'; ws['A1'].font = Font(bold=True, size=18)
    ws['A2'] = ('Fill the lime columns for each card (the 3 rows below are examples; overwrite them), then log purchases on the Spends tab. '
                'Dates work themselves out as of today. No card numbers needed.')
    ws['A2'].font = Font(color=GREY, italic=True)
    summary = [('A4', 'Total credit limit', 'C4', f'=SUM({rng("C")})', MONEY),
               ('A5', 'Limit used (unpaid bills + new spends)', 'C5', f'=SUM({rng("P")})', MONEY),
               ('A6', 'Overall utilisation', 'C6', '=IF(C4>0,C5/C4,"")', '0%'),
               ('A7', 'Next payment due', 'C7', f'=IF(COUNT({rng("L")})=0,"",MIN({rng("L")}))', DATE),
               ('A8', 'Card with the most interest-free days today', 'C8', f'=IF(COUNT({rng("N")})=0,"",INDEX({rng("A")},MATCH(MAX({rng("N")}),{rng("N")},0)))', '@'),
               ('A9', 'Warn me when utilisation is above', 'C9', 0.3, '0%')]
    for a, t, c, f, fmt in summary:
        ws[a] = t; ws[a].font = B; ws[c] = f; ws[c].number_format = fmt
        for x in ('A', 'B', 'C'): ws[f'{x}{a[1:]}'].border = BOX
    ws['C9'].fill = DONE
    ws['D7'] = f'=IF(C7="","",INDEX({rng("A")},MATCH(C7,{rng("L")},0)))'
    ws['E7'] = '=IF(C7="","",C7-TODAY()&" days left")'
    ws['D8'] = f'=IF(C8="","",MAX({rng("N")})&" days to pay if you buy today")'
    for r in (7, 8): ws[f'E{r}'].font = Font(color=GREY, italic=True); ws[f'D{r}'].font = Font(color=GREY, italic=True)
    heads = [('A', 'Card', 18), ('B', 'Bank', 14), ('C', 'Credit limit', 12), ('D', 'Statement day (1-31)', 10), ('E', 'Due day (1-31)', 9),
             ('F', 'Last bill paid?', 9), ('G', 'Last statement', 12), ('H', 'Last bill (from your spends)', 13), ('I', 'Last bill due', 12),
             ('J', 'Next statement', 12), ('K', 'On next bill so far', 13), ('L', 'Next payment due', 12), ('M', 'Days left to pay', 9),
             ('N', 'Interest-free days if you buy today', 12), ('O', 'Best day to buy next', 12), ('P', 'Limit used', 12), ('Q', 'Utilisation', 10)]
    hr = C0 - 1
    for c, h, w in heads:
        ws[f'{c}{hr}'] = h; ws[f'{c}{hr}'].fill = HEAD; ws[f'{c}{hr}'].font = HEADF
        ws[f'{c}{hr}'].alignment = Alignment(wrap_text=True, vertical='center'); ws.column_dimensions[c].width = w
    ws.row_dimensions[hr].height = 46
    SP = lambda c: f'Spends!${c}${S0}:${c}${S1}'
    for r in range(C0, C1 + 1):
        ok = f'OR(A{r}="",D{r}="",E{r}="")'
        ws[f'J{r}'] = f'=IF({ok},"",{stmt_on_or_after("TODAY()", f"D{r}")})'
        ws[f'G{r}'] = f'=IF(J{r}="","",EOMONTH(J{r},-2)+MIN(D{r},DAY(EOMONTH(J{r},-1))))'
        ws[f'I{r}'] = f'=IF(G{r}="","",{due_after(f"G{r}", f"E{r}")})'
        ws[f'H{r}'] = f'=IF(G{r}="","",SUMIFS({SP("C")},{SP("B")},A{r},{SP("E")},G{r}))'
        ws[f'K{r}'] = f'=IF(J{r}="","",SUMIFS({SP("C")},{SP("B")},A{r},{SP("E")},J{r}))'
        ws[f'L{r}'] = f'=IF(J{r}="","",IF(AND(F{r}<>"Yes",H{r}>0),I{r},{due_after(f"J{r}", f"E{r}")}))'
        ws[f'M{r}'] = f'=IF(L{r}="","",L{r}-TODAY())'
        ws[f'N{r}'] = f'=IF(J{r}="","",{due_after(f"J{r}", f"E{r}")}-TODAY())'
        ws[f'O{r}'] = f'=IF(J{r}="","",IF(TODAY()=G{r}+1,TODAY(),J{r}+1))'
        ws[f'P{r}'] = f'=IF(J{r}="","",K{r}+IF(F{r}="Yes",0,H{r}))'
        ws[f'Q{r}'] = f'=IF(OR(P{r}="",N(C{r})=0),"",P{r}/C{r})'
        for c in 'ABCDEF': ws[f'{c}{r}'].fill = DONE if r < C0 + 3 else PatternFill('solid', fgColor='F7FBDF')
        for c in 'CHKP': ws[f'{c}{r}'].number_format = MONEY
        for c in 'GIJLO': ws[f'{c}{r}'].number_format = DATE
        ws[f'Q{r}'].number_format = '0%'
        for c in 'ABCDEFGHIJKLMNOPQ': ws[f'{c}{r}'].border = BOX
    cards = [('HDFC card', 'HDFC Bank', 200000, 4, 24, 'Yes'), ('SBI card', 'SBI Card', 150000, 15, 5, 'No'), ('Axis card', 'Axis Bank', 100000, 22, 11, 'Yes')]
    for i, row in enumerate(cards):
        for c, v in zip('ABCDEF', row): ws[f'{c}{C0 + i}'] = v
    lists = wb.create_sheet('Lists'); lists.sheet_state = 'hidden'
    lists['A1'], lists['A2'] = 'Yes', 'No'
    dv = DataValidation(type='list', formula1='=Lists!$A$1:$A$2', allow_blank=True); ws.add_data_validation(dv); dv.add(f'F{C0}:F{C1}')
    dvd = DataValidation(type='whole', operator='between', formula1='1', formula2='31', allow_blank=True,
                         error='Type a day of the month, 1 to 31.', showErrorMessage=True)
    ws.add_data_validation(dvd); dvd.add(f'D{C0}:E{C1}')
    ws.conditional_formatting.add(f'Q{C0}:Q{C1}', FormulaRule(formula=[f'AND(ISNUMBER(Q{C0}),Q{C0}>$C$9)'], font=Font(color='DC2626', bold=True)))
    ws.conditional_formatting.add('C6', FormulaRule(formula=['AND(ISNUMBER(C6),C6>$C$9)'], font=Font(color='DC2626', bold=True)))
    ws.conditional_formatting.add(f'L{C0}:M{C1}', FormulaRule(formula=[f'AND(ISNUMBER($M{C0}),$M{C0}<=3)'], font=Font(color='DC2626', bold=True)))
    notes = ['How the dates work: a purchase made on or before the statement day goes on that statement; anything after rolls to the next one. '
             'The bill is due on the next due day after the statement.',
             'Statement day 29, 30 or 31 counts as the last day of shorter months. Banks post some spends a day or two late, so a purchase on the statement day itself can land on either bill.',
             '"Last bill paid?": set it to Yes once you pay the full bill, and back to No when the next statement arrives. An unpaid bill stays as "Next payment due" (in red once it is 3 days away or late). Your bank statement is the final word on what you owe.',
             FOOT]
    for i, t in enumerate(notes):
        ws[f'A{C1 + 2 + i}'] = t; ws[f'A{C1 + 2 + i}'].font = Font(color=GREY, italic=True)
    ws.freeze_panes = f'B{C0}'; ws.sheet_view.showGridLines = False
    # spends
    sp = wb.create_sheet('Spends')
    sp['A1'] = 'Card spends'; sp['A1'].font = Font(bold=True, size=18)
    sp['A2'] = 'One row per purchase. Pick the card from the list; the sheet puts it on the right statement and shows when it is due.'
    sp['A2'].font = Font(color=GREY, italic=True)
    for c, h, w in zip('ABCDEFG', ('Date', 'Card', 'Amount', 'What for', 'Lands on statement', 'Pay by', 'Which bill'), (13, 18, 12, 26, 14, 13, 18)):
        sp[f'{c}4'] = h; sp[f'{c}4'].fill = HEAD; sp[f'{c}4'].font = HEADF; sp.column_dimensions[c].width = w
    look = lambda c, r: f'INDEX(Cards!{rng(c)},MATCH(B{r},Cards!{rng("A")},0))'
    for r in range(S0, S1 + 1):
        sp[f'E{r}'] = f'=IF(OR(A{r}="",B{r}=""),"",IFERROR({stmt_on_or_after(f"A{r}", look("D", r))},""))'
        sp[f'F{r}'] = f'=IF(E{r}="","",{due_after(f"E{r}", look("E", r))})'
        sp[f'G{r}'] = f'=IF(E{r}="","",IF(E{r}>=TODAY(),"Next bill (not billed yet)",IF(F{r}>=TODAY(),"Current bill","Older bill")))'
        for c in 'ABCD': sp[f'{c}{r}'].fill = DONE if r < S0 + 9 else PatternFill('solid', fgColor='F7FBDF')
        sp[f'A{r}'].number_format = DATE; sp[f'E{r}'].number_format = DATE; sp[f'F{r}'].number_format = DATE
        sp[f'C{r}'].number_format = MONEY
        for c in 'ABCDEFG': sp[f'{c}{r}'].border = BOX
    spends = [((2026, 11, 2), 'HDFC card', 4200, 'Groceries'), ((2026, 11, 6), 'HDFC card', 18999, 'Phone (bought just after statement)'),
              ((2026, 10, 18), 'SBI card', 2450, 'Swiggy and Zomato'), ((2026, 11, 9), 'SBI card', 6300, 'Flight tickets'),
              ((2026, 11, 16), 'SBI card', 1200, 'Fuel'), ((2026, 10, 20), 'Axis card', 2100, 'Train tickets'), ((2026, 10, 25), 'Axis card', 3500, 'Electricity bill'),
              ((2026, 11, 12), 'Axis card', 899, 'OTT subscription'), ((2026, 11, 14), 'Axis card', 5400, 'Shopping')]
    for i, (d, c, a, w) in enumerate(spends):
        r = S0 + i; sp[f'A{r}'] = datetime.date(*d); sp[f'B{r}'], sp[f'C{r}'], sp[f'D{r}'] = c, a, w
    dv2 = DataValidation(type='list', formula1=f'=Cards!$A${C0}:$A${C1}', allow_blank=True); sp.add_data_validation(dv2); dv2.add(f'B{S0}:B{S1}')
    sp.conditional_formatting.add(f'G{S0}:G{S1}', FormulaRule(formula=[f'G{S0}="Current bill"'], font=Font(bold=True, color='DC2626')))
    sp.conditional_formatting.add(f'A{S0}:G{S1}', FormulaRule(formula=[f'$G{S0}="Older bill"'], font=Font(color=GREY)))
    sp.freeze_panes = f'A{S0}'; sp.sheet_view.showGridLines = False
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    return wb

DEBT_TYPES = ['Credit card', 'Personal loan', 'Car loan', 'Two-wheeler loan', 'Home loan', 'Education loan', 'Gold loan',
              'Consumer durable / no-cost EMI', 'Pay later / BNPL', 'Loan from family or friends', 'Other']

def debt_payoff():
    """Debt snowball and avalanche in one file. You list your debts and what you can pay towards them each month; three
    plan sheets simulate it month by month (avalanche, snowball, and minimums only), and the Debts sheet compares them.
    Each month: interest is added, every debt gets its minimum, and the rest goes to the first debt in the plan's order.
    A cleared debt's minimum rolls on to the next one."""
    from openpyxl.workbook.properties import CalcProperties
    wb = Workbook()
    ws = wb.active; ws.title = 'Debts'
    MONEY = '₹#,##,##0'; MDATE = 'mmm yyyy'
    R0, R1 = 13, 22            # debt rows (10 debts)
    N = R1 - R0 + 1
    M0, M1 = 13, 372           # plan rows (360 months)
    rng = lambda c: f'${c}${R0}:${c}${R1}'
    ws['A1'] = 'Debt payoff plan: snowball vs avalanche'; ws['A1'].font = Font(bold=True, size=18)
    ws['A2'] = ('Fill the lime cells: what you can pay towards debts each month, then each debt below (the 3 rows are examples; overwrite them). '
                'The sheet compares both methods and shows the month each debt is cleared.')
    ws['A2'].font = Font(color=GREY, italic=True)
    inputs = [('A4', 'Total you can pay towards debts each month', 'C4', 20000, MONEY),
              ('A5', 'Minimums and EMIs add up to', 'C5', f'=SUMPRODUCT({rng("O")},{rng("E")})', MONEY),
              ('A6', 'Extra each month (goes to one debt at a time)', 'C6', '=C4-C5', MONEY),
              ('A7', 'First payment month', 'C7', '=EOMONTH(TODAY(),0)+1', MDATE),
              ('A8', 'Total you owe today', 'C8', f'=SUMPRODUCT({rng("O")},{rng("C")})', MONEY),
              ('A9', 'Interest added this month (at today\'s balances)', 'C9', f'=SUM({rng("F")})', MONEY)]
    for a, t, c, f, fmt in inputs:
        ws[a] = t; ws[a].font = B; ws[c] = f; ws[c].number_format = fmt
        for x in 'ABC': ws[f'{x}{a[1:]}'].border = BOX
    ws['C4'].fill = DONE; ws['C7'].fill = DONE
    ws['D6'] = '=IF(C6<0,"Less than your minimums: the plans pay the minimums anyway, so find "&TEXT(-C6,"#,##0")&" more or talk to your lender","")'
    ws['D6'].font = Font(color='DC2626', bold=True)
    ws['D7'] = '← works itself out (next month); type a date to change it'; ws['D7'].font = Font(color=GREY, italic=True)
    # comparison table
    ws['F3'] = 'Plan'; ws['G3'] = 'Debt-free in (months)'; ws['H3'] = 'Debt-free month'; ws['I3'] = 'Total interest'; ws['J3'] = 'Saves vs minimums only'
    for c in 'FGHIJ':
        ws[f'{c}3'].fill = HEAD; ws[f'{c}3'].font = HEADF; ws[f'{c}3'].alignment = Alignment(wrap_text=True, vertical='center')
    ws.row_dimensions[3].height = 30
    plans = [('Avalanche', 'Avalanche (highest rate first)'), ('Snowball', 'Snowball (smallest balance first)'), ('Minimums', 'Minimums only')]
    for i, (sh, label) in enumerate(plans):
        r = 4 + i
        ws[f'F{r}'] = label; ws[f'F{r}'].font = B
        ws[f'G{r}'] = f"=IF({sh}!$C$6,\"over 30 years\",{sh}!$C$4)"
        ws[f'H{r}'] = f"=IF(OR({sh}!$C$6,{sh}!$C$4=0),\"\",EDATE($C$7,{sh}!$C$4-1))"; ws[f'H{r}'].number_format = MDATE
        ws[f'I{r}'] = f"=IF({sh}!$C$6,\"\",{sh}!$C$5)"; ws[f'I{r}'].number_format = MONEY
        ws[f'J{r}'] = f'=IF(OR(I{r}="",$I$6=""),"",$I$6-I{r})'; ws[f'J{r}'].number_format = MONEY
        for c in 'FGHIJ': ws[f'{c}{r}'].border = BOX
    ws['J6'] = '—'
    ws['F8'] = '=IF(OR(I4="",I5=""),"",IF(ROUND(I5,0)-ROUND(I4,0)>=1,"Avalanche saves "&TEXT(ROUND(I5,0)-ROUND(I4,0),"#,##0")&" in interest over snowball.","Both methods cost the same here: pick the one you will stick with."))'
    ws['F8'].font = Font(bold=True)
    ws['F9'] = '="Minimums only means paying today\'s minimums total ("&TEXT($C$5,"#,##0")&" a month) with nothing extra."'
    ws['F9'].font = Font(color=GREY, italic=True)
    heads = [('A', 'Debt', 22), ('B', 'Type', 20), ('C', 'Balance today', 13), ('D', 'Rate % (yearly)', 10), ('E', 'Minimum or EMI a month', 12),
             ('F', 'Interest this month', 12), ('G', 'Order (avalanche)', 10), ('H', 'Cleared (avalanche)', 12), ('I', 'Order (snowball)', 10), ('J', 'Cleared (snowball)', 12),
             ('K', 'Cleared (minimums only)', 12)]
    hr = R0 - 1
    for c, h, w in heads:
        ws[f'{c}{hr}'] = h; ws[f'{c}{hr}'].fill = HEAD; ws[f'{c}{hr}'].font = HEADF
        ws[f'{c}{hr}'].alignment = Alignment(wrap_text=True, vertical='center'); ws.column_dimensions[c].width = w
    ws.row_dimensions[hr].height = 46
    for c in 'LMN': ws.column_dimensions[c].hidden = True
    ws.column_dimensions['O'].hidden = True
    def cleared(sh, rank_col, r):
        return (f'=IF({rank_col}{r}="","",IF(INDEX({sh}!$C$11:$AF$11,1,({rank_col}{r}-1)*3+1)=0,"",'
                f'IF(INDEX({sh}!$C$11:$AF$11,1,({rank_col}{r}-1)*3+1)>={M1 - M0 + 1},"over 30 years",EDATE($C$7,INDEX({sh}!$C$11:$AF$11,1,({rank_col}{r}-1)*3+1)-1))))')
    for r in range(R0, R1 + 1):
        ws[f'O{r}'] = f'=IF(AND(A{r}<>"",ISNUMBER(C{r}),N(C{r})>0,ISNUMBER(D{r})),1,0)'   # counts as a debt
        ws[f'N{r}'] = r                                                                   # tie-break
        ws[f'F{r}'] = f'=IF(O{r}=1,ROUND(C{r}*D{r}/1200,0),"")'
        ws[f'G{r}'] = (f'=IF(O{r}=1,1+COUNTIFS({rng("O")},1,{rng("D")},">"&D{r})+COUNTIFS({rng("O")},1,{rng("D")},D{r},{rng("C")},"<"&C{r})'
                       f'+COUNTIFS({rng("O")},1,{rng("D")},D{r},{rng("C")},C{r},{rng("N")},"<"&N{r}),"")')
        ws[f'I{r}'] = (f'=IF(O{r}=1,1+COUNTIFS({rng("O")},1,{rng("C")},"<"&C{r})+COUNTIFS({rng("O")},1,{rng("C")},C{r},{rng("D")},">"&D{r})'
                       f'+COUNTIFS({rng("O")},1,{rng("C")},C{r},{rng("D")},D{r},{rng("N")},"<"&N{r}),"")')
        ws[f'H{r}'] = cleared('Avalanche', 'G', r); ws[f'J{r}'] = cleared('Snowball', 'I', r); ws[f'K{r}'] = cleared('Minimums', 'G', r)
        for c in 'ABCDE': ws[f'{c}{r}'].fill = DONE if r < R0 + 3 else PatternFill('solid', fgColor='F7FBDF')
        for c in 'CEF': ws[f'{c}{r}'].number_format = MONEY
        for c in 'HJK': ws[f'{c}{r}'].number_format = MDATE
        for c in 'ABCDEFGHIJK': ws[f'{c}{r}'].border = BOX
    sample = [('Credit card', 'Credit card', 60000, 42, 3000), ('Personal loan', 'Personal loan', 150000, 14, 5000), ('Phone EMI', 'Consumer durable / no-cost EMI', 20000, 16, 2000)]
    for i, row in enumerate(sample):
        for c, v in zip('ABCDE', row): ws[f'{c}{R0 + i}'] = v
    lists = wb.create_sheet('Lists'); lists.sheet_state = 'hidden'
    for i, t in enumerate(DEBT_TYPES, start=1): lists[f'A{i}'] = t
    dv = DataValidation(type='list', formula1=f'=Lists!$A$1:$A${len(DEBT_TYPES)}', allow_blank=True); ws.add_data_validation(dv); dv.add(f'B{R0}:B{R1}')
    ws.conditional_formatting.add('C6', CellIsRule(operator='lessThan', formula=['0'], font=Font(color='DC2626', bold=True)))
    notes = ['How it works: each month interest is added to every debt, every debt gets its minimum or EMI, and the extra goes to the first debt in the order. '
             'When a debt is cleared, its minimum moves to the next one, so the amount you pay each month stays the same.',
             'Avalanche orders debts by rate (highest first). Snowball orders them by balance (smallest first). Change a rate or balance and the order updates.',
             'Interest is worked out monthly at the yearly rate ÷ 12. Card issuers charge daily interest, add 18% GST on it, and the minimum due shrinks as the balance falls, '
             'so treat card figures as estimates. Your lender\'s statement is the final word.',
             'For a loan, the minimum is its EMI and the balance is the outstanding principal from your loan statement. Check prepayment charges before paying a fixed-rate loan early.',
             FOOT]
    for i, t in enumerate(notes):
        ws[f'A{R1 + 2 + i}'] = t; ws[f'A{R1 + 2 + i}'].font = Font(color=GREY, italic=True)
    ws.freeze_panes = f'B{R0}'; ws.sheet_view.showGridLines = False
    # plan sheets
    ranks = {'Avalanche': 'G', 'Snowball': 'I', 'Minimums': 'G'}
    titles = {'Avalanche': 'Avalanche plan: highest interest rate first', 'Snowball': 'Snowball plan: smallest balance first',
              'Minimums': 'Minimums only: today\'s minimums total, nothing extra'}
    for sh, rk in ranks.items():
        p = wb.create_sheet(sh)
        p['A1'] = titles[sh]; p['A1'].font = Font(bold=True, size=16)
        p['A2'] = 'Works itself out from the Debts tab. Nothing to type here.'; p['A2'].font = Font(color=GREY, italic=True)
        p['A3'] = 'Paying each month'; p['C3'] = '=MAX(Debts!$C$4,Debts!$C$5)' if sh != 'Minimums' else '=Debts!$C$5'
        p['A4'] = 'Debt-free in (months)'; p['C4'] = f'=COUNTIF(AH{M0}:AH{M1},">0")'
        p['A5'] = 'Total interest'; p['C5'] = f'=SUM(AI{M0}:AI{M1})-Debts!$C$8'
        p['A6'] = 'Not cleared in 30 years?'; p['C6'] = f'=AH{M1}-AI{M1}>0.5'
        for r in (3, 5): p[f'C{r}'].number_format = MONEY
        for r in range(3, 7):
            p[f'A{r}'].font = B
            for c in 'ABC': p[f'{c}{r}'].border = BOX
        p['A13'].value = None
        p['A12'] = 'No.'; p['B12'] = 'Month'
        p.column_dimensions['A'].width = 6; p.column_dimensions['B'].width = 10
        pool = 'AG'
        mins = []
        for k in range(1, N + 1):
            o, y, x = col(3 + (k - 1) * 3), col(4 + (k - 1) * 3), col(5 + (k - 1) * 3)
            match = f'MATCH({k},Debts!{rng(rk)},0)'
            p[f'{o}11'] = f'=IF({o}$7="",0,COUNTIF({o}{M0}:{o}{M1},">0"))'
            p[f'{y}11'] = f'=IF({o}11=0,"",IF({o}11>={M1 - M0 + 1},"not in 30 yrs","cleared in month "&{o}11))'
            p[f'{o}7'] = f'=IFERROR(INDEX(Debts!{rng("A")},{match}),"")'
            p[f'{o}8'] = f'=IFERROR(INDEX(Debts!{rng("D")},{match}),0)'
            p[f'{o}9'] = f'=IFERROR(N(INDEX(Debts!{rng("E")},{match})),0)'
            p[f'{o}10'] = f'=IFERROR(INDEX(Debts!{rng("C")},{match}),0)'
            for rr, lab in ((8, 'rate %'), (9, 'minimum'), (10, 'balance today')): p[f'{y}{rr}'] = lab; p[f'{y}{rr}'].font = Font(color=GREY, italic=True)
            p[f'{o}7'].font = B; p[f'{o}10'].number_format = MONEY; p[f'{o}9'].number_format = MONEY
            for c, h in ((o, 'Owed'), (y, 'Paid'), (x, 'Extra left')):
                p[f'{c}12'] = h; p.column_dimensions[c].width = 11
            p[f'{x}12'].font = Font(color=GREY); p.column_dimensions[x].width = 9
            for c in (o, y): p[f'{c}12'].fill = HEAD; p[f'{c}12'].font = HEADF
            prev_x = pool if k == 1 else col(5 + (k - 2) * 3)
            for r in range(M0, M1 + 1):
                if r == M0: p[f'{o}{r}'] = f'=IF({o}$7="",0,ROUND({o}$10*(1+{o}$8/1200),2))'
                else: p[f'{o}{r}'] = f'=ROUND(({o}{r - 1}-{y}{r - 1})*(1+{o}$8/1200),2)'
                p[f'{y}{r}'] = f'=MIN({o}{r},MIN({o}$9,{o}{r})+{prev_x}{r})'
                p[f'{x}{r}'] = f'={prev_x}{r}-({y}{r}-MIN({o}$9,{o}{r}))'
                for c in (o, y): p[f'{c}{r}'].number_format = MONEY
                p[f'{x}{r}'].number_format = MONEY; p[f'{x}{r}'].font = Font(color=GREY)
            mins.append(f'MIN({o}$9,{o}{{r}})')
        p[f'{pool}12'] = 'Extra to share'; p['AH12'] = 'Total owed'; p['AI12'] = 'Total paid'
        for c in (pool, 'AH', 'AI'): p[f'{c}12'].fill = HEAD; p[f'{c}12'].font = HEADF; p.column_dimensions[c].width = 12
        owed_cols = [col(3 + (k - 1) * 3) for k in range(1, N + 1)]; paid_cols = [col(4 + (k - 1) * 3) for k in range(1, N + 1)]
        for r in range(M0, M1 + 1):
            p[f'A{r}'] = r - M0 + 1
            p[f'B{r}'] = f'=EDATE(Debts!$C$7,{r - M0})'; p[f'B{r}'].number_format = MDATE
            p[f'{pool}{r}'] = f'=MAX(0,$C$3-(' + '+'.join(m.format(r=r) for m in mins) + '))'
            p[f'AH{r}'] = '=' + '+'.join(f'{c}{r}' for c in owed_cols)
            p[f'AI{r}'] = '=' + '+'.join(f'{c}{r}' for c in paid_cols)
            for c in (pool, 'AH', 'AI'): p[f'{c}{r}'].number_format = MONEY
        p.conditional_formatting.add(f'A{M0}:AI{M1}', FormulaRule(formula=[f'$AH{M0}<=0'], font=Font(color='D4D4D8')))
        p.freeze_panes = f'C{M0}'; p.sheet_view.showGridLines = False
    wb.calculation = CalcProperties(fullCalcOnLoad=True)
    return wb

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    import sys
    files = (('self-streak-habit-tracker-2027.xlsx', habit_tracker), ('self-streak-monthly-budget-india.xlsx', budget_india),
             ('self-streak-emi-tracker.xlsx', emi_tracker), ('self-streak-credit-card-tracker.xlsx', credit_card_tracker),
             ('self-streak-debt-payoff-planner.xlsx', debt_payoff))
    only = sys.argv[1:]   # e.g. `make-templates.py self-streak-emi-tracker.xlsx` rebuilds just that file
    for name, fn in files:
        if only and name not in only: continue
        p = os.path.join(OUT, name); fn().save(p); print(f'templates/{name}  {os.path.getsize(p):,} bytes')
