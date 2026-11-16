import { Link } from 'react-router-dom'

export default function StatCard({ label, value, to }) {
  const content = (
    <>
      <span className="label">{label}</span>
      <b>{value}</b>
    </>
  )

  if (to) {
    return (
      <Link to={to} className="card stat-card stat-card-link" style={{ textDecoration: 'none', color: 'inherit' }}>
        {content}
      </Link>
    )
  }

  return (
    <div className="card stat-card">
      {content}
    </div>
  )
}
