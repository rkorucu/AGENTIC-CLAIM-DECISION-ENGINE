import { useState } from 'react'
import lowRisk from '../samples/claim_low_risk.json'
import mediumRisk from '../samples/claim_medium_risk.json'
import highRisk from '../samples/claim_high_risk.json'

const SAMPLES = { LOW: lowRisk, MED: mediumRisk, HIGH: highRisk }

export default function ClaimForm({ onSubmit, loading }) {
  const [form, setForm] = useState({
    claimId: '',
    claimant: { fullName: '', state: '' },
    policy: { policyId: '', coverageType: 'AUTO', coverageLimit: 25000, deductible: 500, active: true },
    incident: { type: 'COLLISION', date: '', description: '' },
    claim: { amount: 0, priorClaimsCount: 0, hasPoliceReport: false, attachmentsCount: 0 },
  })

  const loadSample = (level) => {
    setForm(JSON.parse(JSON.stringify(SAMPLES[level])))
  }

  const handleChange = (path, value) => {
    setForm((prev) => {
      const next = JSON.parse(JSON.stringify(prev))
      const parts = path.split('.')
      let cur = next
      for (let i = 0; i < parts.length - 1; i++) {
        const p = parts[i]
        if (!cur[p]) cur[p] = {}
        cur = cur[p]
      }
      cur[parts[parts.length - 1]] = value
      return next
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(form)
  }

  return (
    <form onSubmit={handleSubmit} className="claim-form">
      <div className="form-actions">
        <button type="button" onClick={() => loadSample('LOW')} className="btn btn-sample btn-low">
          Load sample LOW
        </button>
        <button type="button" onClick={() => loadSample('MED')} className="btn btn-sample btn-med">
          Load sample MED
        </button>
        <button type="button" onClick={() => loadSample('HIGH')} className="btn btn-sample btn-high">
          Load sample HIGH
        </button>
      </div>

      <fieldset>
        <legend>Claim</legend>
        <label>Claim ID</label>
        <input
          value={form.claimId}
          onChange={(e) => handleChange('claimId', e.target.value)}
          placeholder="CLM-2024-001"
        />
      </fieldset>

      <fieldset>
        <legend>Claimant</legend>
        <label>Full Name</label>
        <input
          value={form.claimant.fullName}
          onChange={(e) => handleChange('claimant.fullName', e.target.value)}
        />
        <label>State</label>
        <input
          value={form.claimant.state}
          onChange={(e) => handleChange('claimant.state', e.target.value)}
          placeholder="CA"
        />
      </fieldset>

      <fieldset>
        <legend>Policy</legend>
        <label>Policy ID</label>
        <input
          value={form.policy.policyId}
          onChange={(e) => handleChange('policy.policyId', e.target.value)}
        />
        <label>Coverage Type</label>
        <select
          value={form.policy.coverageType}
          onChange={(e) => handleChange('policy.coverageType', e.target.value)}
        >
          <option value="AUTO">AUTO</option>
          <option value="HOME">HOME</option>
        </select>
        <label>Coverage Limit</label>
        <input
          type="number"
          value={form.policy.coverageLimit}
          onChange={(e) => handleChange('policy.coverageLimit', Number(e.target.value))}
        />
        <label>Deductible</label>
        <input
          type="number"
          value={form.policy.deductible}
          onChange={(e) => handleChange('policy.deductible', Number(e.target.value))}
        />
        <label>
          <input
            type="checkbox"
            checked={form.policy.active}
            onChange={(e) => handleChange('policy.active', e.target.checked)}
          />
          Active
        </label>
      </fieldset>

      <fieldset>
        <legend>Incident</legend>
        <label>Type</label>
        <select
          value={form.incident.type}
          onChange={(e) => handleChange('incident.type', e.target.value)}
        >
          <option value="COLLISION">COLLISION</option>
          <option value="THEFT">THEFT</option>
          <option value="VANDALISM">VANDALISM</option>
        </select>
        <label>Date</label>
        <input
          type="date"
          value={form.incident.date}
          onChange={(e) => handleChange('incident.date', e.target.value)}
        />
        <label>Description</label>
        <textarea
          value={form.incident.description}
          onChange={(e) => handleChange('incident.description', e.target.value)}
          rows={3}
        />
      </fieldset>

      <fieldset>
        <legend>Claim Details</legend>
        <label>Amount</label>
        <input
          type="number"
          value={form.claim.amount}
          onChange={(e) => handleChange('claim.amount', Number(e.target.value))}
        />
        <label>Prior Claims Count</label>
        <input
          type="number"
          min={0}
          value={form.claim.priorClaimsCount}
          onChange={(e) => handleChange('claim.priorClaimsCount', Number(e.target.value))}
        />
        <label>
          <input
            type="checkbox"
            checked={form.claim.hasPoliceReport}
            onChange={(e) => handleChange('claim.hasPoliceReport', e.target.checked)}
          />
          Has Police Report
        </label>
        <label>Attachments Count</label>
        <input
          type="number"
          min={0}
          value={form.claim.attachmentsCount}
          onChange={(e) => handleChange('claim.attachmentsCount', Number(e.target.value))}
        />
      </fieldset>

      <button type="submit" className="btn btn-primary" disabled={loading}>
        {loading ? 'Analyzing…' : 'Analyze'}
      </button>
    </form>
  )
}
