import { CATEGORIES, PRODUCTS } from '../../data/data.js'

function countCat(key) {
  return key === 'all' ? PRODUCTS.length : PRODUCTS.filter((p) => p.cat === key).length
}

export default function Sidebar({ state, dispatch }) {
  const { cat, type, checks, search } = state

  return (
    <aside className="sidebar">
      <div>
        <div className="sb-label">Search</div>
        <div className="search-wrap">
          <svg className="search-icon" viewBox="0 0 16 16" fill="none">
            <circle cx="6.5" cy="6.5" r="4" stroke="currentColor" strokeWidth="1.2" />
            <path d="M10 10l3 3" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
          </svg>
          <input
            className="search-input"
            placeholder="Product, ingredient…"
            value={search}
            onChange={(e) => dispatch({ type: 'SET_SEARCH', value: e.target.value })}
          />
        </div>
      </div>

      <div>
        <div className="sb-label">Category</div>
        <div className="cat-list">
          {CATEGORIES.map((c) => (
            <div
              key={c.key}
              className={`cat-item ${cat === c.key ? 'active' : ''}`}
              onClick={() => dispatch({ type: 'SET_CAT', value: c.key })}
            >
              <div className="cat-left">
                <div className="cat-dot" style={{ background: c.color }} />
                {c.label}
              </div>
              <span className="cat-count">{countCat(c.key)}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="divider" />

      <div>
        <div className="sb-label">Trend status</div>
        <div className="check-list">
          {[
            { key: 'hot',    label: 'Hot (9–10)',   color: 'var(--orange)' },
            { key: 'rising', label: 'Rising (7–8)', color: 'var(--green)' },
            { key: 'new',    label: 'New entry',    color: 'var(--navy-mid)' },
          ].map(({ key, label, color }) => (
            <div key={key} className="check-row" onClick={() => dispatch({ type: 'TOGGLE_CHECK', key })}>
              <div className={`check-box ${checks[key] ? 'active' : ''}`}>
                {checks[key] && (
                  <svg width="10" height="10" viewBox="0 0 10 10">
                    <path d="M2 5l2.5 2.5L8 3" stroke="white" strokeWidth="1.3" strokeLinecap="round" fill="none" />
                  </svg>
                )}
              </div>
              <span className="check-pip" style={{ background: color }} />
              {label}
            </div>
          ))}
        </div>
      </div>

      <div className="divider" />

      <div>
        <div className="sb-label">Opportunity type</div>
        <div className="type-list">
          {[
            { key: 'all',        label: 'All types' },
            { key: 'distribute', label: 'Distribute existing' },
            { key: 'develop',    label: 'Develop PoP brand' },
          ].map(({ key, label }) => (
            <div
              key={key}
              className={`type-item ${type === key ? 'active' : ''}`}
              onClick={() => dispatch({ type: 'SET_TYPE', value: key })}
            >
              {label}
            </div>
          ))}
        </div>
      </div>
    </aside>
  )
}
