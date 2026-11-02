"""Builds (1) the blank DDQ, (2) a completed example for one vendor, (3) the internal inherent-risk intake workbook. Then recalculates with LibreOffice and cross-checks formulas against score.py."""
import json, subprocess, os, shutil
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from grc_kit import render_questionnaire
from ddq_content import SECTIONS
Q = dict(title="AI Vendor Due Diligence Questionnaire (DDQ)", purpose="To obtain evidence on governance, data protection, performance, fairness, transparency, security, oversight and contractual terms before we contract for an AI-enabled product.",
 respondent="Vendor accountable executive plus product, privacy, security, data science and legal leads. One named signatory.",
 instructions=["1. Answer all 48 questions in column F using the drop-down.", "2. Unsupported claims score half. Cite document, section and date in column H and attach it.", "3. Knockout questions (column D = Y) are mandatory controls; a No blocks approval unless a named executive signs an exception.", "4. Return within 15 working days. Responses are verified and may be audited.", "5. Reviewers complete columns L to O."],
 scoring=dict(rule="Approve: total at least 75%, no domain under 50%, no knockout No. Otherwise Conditional. Reject: any knockout No and total under 50%.", approve=75, domain_min=50), sections=SECTIONS)
render_questionnaire(Q, "docs/AI_Vendor_DDQ.xlsx")
# completed example: Atlas Analytics
resp = json.load(open("data/vendor_responses.json"))["Atlas Analytics"]
wb = load_workbook("docs/AI_Vendor_DDQ.xlsx"); ws = wb["Questionnaire"]; LAB = {2: "Yes - evidenced", 1: "Partial / claimed", 0: "No / not in place"}
for r in range(2, ws.max_row + 1):
    qid = ws.cell(r, 1).value; s = resp[qid]; ws.cell(r, 6, LAB[s]); ws.cell(r, 12, s)
    ws.cell(r, 7, {2: "See attached evidence.", 1: "Described in sales documentation; formal evidence to follow.", 0: "Not currently provided."}[s])
    ws.cell(r, 8, {2: f"Evidence pack {qid}.pdf, v2026-09", 1: "Marketing whitepaper (not independently verified)", 0: ""}[s])
    ws.cell(r, 14, {2: "Reviewed, accepted.", 1: "Request evidence; half credit.", 0: "Gap. Follow up."}[s]); ws.cell(r, 15, "Y" if s < 2 else "N")
wb.save("docs/examples/Atlas_Analytics_completed_DDQ.xlsx")
# recalc and verify formulas against python
tmp = "/tmp/recalc"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", tmp, "docs/examples/Atlas_Analytics_completed_DDQ.xlsx"], check=True, capture_output=True, timeout=110)
vals = load_workbook(f"{tmp}/Atlas_Analytics_completed_DDQ.xlsx", data_only=True)["Scoring"]; py = json.load(open("data/scores.json"))["scores"]["Atlas Analytics"]
rows = [[c.value for c in r] for r in vals.iter_rows(min_row=2, max_row=10)]
print("workbook:", [(r[0][:12], r[3], r[4]) for r in rows[:9]]); print("python  :", py["total"], py["outcome"], py["knockouts"], list(py["domains"].values()))
wb_total = [r for r in rows if r[0] == "TOTAL"][0]; assert wb_total[3] == py["total"], (wb_total, py["total"])
assert [r[3] for r in rows[:8]] == list(py["domains"].values()), "domain scores differ"
outcome = [r for r in vals.iter_rows(min_row=11, max_row=18) if r[0].value and "Recommended" in str(r[0].value)][0][1].value
print("workbook outcome:", outcome); assert outcome.upper() == py["outcome"].upper(), (outcome, py["outcome"])
shutil.copy(f"{tmp}/Atlas_Analytics_completed_DDQ.xlsx", "docs/examples/Atlas_Analytics_completed_DDQ.xlsx")  # ship the recalculated copy so values show in any viewer
# inherent-risk intake (internal; business owner completes) -> tier by formula
wb = Workbook(); ws = wb.active; ws.title = "Intake"; H = PatternFill("solid", fgColor="1F3A5F")
for i, h in enumerate(["#", "Question for the business owner", "Answer", "Points"], 1):
    c = ws.cell(1, i, h); c.font = Font(bold=True, color="FFFFFF"); c.fill = H
