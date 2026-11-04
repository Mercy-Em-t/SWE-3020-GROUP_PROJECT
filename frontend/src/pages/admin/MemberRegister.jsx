import { useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import StatusTag from '../../components/StatusTag'
import { MEMBERS } from '../../data/mock'
import { formatKES, isValidKenyanPhone, nextId } from '../../utils/format'

const columns = [
  { key: 'name', label: 'Member' },
  { key: 'role', label: 'Role' },
  { key: 'savings', label: 'Savings balance', render: (r) => <span className="mono">{formatKES(r.savings)}</span> },
  {
    key: 'status',
    label: 'Status',
    render: (r) => (
      <StatusTag status={r.status}>{r.status === 'active' ? 'Active' : 'Pending KYC'}</StatusTag>
    ),
  },
]

export default function MemberRegister() {
  const [members, setMembers] = useState(MEMBERS)
  const [query, setQuery] = useState('')
  const [adding, setAdding] = useState(false)
  const [form, setForm] = useState({ name: '', phone: '', role: 'Member' })
  const [error, setError] = useState('')

  const shown = members.filter((m) => m.name.toLowerCase().includes(query.trim().toLowerCase()))

  const handleAdd = (event) => {
    event.preventDefault()
    if (!form.name.trim()) return setError('Enter the member name.')
    if (!isValidKenyanPhone(form.phone)) return setError('Enter a valid phone number.')
    setError('')
    setMembers([...members, { id: nextId(members), name: form.name.trim(), role: form.role, savings: 0, status: 'review' }])
    setForm({ name: '', phone: '', role: 'Member' })
    setAdding(false)
  }

  return (
    <AppShell title="Member register" subtitle={`${members.length} members`}>
      <div className="toolbar">
        <div className="field grow">
          <label htmlFor="search">Search members</label>
          <input id="search" type="search" value={query} onChange={(e) => setQuery(e.target.value)} />
        </div>
        <button type="button" className="btn-sm primary" onClick={() => setAdding(!adding)}>
          {adding ? 'Cancel' : 'Add member'}
        </button>
      </div>

      {adding && (
        <Card title="Add a member" subtitle="New members start as Pending KYC until verified">
          <form onSubmit={handleAdd} noValidate>
            <div className="field-row three">
              <div className="field">
                <label htmlFor="m-name">Full name</label>
                <input id="m-name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
              </div>
              <div className="field">
                <label htmlFor="m-phone">Phone number</label>
                <input id="m-phone" type="tel" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
              </div>
              <div className="field">
                <label htmlFor="m-role">Role</label>
                <select id="m-role" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
                  <option>Member</option>
                  <option>Treasurer</option>
                  <option>Admin</option>
                </select>
              </div>
            </div>
            {error && <p className="form-error" role="alert">{error}</p>}
            <button type="submit" className="btn-sm primary">Save member</button>
          </form>
        </Card>
      )}

      <Card>
        <DataTable columns={columns} rows={shown} empty="No members match your search." />
      </Card>
    </AppShell>
  )
}
