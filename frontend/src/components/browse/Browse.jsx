import { useReducer, useMemo, useState, useEffect } from 'react'
import { fetchBrowse } from '../../data/api.js'
import Sidebar from './Sidebar.jsx'
import ProductCard from './ProductCard.jsx'
import ProductPopup from './ProductPopup.jsx'

const initialState = {
  cat: 'all',
  type: 'all',
  sort: 'signal',
  search: '',
  checks: { hot: true, rising: true, new: true },
}

function reducer(state, action) {
  switch (action.type) {
    case 'SET_CAT':      return { ...state, cat: action.value }
    case 'SET_TYPE':     return { ...state, type: action.value }
    case 'SET_SORT':     return { ...state, sort: action.value }
    case 'SET_SEARCH':   return { ...state, search: action.value }
    case 'TOGGLE_CHECK': return { ...state, checks: { ...state.checks, [action.key]: !state.checks[action.key] } }
    case 'CLEAR_CAT':    return { ...state, cat: 'all' }
    case 'CLEAR_TYPE':   return { ...state, type: 'all' }
    default:             return state
  }
}

function filterProducts(products, { cat, type, checks, search, sort }) {
  let list = [...products]
  if (cat !== 'all')  list = list.filter((p) => p.cat === cat)
  if (type !== 'all') list = list.filter((p) => p.type === type)
  list = list.filter((p) => checks[p.badge])
  if (search) {
    const q = search.toLowerCase()
    list = list.filter((p) => p.name.toLowerCase().includes(q) || p.cat.toLowerCase().includes(q))
  }
  if (sort === 'name')          list.sort((a, b) => a.name.localeCompare(b.name))
  else if (sort === 'category') list.sort((a, b) => a.cat.localeCompare(b.cat))
  else                          list.sort((a, b) => b.signal - a.signal)
  return list
}

export default function Browse() {
  const [state, dispatch] = useReducer(reducer, initialState)
  const [products, setProducts] = useState([])
  const [selectedProduct, setSelectedProduct] = useState(null)

  useEffect(() => {
    fetchBrowse().then(setProducts).catch(console.error)
  }, [])

  const filtered = useMemo(() => filterProducts(products, state), [products, state])

  const sortLabel = state.sort === 'signal' ? 'signal strength' : state.sort

  return (
    <div className="page-wrap">
      <Sidebar state={state} dispatch={dispatch} />

      <div className="browse-main">
        <div className="main-header">
          <div className="header-eyebrow">Browse &amp; Filter</div>
          <div className="header-title">All recommendations</div>
          <div className="header-sub">
            {filtered.length} results &middot; Sorted by {sortLabel}
          </div>
        </div>

        <div className="content">
          <div className="toolbar">
            <div className="toolbar-search">
              <svg className="toolbar-icon" viewBox="0 0 16 16" fill="none">
                <circle cx="6.5" cy="6.5" r="4" stroke="currentColor" strokeWidth="1.2" />
                <path d="M10 10l3 3" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
              </svg>
              <input
                className="toolbar-input"
                placeholder="Search by product, ingredient, or category…"
                value={state.search}
                onChange={(e) => dispatch({ type: 'SET_SEARCH', value: e.target.value })}
              />
            </div>
            <select
              className="sort-select"
              value={state.sort}
              onChange={(e) => dispatch({ type: 'SET_SORT', value: e.target.value })}
            >
              <option value="signal">Signal strength</option>
              <option value="name">Name A–Z</option>
              <option value="category">Category</option>
            </select>
          </div>

          <div className="results-meta">
            <div className="results-count">
              Showing <span>{filtered.length}</span> results
            </div>
            <div className="active-chips">
              {state.cat !== 'all' && (
                <div className="chip">
                  {state.cat}
                  <span className="chip-x" onClick={() => dispatch({ type: 'CLEAR_CAT' })}>&times;</span>
                </div>
              )}
              {state.type !== 'all' && (
                <div className="chip">
                  {state.type}
                  <span className="chip-x" onClick={() => dispatch({ type: 'CLEAR_TYPE' })}>&times;</span>
                </div>
              )}
            </div>
          </div>

          <div className="grid">
            {filtered.length === 0 ? (
              <div className="empty">No results match your filters.</div>
            ) : (
              filtered.map((p, i) => (
                <ProductCard key={p.name} product={p} index={i} onClick={setSelectedProduct} />
              ))
            )}
          </div>
        </div>
      </div>

      {selectedProduct && (
        <ProductPopup product={selectedProduct} onClose={() => setSelectedProduct(null)} />
      )}
    </div>
  )
}
