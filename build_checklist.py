"""Writes data/checklist.csv. Weight 1 to 3 (importance). knockout=Y means a score of 0 blocks approval without a formal exception."""
import csv
Q = [
("Governance and accountability", [
 ("Has a named executive accountable for AI risk and a published AI policy?", "Policy document, org chart", 2, "N"),
 ("Does the vendor maintain an inventory of its AI systems and model versions?", "Inventory extract", 2, "N"),
 ("Is there an independent review (internal or external) of high-risk releases?", "Review records", 2, "N"),
 ("Does the vendor hold an AI management certification (for example ISO/IEC 42001) or equivalent?", "Certificate and scope", 1, "N"),
 ("Does the vendor disclose material sub-processors and foundation-model providers?", "Sub-processor list", 3, "N")]),
("Data protection and privacy", [
 ("Is our data excluded from training vendor or third-party models by default?", "Contract clause, technical control", 3, "Y"),
 ("Is there a data processing agreement covering AI processing and cross-border transfers?", "Signed DPA", 3, "Y"),
 ("Can data be deleted on request, including from logs and derived datasets?", "Deletion procedure, test", 2, "N"),
 ("Is personal data minimised and are retention periods defined?", "Retention schedule", 2, "N"),
 ("Has a privacy impact assessment been performed for this use case?", "DPIA", 2, "N")]),
("Model performance and testing", [
 ("Is performance documented on data similar to our use case?", "Validation report", 3, "N"),
 ("Are limits and out-of-scope uses documented (model card or equivalent)?", "Model card", 2, "N"),
 ("Are accuracy results broken down by relevant subgroups and conditions?", "Subgroup results", 3, "N"),
 ("Is there a process to detect drift and re-validate after changes?", "Monitoring procedure", 2, "N"),
 ("Can we run our own acceptance test before go-live?", "Sandbox access", 2, "N")]),
("Fairness and bias", [
 ("Has the system been tested for discriminatory impact on protected groups?", "Bias audit report", 3, "Y"),
 ("Is the audit independent and recent (last 12 months)?", "Auditor name, date", 2, "N"),
 ("Are proxy variables identified and controlled?", "Feature review", 2, "N"),
 ("Does the vendor share fairness results for each release?", "Release notes", 1, "N"),
 ("Is there a remediation process if bias is found?", "Procedure", 2, "N")]),
("Transparency and explainability", [
 ("Can the vendor explain, per decision, which factors drove the output?", "Demo, documentation", 3, "N"),
 ("Are users told when they are interacting with AI or when AI informed a decision?", "UI screenshots", 2, "N"),
 ("Are changes to models communicated to customers in advance?", "Change policy", 2, "N"),
 ("Is documentation sufficient for us to meet our own transparency duties?", "Documentation pack", 2, "N"),
 ("Does the vendor provide logs we can export for audit?", "Log sample", 2, "N")]),
("Security", [
 ("Independent security certification (SOC 2 Type II, ISO 27001)?", "Report and scope", 3, "N"),
 ("Is the system tested for AI-specific attacks: prompt injection, data poisoning, model extraction?", "Red-team summary", 3, "N"),
 ("Is access to our data role-based, logged and reviewed?", "Access policy", 2, "N"),
 ("Are breaches notified to us within 72 hours or less?", "Contract clause", 3, "Y"),
 ("Is there a tested business continuity and exit plan?", "BCP, exit plan", 2, "N")]),
("Human oversight and incident response", [
 ("Can a human review and override any consequential output?", "Workflow demo", 3, "Y"),
 ("Is there an AI incident process with defined severity levels and timelines?", "Incident procedure", 2, "N"),
 ("Is there a kill switch or the ability to suspend features quickly?", "Technical description", 2, "N"),
 ("Does the vendor provide user training and guidance on limitations?", "Training materials", 1, "N"),
 ("Are incidents involving other customers disclosed to us when relevant?", "Contract clause", 2, "N")]),
("Legal, contractual and regulatory", [
 ("Does the vendor map its product to applicable regulation (EU AI Act risk class, sector rules)?", "Compliance mapping", 3, "N"),
 ("Is the vendor's liability for AI errors addressed, with indemnity for IP and data claims?", "Contract draft", 2, "N"),
 ("Do we have audit rights and the right to documentation on request?", "Contract clause", 3, "N"),
 ("Are service levels defined for accuracy, availability and support?", "SLA", 2, "N"),
 ("Is there a right to terminate and retrieve data if the system is found non-compliant?", "Termination clause", 2, "N")])]
rows = []; n = 1
for dom, qs in Q:
    for q, ev, w, ko in qs:
        rows.append([f"Q{n:02d}", dom, q, ev, w, ko]); n += 1
with open("data/checklist.csv", "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["id", "domain", "question", "evidence_required", "weight", "knockout"]); wr.writerows(rows)
print(len(rows), "questions")
