import { useEffect } from 'react'

export default function ProductPopup({ product, onClose }) {
  if (!product) return null

  const displayIcon = product.icon || '📦'
  const catLabel = product.cat || ''
  const recommendation = product.existing === 1
    ? 'Existing - Expand Distribution'
    : 'New Product - Develop'
  const statusColor = product.existing === 1 ? '#185FA5' : '#2E7D52'

  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  const keywords = product.keywords || []

  return (
    <div className="popup-overlay" onClick={(e) => { if (e.target === e.currentTarget) onClose() }}>
      <div className="popup">
        <button className="popup-close" onClick={onClose}>&times;</button>
        <div className="popup-header">
          <div className="popup-icon">{displayIcon}</div>
          <div className="popup-name">{product.name}</div>
          <div className="popup-cat">{catLabel}</div>
        </div>
        <div className="popup-body">
          <div className="popup-row">
            <div className="popup-label">Signal strength</div>
            <div className="popup-value">{product.signal}/10</div>
          </div>
          <div className="popup-row">
            <div className="popup-label">Shelf life</div>
            <div className="popup-value">
              {product.shelf_life || 'N/A'}
            </div>
          </div>
          <div className="popup-row">
            <div className="popup-label">Country of origin</div>
            <div className="popup-value">{product.country_of_origin || 'N/A'}</div>
          </div>
          <div className="popup-row">
            <div className="popup-label">Ingredients</div>
            <div className="popup-value">{product.ingredients?.join(', ') || 'N/A'}</div>
          </div>
          {keywords.length > 0 && (
            <div className="popup-row">
              <div className="popup-label">Related trends</div>
              <div className="popup-value">
                <div className="popup-keywords">
                  {keywords.map((kw) => (
                    <span key={kw} className="popup-keyword">{kw}</span>
                  ))}
                </div>
              </div>
            </div>
          )}
          <div className="popup-row">
            <div className="popup-label">Recommendation</div>
            <div className="popup-value" style={{ color: statusColor, fontWeight: 600 }}>
              {recommendation}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
