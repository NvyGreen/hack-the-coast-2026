import { useState, useEffect } from 'react'
import { fetchDashboard } from '../../data/api.js'
import TopCard from './TopCard.jsx'
import KeywordCloud from './KeywordCloud.jsx'
import InsightsGrid from './InsightsGrid.jsx'

export default function Home({ setPage }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .catch(setError)
  }, [])

  const stats = data
    ? [
        { val: String(data.stats.trends_scanned),     label: 'Trends scanned' },
        { val: String(data.stats.actionable_signals),  label: 'Actionable signals' },
        { val: String(data.stats.pop_adjacencies),     label: 'PoP adjacencies' },
        { val: String(data.stats.fda_flags_removed),   label: 'FDA flags removed' },
      ]
    : [
        { val: '—', label: 'Trends scanned' },
        { val: '—', label: 'Actionable signals' },
        { val: '—', label: 'PoP adjacencies' },
        { val: '—', label: 'FDA flags removed' },
      ]

  return (
    <>
      <div className="hero">
        <div className="hero-inner">
          <div className="hero-eyebrow">Product Discovery Platform</div>
          <div className="hero-title">
            Find the next trend <em>before</em> competitors do.
          </div>
          <div className="hero-sub">
            AI-powered signal scanning across Amazon, Google Trends, and social
            platforms — filtered against PoP&apos;s sourcing criteria and product categories.
          </div>
        </div>
      </div>

      <div className="stats-strip">
        {stats.map((s) => (
          <div key={s.label} className="stat">
            <div className="stat-inner">
              <div className="stat-val">{s.val}</div>
              <div className="stat-label">{s.label}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="home-body">
        {error && (
          <div style={{ color: 'var(--orange)', fontSize: 13, padding: '0.5rem 0' }}>
            Could not reach backend — start the Flask server and refresh.
          </div>
        )}

        <div>
          <div className="section-header">
            <div className="section-title">
              <div className="section-dot" />
              Top {data ? data.top_products.length : 3} recommendations this week
            </div>
            <div className="section-link" onClick={() => setPage('browse')}>
              See all &rarr;
            </div>
          </div>
          <div className="top5-grid">
            {data
              ? data.top_products.map((p) => (
                  <TopCard
                    key={p.name}
                    rank={p.rank}
                    name={p.name}
                    cat={p.category}
                    signal={p.signal}
                    bar={p.bar}
                    color={p.color}
                    badge={p.badge}
                    approved={p.approved}
                    icon={p.icon}
                  />
                ))
              : [1, 2, 3].map((i) => (
                  <div key={i} className="card" style={{ opacity: 0.4, minHeight: 180 }} />
                ))}
          </div>
        </div>

        <KeywordCloud keywords={data ? data.keywords : null} />
        <InsightsGrid opportunities={data ? data.opportunities : null} />
      </div>
    </>
  )
}
