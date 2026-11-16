import { useEffect, useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import StatusTag from '../../components/StatusTag'
import { getMembers, createMember } from '../../api/members'
import { getMemberLoans } from '../../api/loans'
import { getLedgerJournal } from '../../api/deposits'
import { formatKES, isValidKenyanPhone } from '../../utils/format'

export default function MemberRegister() {
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')
  const [adding, setAdding] = useState(false)
  const [form, setForm] = useState({ name: '', phone: '', email: '', role: 'member' })
  const [error, setError] = useState('')
  const [successNotice, setSuccessNotice] = useState('')

  // Member inspect modal state
  const [selectedMember, setSelectedMember] = useState(null)
  const [memberLoans, setMemberLoans] = useState([])
  const [memberTxs, setMemberTxs] = useState([])
  const [inspectLoading, setInspectLoading] = useState(false)

  const loadMembers = async () => {
    try {
      setLoading(true)
      const data = await getMembers()
      setMembers(data)
      setError('')
    } catch (err) {
      setError(err.message || 'Failed to load members.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadMembers()
  }, [])

  const inspectMember = async (member) => {
    setSelectedMember(member)
    setInspectLoading(true)
    try {
      const [loans, txs] = await Promise.all([
        getMemberLoans(member.id),
        getLedgerJournal(member.id)
      ])
      setMemberLoans(loans)
      setMemberTxs(txs)
    } catch (err) {
      console.error(err)
    } finally {
      setInspectLoading(false)
    }
  }

  const columns = [
    { key: 'full_name', label: 'Member' },
    { key: 'role', label: 'Role', render: (r) => (r.role ? r.role.toUpperCase() : 'MEMBER') },
    { key: 'phone_number', label: 'Phone', render: (r) => <span className="mono">{r.phone_number}</span> },
    {
      key: 'total_savings',
      label: 'Savings balance',
      render: (r) => <span className="mono">{formatKES(r.total_savings || 0)}</span>,
    },
    {
      key: 'total_shares',
      label: 'Shares',
      render: (r) => <span className="mono">{formatKES(r.total_shares || 0)}</span>,
    },
    {
      key: 'status',
      label: 'Status',
      render: () => <StatusTag status="active">Active</StatusTag>,
    },
    {
      key: 'action',
      label: 'Inspect',
      render: (r) => (
        <button
          type="button"
          className="btn-sm ghost"
          onClick={() => inspectMember(r)}
        >
          View Activity
        </button>
      ),
    },
  ]

  const shown = members.filter((m) =>
    (m.full_name || '').toLowerCase().includes(query.trim().toLowerCase()) ||
    (m.phone_number || '').includes(query.trim())
  )

  const handleAdd = async (event) => {
    event.preventDefault()
    setSuccessNotice('')
    if (!form.name.trim()) return setError('Enter the member name.')
    if (!isValidKenyanPhone(form.phone)) return setError('Enter a valid phone number.')
    setError('')

    try {
      const res = await createMember({
        fullName: form.name.trim(),
        phoneNumber: form.phone.trim(),
        email: form.email.trim() || undefined,
        role: form.role
      })
      setSuccessNotice(`Member registered! Temporary password: ${res.temporary_password}`)
      setForm({ name: '', phone: '', email: '', role: 'member' })
      setAdding(false)
      loadMembers()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <AppShell title="Member register" subtitle={`${members.length} members`}>
      <div className="toolbar">
        <div className="field grow">
          <label htmlFor="search">Search members</label>
          <input
            id="search"
            type="search"
            placeholder="Search by name or phone..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <button type="button" className="btn-sm primary" onClick={() => setAdding(!adding)}>
          {adding ? 'Cancel' : 'Add member'}
        </button>
      </div>

      {successNotice && <p className="notice" role="status">{successNotice}</p>}

      {adding && (
        <Card title="Add a member" subtitle="Admin-initiated onboarding with role assignment">
          <form onSubmit={handleAdd} noValidate>
            <div className="field-row three">
              <div className="field">
                <label htmlFor="m-name">Full name</label>
                <input
                  id="m-name"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
              <div className="field">
                <label htmlFor="m-phone">Phone number</label>
                <input
                  id="m-phone"
                  type="tel"
                  placeholder="+254 7XX XXX XXX"
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                />
              </div>
              <div className="field">
                <label htmlFor="m-role">Role</label>
                <select
                  id="m-role"
                  value={form.role}
                  onChange={(e) => setForm({ ...form, role: e.target.value })}
                >
                  <option value="member">Member</option>
                  <option value="treasurer">Treasurer</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
            </div>
            {error && <p className="form-error" role="alert">{error}</p>}
            <button type="submit" className="btn-sm primary">Save member</button>
          </form>
        </Card>
      )}

      {selectedMember && (
        <Card
          title={`Member Profile: ${selectedMember.full_name}`}
          subtitle={`Email: ${selectedMember.email} · Phone: ${selectedMember.phone_number}`}
          action={
            <button type="button" className="btn-sm ghost" onClick={() => setSelectedMember(null)}>
              Close Panel
            </button>
          }
        >
          {inspectLoading ? (
            <p className="sub-line">Loading account activity...</p>
          ) : (
            <div className="grid2" style={{ marginTop: '0.5rem' }}>
              <div>
                <h4>Recent Ledger Transactions</h4>
                {memberTxs.length === 0 ? (
                  <p className="sub-line">No deposits recorded.</p>
                ) : (
                  <ul className="audit-list" style={{ marginTop: '0.5rem' }}>
                    {memberTxs.slice(0, 5).map((t) => (
                      <li key={t.id} className="audit-item">
                        <span className="h">{new Date(t.timestamp).toLocaleDateString()}</span>
                        <p><b>+{formatKES(t.amount)}</b> via {t.reference_code}</p>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              <div>
                <h4>Loan Portfolio</h4>
                {memberLoans.length === 0 ? (
                  <p className="sub-line">No active or past loans.</p>
                ) : (
                  <ul className="audit-list" style={{ marginTop: '0.5rem' }}>
                    {memberLoans.map((l) => (
                      <li key={l.id} className="audit-item">
                        <span className="h">{l.status}</span>
                        <p>
                          <b>{formatKES(l.principal_amount)}</b> ({l.duration_months} mo) — Outstanding: {formatKES(l.balance_outstanding)}
                        </p>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          )}
        </Card>
      )}

      {error && !adding && <p className="form-error" role="alert">{error}</p>}

      <Card>
        {loading ? (
          <p className="sub-line">Loading member directory...</p>
        ) : (
          <DataTable columns={columns} rows={shown} empty="No members match your search." />
        )}
      </Card>
    </AppShell>
  )
}
