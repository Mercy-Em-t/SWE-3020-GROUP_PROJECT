export default function StatCard({ label, value }) {
  return (
    <div className="card stat-card">
      <span className="label">{label}</span>
      <b>{value}</b>
    </div>
  )
}
