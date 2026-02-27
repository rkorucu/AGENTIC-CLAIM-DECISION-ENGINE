# API Contract

## ClaimRequest Schema

| Field | Type | Description |
|-------|------|-------------|
| claimId | string | Unique claim identifier |
| claimant | object | Claimant information |
| claimant.fullName | string | Full name |
| claimant.state | string | State code (e.g., CA, TX) |
| policy | object | Policy details |
| policy.policyId | string | Policy identifier |
| policy.coverageType | string | e.g., AUTO, HOME |
| policy.coverageLimit | number | Maximum coverage amount |
| policy.deductible | number | Deductible amount |
| policy.active | boolean | Whether policy is active |
| incident | object | Incident details |
| incident.type | string | e.g., COLLISION, THEFT, VANDALISM |
| incident.date | string | Date of incident |
| incident.description | string | Description text |
| claim | object | Claim details |
| claim.amount | number | Claim amount |
| claim.priorClaimsCount | number | Number of prior claims |
| claim.hasPoliceReport | boolean | Whether police report exists |
| claim.attachmentsCount | number | Number of attachments |

## ClaimDecision Schema

| Field | Type | Description |
|-------|------|-------------|
| decision | string | "APPROVE" \| "REVIEW" \| "REJECT" |
| riskScore | integer | 0-100 |
| riskLevel | string | "LOW" \| "MEDIUM" \| "HIGH" |
| flags | array | Array of flag objects |
| flags[].code | string | Flag code (e.g., POLICY_INACTIVE) |
| flags[].severity | string | "LOW" \| "MEDIUM" \| "HIGH" |
| flags[].message | string | Human-readable message |
| explanation | string | Short paragraph (LLM-generated or fallback) |
| reflectionNotes | array | Array of strings from reflection step |
| toolSummary | object | Optional summary of tool outputs |
| toolSummary.coverageCheck | object | Coverage check result |
| toolSummary.fraudSignals | object | Fraud signal details |

## Endpoints

### Agent Service (FastAPI)

- **GET /health** — Health check
- **POST /analyze** — Body: ClaimRequest, Response: ClaimDecision

### Backend (Spring Boot)

- **GET /actuator/health** — Health check
- **POST /api/claims/analyze** — Body: ClaimRequest, Response: ClaimDecision

## Sample Payloads

See `docs/sample-payloads/`:
- `claim_low_risk.json` — Expected APPROVE
- `claim_medium_risk.json` — Expected REVIEW
- `claim_high_risk.json` — Expected REVIEW or REJECT
