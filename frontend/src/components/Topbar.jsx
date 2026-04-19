export default function Topbar({ page, setPage }) {
  return (
    <div className="topbar">
      <div className="logo-area">
        <div className="logo-mark">PoP</div>
        <span className="logo-text">Prince of Peace &mdash; Trend Intelligence</span>
      </div>
      <nav className="nav">
        <button
          className={`nav-btn ${page === 'home' ? 'active' : ''}`}
          onClick={() => setPage('home')}
        >
          Home
        </button>
        <button
          className={`nav-btn ${page === 'browse' ? 'active' : ''}`}
          onClick={() => setPage('browse')}
        >
          Browse
        </button>
      </nav>
    </div>
  )
}
