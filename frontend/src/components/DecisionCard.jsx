export default function DecisionCard({ decision }) {
  if (!decision) return null

  const decisionClass = decision.decision?.toLowerCase() || ''
  const riskClass = decision.riskLevel?.toLowerCase() || ''

  return (
    <div className="decision-card">
      <div className="decision-badge" data-decision={decisionClass}>
        {decision.decision}
      </div>
      <div className="risk-score">
        <span className="score-value">{decision.riskScore}</span>
        <span className="score-label">Risk Score</span>
      </div>
      <div className="risk-level-badge" data-level={riskClass}>
        {decision.riskLevel}
      </div>
    </div>
  )
}
