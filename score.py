"""Scores three fictional vendors against ddq_content. Response strings are explicit and auditable: one digit per question, in questionnaire order
(2 = yes with evidence, 1 = claimed or partial, 0 = no or unknown). Also runs a weighting sensitivity analysis and writes data files."""
import json, csv, statistics
from ddq_content import SECTIONS
Qs = [(s, q) for s, qs in SECTIONS for q in qs]
with open("data/checklist.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "domain", "question", "evidence_required", "weight", "knockout", "framework_refs"])
    for s, q in Qs: w.writerow([q[0], s, q[1], q[3], q[4], q[5], q[6]])
R = {  # per domain, 6 digits
 "Meridian HR Cloud": "221221 222221 221122 222112 221211 221212 221211 211122",
 "Atlas Analytics":   "221122 222112 222221 211111 211111 210012 222211 211111",
 "QuickScreen AI":    "112010 012011 211010 010100 100100 110010 102100 100110"}
resp = {v: [int(c) for c in s.replace(" ", "")] for v, s in R.items()}
assert all(len(r) == len(Qs) for r in resp.values())
json.dump({v: {q[0]: r[i] for i, (_, q) in enumerate(Qs)} for v, r in resp.items()}, open("data/vendor_responses.json", "w"), indent=1)
doms = [s for s, _ in SECTIONS]
hu = lambda x: int(x + 0.5)   # round half up, matching Excel ROUND (Python round() is banker's rounding)
def score(r, weights=None, evidence_discount=0.5):
    out = {}; tot = mx = 0
    for d in doms:
        n = m = 0
        for i, (s, q) in enumerate(Qs):
            if s != d: continue
            w = (weights or {}).get(q[0], q[4]); v = r[i]; v = evidence_discount if v == 1 else v / 1 if v == 0 else 2
            n += (0 if r[i] == 0 else (2 * evidence_discount if r[i] == 1 else 2)) * w; m += 2 * w
        out[d] = hu(100 * n / m); tot += n; mx += m
    ko = [q[0] for i, (_, q) in enumerate(Qs) if q[5] == "Y" and r[i] == 0]
    total = hu(100 * tot / mx)
    outcome = "Reject" if ko and total < 50 else "Conditional" if ko or total < 75 or min(out.values()) < 50 else "Approve"
    return dict(total=total, domains=out, knockouts=ko, outcome=outcome)
res = {v: score(r) for v, r in resp.items()}
# sensitivity: equal weights, double weight on fairness+security, and a harsher evidence discount
fs = {q[0]: q[4] * 2 for s, q in Qs if s.startswith(("4", "6"))}
sens = {}
for v, r in resp.items():
    sens[v] = {"Base": res[v], "Equal weights": score(r, {q[0]: 1 for _, q in Qs}), "Double fairness and security": score(r, {q[0]: fs.get(q[0], q[4]) for _, q in Qs}), "Claims worth 0.25 not 0.5": score(r, evidence_discount=0.25)}
# rank stability and score range
for v in sens: sens[v]["range"] = [min(x["total"] for k, x in sens[v].items() if k != "range"), max(x["total"] for k, x in sens[v].items() if k != "range")]
json.dump(dict(scores=res, sensitivity=sens), open("data/scores.json", "w"), indent=1)
for v, s in res.items(): print(v, s["total"], s["outcome"], s["knockouts"], min(s["domains"].values()))
for v in sens: print(v, {k: (x["total"], x["outcome"]) for k, x in sens[v].items() if k != "range"})
