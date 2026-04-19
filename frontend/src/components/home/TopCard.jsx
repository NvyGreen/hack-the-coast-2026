import { useEffect, useRef } from 'react'

export default function TopCard({ rank, name, cat, signal, bar, color, badge, approved, icon }) {
  const barRef = useRef(null)

  useEffect(() => {
    const frame = requestAnimationFrame(() => {
      if (barRef.current) barRef.current.style.width = bar + '%'
    })
    return () => cancelAnimationFrame(frame)
  }, [bar])

  return (
    <div className="card">
      <span className="card-rank">#{rank}</span>
      <span className={`card-status ${approved ? 'status-approved' : 'status-rejected'}`}>
        {approved ? '✔' : '✖'}
      </span>
      <span className={`card-badge ${badge === 'hot' ? 'badge-hot' : 'badge-new'}`}>
        {badge === 'hot' ? 'Hot' : 'New'}
      </span>
      <div className="card-icon">{icon}</div>
      <div className="card-name">{name}</div>
      <div className="card-cat">{cat}</div>
      <div className="bar-wrap">
        <div ref={barRef} className="bar" style={{ background: color, width: 0 }} />
      </div>
      <div className="card-score">{signal}/10 signal strength</div>
    </div>
  )
}
