export default function ProductCard({ product, index, onClick }) {
  const { name, cat, signal, approved, icon, type } = product
  const catLabel = cat.charAt(0).toUpperCase() + cat.slice(1)
  const typeStyle = type === 'develop'
    ? { background: '#EAF5EE', color: '#2E7D52' }
    : { background: '#EBF3FD', color: '#185FA5' }
  const typeLabel = type === 'develop' ? 'Develop' : 'Distribute'

  const pips = [0, 1, 2, 3, 4].map((j) => {
    const filled = j < Math.round(signal / 2)
    const strong = filled && signal >= 8
    return { filled, strong, height: 10 + j * 3 }
  })

  return (
    <div
      className="product-card"
      style={{ animationDelay: `${index * 30}ms` }}
      onClick={() => onClick(name)}
    >
      <span className={`product-card-status ${approved ? 'status-approved' : 'status-rejected'}`}>
        {approved ? '✔' : '✖'}
      </span>
      <div className="product-card-icon">{icon}</div>
      <div className="card-name">{name}</div>
      <div className="card-cat">{catLabel}</div>
      <div className="card-divider" />
      <div className="card-bottom">
        <div>
          <div className="signal-label">Trend signal</div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div className="pips">
              {pips.map((p, j) => (
                <div
                  key={j}
                  className={`pip${p.filled ? (p.strong ? ' strong' : ' active') : ''}`}
                  style={{ height: p.height }}
                />
              ))}
            </div>
            <span className="signal-score">{signal}/10</span>
          </div>
        </div>
        <div className="type-badge" style={typeStyle}>{typeLabel}</div>
      </div>
    </div>
  )
}
