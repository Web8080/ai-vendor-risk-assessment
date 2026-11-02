# AI Vendor Risk Management Standard (v1.0)

**Owner:** Head of Procurement with GRC. **Applies to:** any third-party product or service that contains AI or processes our data with AI. **Review:** annually.

## 1. Lifecycle
| Stage | Activity | Output | Accountable |
|---|---|---|---|
| 1 Intake | Business owner completes the inherent-risk intake workbook | Tier 1 to 4 | Business owner |
| 2 Due diligence | Vendor completes the DDQ; depth set by tier | Completed DDQ plus evidence | Procurement |
| 3 Validation | Reviewers verify evidence; test where possible (sandbox, local bias test) | Reviewer scores | GRC, Security, Privacy, Legal |
| 4 Decision | Apply decision rule; exceptions need a named executive | Approve, Conditional, Reject | AI governance board |
| 5 Contract | AI schedule and conditions embedded | Signed contract | Legal |
| 6 Onboarding | Register in AI inventory; DPIA; owner assigned | Inventory entry | Business owner |
| 7 Monitoring | KPIs, change notices, periodic re-assessment | Monitoring record | GRC |
| 8 Exit | Data return and deletion; lessons learned | Exit certificate | Procurement |

## 2. Tiers and depth
| Tier | Trigger (examples) | Due diligence | Reassess |
|---|---|---|---|
| 1 Critical | Decisions about individuals; special-category data; Annex III system | Full DDQ, all evidence verified, independent audit, board sign-off | 6 months |
| 2 High | Customer-facing; confidential or regulated data | Full DDQ, knockouts and weight-3 verified | 12 months |
| 3 Medium | Internal productivity with some personal data | DDQ sections 2, 6, 8 plus attestation | 24 months |
| 4 Low | No personal data, no decisions | Standard security and privacy checks | At renewal |

## 3. Decision rule
Approve: total at least 75%, no domain under 50%, no knockout failed. Conditional: conditions agreed in writing with dates. Reject: knockout failed and total under 50%. A failed knockout can only be waived by a documented risk acceptance (form provided), signed by an executive, time-limited to 12 months.

## 4. Evidence rules
Claims without evidence earn half credit. Evidence must be dated within 12 months and cover the product in scope. Reviewers record what they checked. Live demonstration may substitute for documents when logged.

## 5. Triggers for re-assessment
Material model change; security or privacy incident; change of sub-processor or foundation model; regulatory change; adverse monitoring signal; contract renewal.

## 6. RACI (summary)
Business owner: A for intake and use. Procurement: R for process. GRC: R for scoring and challenge. Security, Privacy, Legal: R for their domains. Governance board: A for decisions.
