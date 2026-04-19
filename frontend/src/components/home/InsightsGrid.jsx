import { ALERTS } from '../../data/data.js'

function Opportunities({ opportunities }) {
  const items = opportunities || []
  return (
    <div className="ins-card">
      <div className="ins-title">
        <div className="ins-dot" style={{ background: 'var(--green)' }} />
        PoP product development opportunities
      </div>
      <div className="opp-list">
        {items.map((o) => (
          <div key={o.name} className="opp-row">
            <div className="opp-icon">{o.icon}</div>
            <div style={{ flex: 1 }}>
              <div className="opp-name">{o.name}</div>
              <div className="opp-sub">{o.sub}</div>
            </div>
            <div className="opp-badge" style={{ background: o.bc, color: o.bt }}>{o.badge}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

function SourcingAlerts() {
  return (
    <div className="ins-card">
      <div className="ins-title">
        <div className="ins-dot" style={{ background: 'var(--orange)' }} />
        Sourcing alerts &amp; market signals
      </div>
      <div className="alert-chip">
        <div className="chip-dot" />
        Updated April 18, 2026
      </div>
      <div className="alert-list">
        {ALERTS.map((a, i) => (
          <div key={i} className="alert-row">
            <div className="alert-dot" style={{ background: a.color }} />
            <div className="alert-text" dangerouslySetInnerHTML={{ __html: a.html }} />
          </div>
        ))}
      </div>
    </div>
  )
}

export default function InsightsGrid({ opportunities }) {
  return (
    <div className="insights-grid">
      <Opportunities opportunities={opportunities} />
      <SourcingAlerts />
    </div>
  )
}
