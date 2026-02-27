import { useState, useMemo } from 'react'

const SEVERITY_ORDER = { HIGH: 0, MEDIUM: 1, LOW: 2 }

export default function FlagsTable({ flags }) {
  const [sortBy, setSortBy] = useState('severity')

  const sortedFlags = useMemo(() => {
    if (!flags?.length) return []
    const copy = [...flags]
    if (sortBy === 'severity') {
      copy.sort((a, b) => (SEVERITY_ORDER[a.severity] ?? 99) - (SEVERITY_ORDER[b.severity] ?? 99))
    } else if (sortBy === 'code') {
      copy.sort((a, b) => (a.code || '').localeCompare(b.code || ''))
    }
    return copy
  }, [flags, sortBy])

  if (!flags?.length) {
    return (
      <div className="flags-table empty">
        <p>No flags raised.</p>
      </div>
    )
  }

  return (
    <div className="flags-table">
      <div className="flags-header">
        <span>Flags</span>
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="severity">Sort by severity</option>
          <option value="code">Sort by code</option>
        </select>
      </div>
      <table>
        <thead>
          <tr>
            <th>Code</th>
            <th>Severity</th>
            <th>Message</th>
          </tr>
        </thead>
        <tbody>
          {sortedFlags.map((f, i) => (
            <tr key={i} data-severity={f.severity?.toLowerCase()}>
              <td><code>{f.code}</code></td>
              <td><span className="severity-badge">{f.severity}</span></td>
              <td>{f.message}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
