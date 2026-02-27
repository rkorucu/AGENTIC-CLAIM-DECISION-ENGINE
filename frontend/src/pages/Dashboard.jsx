import { useState } from 'react'
import { analyzeClaim } from '../api/client'
import ClaimForm from '../components/ClaimForm'
import DecisionCard from '../components/DecisionCard'
import FlagsTable from '../components/FlagsTable'
import ReflectionPanel from '../components/ReflectionPanel'

export default function Dashboard() {
  const [decision, setDecision] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async (claimRequest) => {
    setLoading(true)
    setError(null)
    setDecision(null)
    try {
      const result = await analyzeClaim(claimRequest)
      setDecision(result)
    } catch (err) {
      setError(err.message || 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>AgenticClaims</h1>
        <p>AI-powered Insurance Claim Decision Agent</p>
      </header>

      <div className="dashboard-layout">
        <aside className="panel panel-form">
          <h2>Claim Request</h2>
          <ClaimForm onSubmit={handleAnalyze} loading={loading} />
        </aside>

        <main className="panel panel-result">
          <h2>Decision</h2>
          {error && <div className="error-banner">{error}</div>}
          {decision && (
            <>
              <DecisionCard decision={decision} />
              {decision.explanation && (
                <div className="explanation-block">
                  <h3>Explanation</h3>
                  <p>{decision.explanation}</p>
                </div>
              )}
              <FlagsTable flags={decision.flags} />
              <ReflectionPanel reflectionNotes={decision.reflectionNotes} />
            </>
          )}
          {!decision && !error && !loading && (
            <p className="placeholder">Submit a claim or load a sample to analyze.</p>
          )}
        </main>
      </div>
    </div>
  )
}
