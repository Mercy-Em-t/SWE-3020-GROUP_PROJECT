import AppShell from '../../components/AppShell'
import StatCard from '../../components/StatCard'

// Placeholder data. Replace with calls to the backend.
export default function AdminDashboard() {
  return (
    <AppShell title="Group overview">
      <div className="grid3">
        <StatCard label="Group balance" value="KES 4,286,150" />
        <StatCard label="Pending loan approvals" value="3" />
        <StatCard label="Unreconciled transactions" value="1" />
      </div>
    </AppShell>
  )
}
