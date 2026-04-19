import { useEffect } from 'react'
import { PRODUCTS, PRODUCT_DETAILS, DEFAULT_DETAILS } from '../../data/data.js'

export default function ProductPopup({ name, onClose }) {
  const product = PRODUCTS.find((p) => p.name === name)
  const data = PRODUCT_DETAILS[name] || DEFAULT_DETAILS
  const catLabel = product ? product.cat.charAt(0).toUpperCase() + product.cat.slice(1) : ''

  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  if (!product) return null

  return (
    <div className="popup-overlay" onClick={(e) => { if (e.target === e.currentTarget) onClose() }}>
      <div className="popup">
        <button className="popup-close" onClick={onClose}>&times;</button>
        <div className="popup-header">
          <div className="popup-icon">{product.icon}</div>
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
            <div className="popup-value">{data.shelfLife} months</div>
          </div>
          <div className="popup-row">
            <div className="popup-label">Country of origin</div>
            <div className="popup-value">{data.origin}</div>
          </div>
          <div className="popup-row">
            <div className="popup-label">Ingredients</div>
            <div className="popup-value">{data.ingredients}</div>
          </div>
          <div className="popup-row">
            <div className="popup-label">Related trends</div>
            <div className="popup-value">
              <div className="popup-keywords">
                {data.keywords.map((kw) => (
                  <span key={kw} className="popup-keyword">{kw}</span>
                ))}
              </div>
            </div>
          </div>
          <div className="popup-row">
            <div className="popup-label">Recommendation</div>
            <div className="popup-value" style={{ color: data.statusColor, fontWeight: 600 }}>
              {data.status}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
