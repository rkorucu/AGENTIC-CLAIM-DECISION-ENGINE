import { useState } from 'react'

export default function ReflectionPanel({ reflectionNotes }) {
  const [open, setOpen] = useState(false)

  if (!reflectionNotes?.length) return null

  return (
    <div className="reflection-panel">
      <button
        type="button"
        className="accordion-trigger"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
      >
        Reflection Notes ({reflectionNotes.length})
      </button>
      {open && (
        <div className="accordion-content">
          <ul>
            {reflectionNotes.map((note, i) => (
              <li key={i}>{note}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
