// PLACEHOLDER DATA. Replace each export with a call to the backend API.

export const MEMBER = { name: 'Peter Otieno', savings: 82400, dividends: 6150, outstanding: 0 }
export const GUARANTORS = ['Grace Achieng', 'Mary Wanjiru', 'James Kariuki']

export const MEMBER_DEPOSITS = [
  { id: 1, ref: 'TQ48J9', date: 'Today, 7:52 AM', amount: 1000, status: 'matched' },
  { id: 2, ref: 'TP31B7', date: 'Sep 24', amount: 1500, status: 'matched' },
  { id: 3, ref: 'TN20Q1', date: 'Aug 24', amount: 1500, status: 'matched' },
]

export const MEMBER_NOTIFICATIONS = [
  { id: 1, tone: 'amber', title: 'Deposit due in 2 days', text: 'KES 1,000 monthly contribution' },
  { id: 2, tone: 'green', title: 'Dividend posted', text: 'KES 6,150 added to your account' },
]

export const MONTHLY_SAVINGS = [
  { month: 'Apr', amount: 9000 },
  { month: 'May', amount: 11500 },
  { month: 'Jun', amount: 10000 },
  { month: 'Jul', amount: 14500 },
  { month: 'Aug', amount: 13000 },
  { month: 'Sep', amount: 18000 },
]

export const DIVIDENDS = [
  { id: 1, period: 'Q1 2026', amount: 1800, status: 'matched' },
  { id: 2, period: 'Q2 2026', amount: 2200, status: 'matched' },
  { id: 3, period: 'Q3 2026', amount: 2150, status: 'matched' },
]

export const MEMBER_STATEMENTS = [
  { id: 1, title: 'September 2026 statement', period: 'Sep 1-30' },
  { id: 2, title: 'August 2026 statement', period: 'Aug 1-31' },
  { id: 3, title: 'Q3 2026 dividend statement', period: 'Jul-Sep' },
]

export const GROUP_DEPOSITS = [
  { id: 1, member: 'Peter Otieno', source: 'M-Pesa', ref: 'TQ48J9', date: 'Today, 7:52 AM', amount: 1000, status: 'matched' },
  { id: 2, member: 'Grace Achieng', source: 'M-Pesa', ref: 'TQ48K2', date: 'Today, 8:14 AM', amount: 2500, status: 'matched' },
  { id: 3, member: 'Group account', source: 'Bank (Co-op)', ref: 'BK1123', date: 'Yesterday', amount: 18000, status: 'pending' },
  { id: 4, member: 'Mary Wanjiru', source: 'M-Pesa', ref: 'TQ47D2', date: 'Yesterday', amount: 3200, status: 'matched' },
]

export const LOAN_REQUESTS = [
  { id: 1, member: 'Peter Otieno', amount: 35000, purpose: 'School fees', guarantors: 2, status: 'pending' },
  { id: 2, member: 'Mary Wanjiru', amount: 20000, purpose: 'Business capital', guarantors: 1, status: 'pending' },
  { id: 3, member: 'James Kariuki', amount: 60000, purpose: 'Emergency', guarantors: 2, status: 'pending' },
]

export const MEMBERS = [
  { id: 1, name: 'Grace Achieng', role: 'Treasurer', savings: 138000, status: 'active' },
  { id: 2, name: 'Peter Otieno', role: 'Member', savings: 82400, status: 'active' },
  { id: 3, name: 'Mary Wanjiru', role: 'Member', savings: 54900, status: 'review' },
  { id: 4, name: 'James Kariuki', role: 'Admin', savings: 210000, status: 'active' },
]

export const AUDIT_LOG = [
  { id: 4, time: '08:14', actor: 'G. Achieng', action: 'logged a deposit of KES 2,500' },
  { id: 3, time: 'Yesterday', actor: 'System', action: 'reconciled 14 M-Pesa transactions' },
  { id: 2, time: 'Yesterday', actor: 'M. Wanjiru', action: 'submitted a loan application' },
  { id: 1, time: 'Sep 24', actor: 'G. Achieng', action: "approved Peter Otieno's loan" },
]

export const GROUP_STATEMENTS = [
  { id: 1, title: 'September 2026', period: 'Sep 1-30', type: 'Group summary' },
  { id: 2, title: 'Q3 2026 dividends', period: 'Jul-Sep', type: 'Per-member' },
]