IQ = [("Does the AI make or materially influence decisions about individuals (hiring, credit, health, education, benefits)?", {"Yes": 5, "Partly": 3, "No": 0}), ("Is the output used with no routine human review?", {"Yes": 4, "Sometimes": 2, "No": 0}), ("Is personal data processed?", {"Special category or children": 5, "Personal data": 3, "None": 0}),
 ("Is our confidential or regulated data sent to the vendor?", {"Regulated": 4, "Confidential": 3, "Public only": 0}), ("Is the system customer-facing?", {"Yes": 3, "Staff only": 1, "No": 0}), ("Is it in an EU AI Act Annex III domain, or would it be a prohibited practice?", {"Prohibited": 10, "Annex III": 5, "No": 0}),
 ("What is the operational impact if it fails or is wrong?", {"Severe": 4, "Moderate": 2, "Minor": 0}), ("Does the vendor use a third-party foundation model?", {"Yes, undisclosed": 3, "Yes, disclosed": 1, "No": 0}), ("Is the vendor hard to replace (lock-in)?", {"Yes": 2, "Partly": 1, "No": 0}), ("Annual contract value or user volume?", {"High": 2, "Medium": 1, "Low": 0})]
LK = wb.create_sheet("Lookup"); r0 = 1; dvs = []
for n, (q, opts) in enumerate(IQ, 2):
    ws.cell(n, 1, n - 1); ws.cell(n, 2, q).alignment = Alignment(wrap_text=True)
    for j, (o, p) in enumerate(opts.items()): LK.cell(r0 + j, 1, o); LK.cell(r0 + j, 2, p)
    rng = f"Lookup!$A${r0}:$A${r0+len(opts)-1}"; dv = DataValidation(type="list", formula1=f"={rng}", allow_blank=True); ws.add_data_validation(dv); dv.add(ws.cell(n, 3))
    ws.cell(n, 4, f'=IFERROR(VLOOKUP(C{n},Lookup!$A${r0}:$B${r0+len(opts)-1},2,FALSE),0)'); r0 += len(opts) + 1
last = len(IQ) + 1
ws.cell(last + 2, 2, "Total inherent risk points").font = Font(bold=True); ws.cell(last + 2, 4, f"=SUM(D2:D{last})")
ws.cell(last + 3, 2, "Inherent risk tier").font = Font(bold=True); ws.cell(last + 3, 4, f'=IF(OR(C7="Prohibited"),"PROHIBITED: stop",IF(D{last+2}>=24,"Tier 1 Critical",IF(D{last+2}>=15,"Tier 2 High",IF(D{last+2}>=7,"Tier 3 Medium","Tier 4 Low"))))')
ws.cell(last + 5, 2, "Tier guide").font = Font(bold=True)
for i, t in enumerate(["Tier 1 Critical: full DDQ, all evidence verified, independent bias/security assessment, legal and board sign-off, reassess every 6 months.", "Tier 2 High: full DDQ, evidence for knockouts, legal and privacy review, reassess annually.", "Tier 3 Medium: DDQ sections 2, 6 and 8, attestation, reassess every 2 years.", "Tier 4 Low: standard security and privacy checks, attestation."], 1): ws.cell(last + 5 + i, 2, t).alignment = Alignment(wrap_text=True)
for col, wd in zip("ABCD", (5, 80, 30, 24)): ws.column_dimensions[col].width = wd
wb.save("docs/AI_Vendor_Inherent_Risk_Intake.xlsx"); print("workbooks built and verified")
