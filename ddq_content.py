"""The AI vendor due-diligence questionnaire: 8 domains x 6 questions. Single source for the workbook and data/checklist.csv."""
Q = lambda *a: a
SECTIONS = [
 ("1 Governance and accountability", [
  Q("G01", "Name the executive accountable for AI risk and describe your AI governance structure and policy.", "Role, reporting line, committee, cadence.", "AI policy, org chart", 2, "N", "ISO 42001 5.3; NIST GOVERN 2.1"),
  Q("G02", "Do you hold ISO/IEC 42001, ISO/IEC 27001 or SOC 2 Type II covering this product?", "Scope covers the product.", "Certificates, scope", 2, "N", "ISO 42001; ISO 27001"),
  Q("G03", "Maintain an AI system inventory and risk assessment for this product, reviewed at least annually?", "Last review date.", "Risk assessment", 2, "N", "NIST MAP 1; ISO 23894"),
  Q("G04", "Disclose material sub-processors and foundation-model providers, with locations.", "Names, roles, flow-down terms.", "Sub-processor list", 3, "N", "GDPR Art 28; AI Act Art 25"),
  Q("G05", "State the EU AI Act risk class you assign and your reasoning.", "Class, annex reference, conformity route.", "Classification memo", 3, "N", "AI Act Art 6, Annex III"),
  Q("G06", "Describe independent assurance of AI releases (internal review board or external audit).", "Who, how often.", "Review records", 2, "N", "ISO 42001 9.2")]),
 ("2 Data protection and privacy", [
  Q("P01", "Is our data excluded from training or tuning any model used for others, by default?", "Contract and technical control.", "DPA clause, config", 3, "Y", "GDPR Art 5, 28"),
  Q("P02", "Is there a DPA covering AI processing and cross-border transfers?", "Signed or ready to sign.", "DPA, transfer mechanism", 3, "Y", "GDPR Art 28, 44"),
  Q("P03", "Can data be deleted on request, including logs and derived data? Show the procedure.", "Procedure and test.", "Deletion procedure", 2, "N", "GDPR Art 17"),
  Q("P04", "Are retention periods defined and enforced?", "Periods and automation.", "Retention schedule", 2, "N", "GDPR Art 5(1)(e)"),
  Q("P05", "Has a DPIA been completed for this use case? Provide or support one.", "Completed or template.", "DPIA", 2, "N", "GDPR Art 35"),
  Q("P06", "Is special-category data inferred or processed? How is it controlled?", "Data map and controls.", "Data map", 2, "N", "GDPR Art 9")]),
 ("3 Model performance and testing", [
  Q("M01", "Provide validation evidence on data similar to our use case.", "Study, sample, results.", "Validation report", 3, "N", "NIST MEASURE 2.1; AI Act Art 15"),
  Q("M02", "Provide a model card or equivalent with limits and out-of-scope uses.", "Limits explicit.", "Model card", 2, "N", "NIST MAP 2"),
  Q("M03", "Report accuracy by relevant subgroups and conditions with sample sizes.", "Stratified tables.", "Subgroup results", 3, "N", "NIST MEASURE 2.11"),
  Q("M04", "Describe drift detection and revalidation after changes.", "Triggers and thresholds.", "Monitoring procedure", 2, "N", "NIST MEASURE 2.4"),
  Q("M05", "Can we run our own acceptance test before go-live?", "Sandbox or test data.", "Access", 2, "N", "Local validation"),
  Q("M06", "State uptime, latency and accuracy commitments and how they are measured.", "SLA metrics.", "SLA", 2, "N", "Commercial")]),
 ("4 Fairness and bias", [
  Q("F01", "Has the system been tested for discriminatory impact on protected groups?", "Method, groups, results.", "Bias audit", 3, "Y", "NYC LL144; EEOC UGESP; AI Act Art 10"),
  Q("F02", "Is the audit independent and within the last 12 months?", "Auditor, date.", "Audit summary", 2, "N", "NYC LL144"),
  Q("F03", "Are proxy variables identified and controlled? List features.", "Feature list and tests.", "Feature review", 2, "N", "AI Act Art 10(2)(f)"),
  Q("F04", "Are fairness results shared with customers for each release?", "Release notes.", "Release notes", 1, "N", "NIST MANAGE"),
  Q("F05", "Describe your remediation process when bias is found.", "Procedure, past example.", "Procedure", 2, "N", "NIST MANAGE 2"),
  Q("F06", "Do you test equal opportunity (qualified individuals), not only overall rates?", "Metrics.", "Test report", 2, "N", "NIST MEASURE 2.11")]),
 ("5 Transparency and explainability", [
  Q("T01", "Can the system explain, per decision, the factors that drove the output?", "Demo.", "Sample explanation", 3, "N", "AI Act Art 13, 86"),
  Q("T02", "Are users told when they interact with AI or when AI informed a decision?", "UI evidence.", "Screenshots", 2, "N", "AI Act Art 50"),
  Q("T03", "Are model changes communicated in advance, with the ability to stay on a prior version?", "Notice period.", "Change policy", 2, "N", "ISO 42001 8"),
  Q("T04", "Is documentation sufficient for us to meet our own transparency duties?", "Instructions for use.", "Documentation pack", 2, "N", "AI Act Art 13, 26"),
  Q("T05", "Do you provide exportable logs for audit?", "Schema and retention.", "Log sample", 2, "N", "AI Act Art 12"),
  Q("T06", "Is there a public description of the AI features and their limits?", "URL.", "Public page", 1, "N", "Transparency")]),
 ("6 Security", [
  Q("S01", "Independent security certification (SOC 2 Type II, ISO 27001) covering the product?", "Report and scope.", "Report", 3, "N", "ISO 27001"),
  Q("S02", "Tested for AI-specific attacks: prompt injection, poisoning, extraction, adversarial inputs?", "Scope, results.", "Red-team summary", 3, "N", "OWASP LLM Top 10; NIST MEASURE 2.7"),
  Q("S03", "Role-based access to our data, logged and reviewed?", "Policy and sample.", "Access policy", 2, "N", "ISO 27001"),
  Q("S04", "Will you notify us of breaches within 72 hours or less?", "Contract clause.", "Contract", 3, "Y", "GDPR Art 33"),
  Q("S05", "Tested business continuity and exit plan?", "Test date.", "BCP, exit plan", 2, "N", "ISO 22301"),
  Q("S06", "Software supply chain controls (SBOM, dependency scanning, model provenance)?", "Description.", "SBOM", 2, "N", "SLSA; NIST SSDF")]),
 ("7 Human oversight and incident response", [
  Q("H01", "Can a human review and override any consequential output, with overrides logged?", "Workflow.", "Demo", 3, "Y", "AI Act Art 14; GDPR Art 22"),
  Q("H02", "AI incident process with severity levels and timelines?", "Procedure.", "Procedure", 2, "N", "AI Act Art 73"),
  Q("H03", "Kill switch or ability to suspend features quickly?", "Mechanism, time.", "Technical description", 2, "N", "NIST MANAGE 2.4"),
  Q("H04", "User training and guidance on limits and automation bias?", "Materials.", "Training pack", 1, "N", "AI Act Art 4"),
  Q("H05", "Do you disclose incidents affecting other customers where relevant to us?", "Contract.", "Clause", 2, "N", "Good practice"),
  Q("H06", "Do you provide a candidate or user appeal route support?", "Features.", "Description", 2, "N", "GDPR Art 22")]),
 ("8 Legal, contractual and regulatory", [
  Q("L01", "Do you map the product to applicable regulation (AI Act class, sector rules)?", "Mapping.", "Compliance mapping", 3, "N", "AI Act; sector"),
  Q("L02", "Liability for AI errors and IP/data indemnity addressed?", "Draft terms.", "Contract draft", 2, "N", "Commercial"),
  Q("L03", "Audit rights and right to documentation on request?", "Clause.", "Contract", 3, "N", "AI Act Art 26"),
  Q("L04", "Service levels for accuracy, availability and support?", "SLA.", "SLA", 2, "N", "Commercial"),
  Q("L05", "Right to terminate and retrieve data if non-compliant?", "Clause.", "Termination clause", 2, "N", "Commercial"),
  Q("L06", "Insurance: cyber and professional indemnity limits?", "Limits.", "Certificates", 1, "N", "Commercial")])]
