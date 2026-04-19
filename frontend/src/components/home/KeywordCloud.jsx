import { useState } from 'react'
import { KEYWORD_POSITIONS } from '../../data/data.js'

const SIZE_MAP    = { xl: 27, lg: 19, md: 15.5, sm: 12 }
const OPACITY_MAP = { hot: 1.0, mid: 0.78, low: 0.52 }

export default function KeywordCloud({ keywords }) {
  const [selected, setSelected] = useState(null)

  const items = keywords || []
  const toggle = (text) => setSelected((prev) => (prev === text ? null : text))

  return (
    <div className="kw-panel">
      <div className="kw-header">
        <div>
          <div className="kw-title">Trending keywords across data sources</div>
          <div className="kw-sub">Sized by search volume &middot; Click any keyword to explore</div>
        </div>
        <div className="kw-legend">
          <div className="legend-item">
            <div className="legend-dot" style={{ background: '#C05621' }} />
            <span style={{ color: '#C05621' }}>Top 40%</span>
          </div>
          <div className="legend-item">
            <div className="legend-dot" style={{ background: 'var(--navy-mid)' }} />
            <span style={{ color: 'var(--navy-mid)' }}>40–80%</span>
          </div>
          <div className="legend-item">
            <div className="legend-dot" style={{ background: 'var(--text-muted)' }} />
            <span style={{ color: 'var(--text-muted)' }}>80–100%</span>
          </div>
        </div>
      </div>

      <div className="kw-cloud">
        {items.map((kw, i) => {
          const fontSize = SIZE_MAP[kw.size] || 12
          const sizeClass = fontSize >= 25 ? 'size-xl' : fontSize >= 18 ? 'size-lg' : fontSize >= 14 ? 'size-md' : 'size-sm'
          const pos = KEYWORD_POSITIONS[i] || { top: `${30 + (i % 5) * 12}%`, left: `${10 + (i % 7) * 12}%` }
          const isSelected = selected === kw.text

          return (
            <div
              key={kw.text}
              className={`kw-tag tier-${kw.tier} ${sizeClass}${isSelected ? ' selected' : ''}`}
              style={{
                position: 'absolute',
                top: pos.top,
                left: pos.left,
                fontSize: `${fontSize}px`,
                opacity: OPACITY_MAP[kw.tier] || 1,
                transform: 'translate(-50%, -50%)',
              }}
              onClick={() => toggle(kw.text)}
            >
              {kw.text}
            </div>
          )
        })}
      </div>
    </div>
  )
}
