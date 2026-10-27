import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './routes/ProtectedRoute'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import MemberDashboard from './pages/member/Dashboard'
import LoanApplication from './pages/member/LoanApplication'
import Deposits from './pages/member/Deposits'
import Savings from './pages/member/Savings'
import Statements from './pages/member/Statements'
import AdminDashboard from './pages/admin/Dashboard'
import LoanApprovals from './pages/admin/LoanApprovals'
import MemberRegister from './pages/admin/MemberRegister'
import AuditStatements from './pages/admin/AuditStatements'
import Reconciliation from './pages/admin/Reconciliation'
import NotFound from './pages/NotFound'

const member = (page) => <ProtectedRoute role="member">{page}</ProtectedRoute>
const admin = (page) => <ProtectedRoute role="admin">{page}</ProtectedRoute>

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/dashboard" element={member(<MemberDashboard />)} />
        <Route path="/deposits" element={member(<Deposits />)} />
        <Route path="/savings" element={member(<Savings />)} />
        <Route path="/loans/apply" element={member(<LoanApplication />)} />
        <Route path="/statements" element={member(<Statements />)} />

        <Route path="/admin/dashboard" element={admin(<AdminDashboard />)} />
        <Route path="/admin/deposits" element={admin(<Reconciliation />)} />
        <Route path="/admin/loans" element={admin(<LoanApprovals />)} />
        <Route path="/admin/members" element={admin(<MemberRegister />)} />
        <Route path="/admin/reports" element={admin(<AuditStatements />)} />

        <Route path="*" element={<ProtectedRoute><NotFound /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  )
}
