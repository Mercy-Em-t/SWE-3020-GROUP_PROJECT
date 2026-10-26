import { api } from './client.js'

export async function checkLoanEligibility(memberId) {
  return await api(`/loans/eligibility/${memberId}`)
}

export async function applyForLoan(loanData) {
  return await api('/loans/apply', {
    method: 'POST',
    body: JSON.stringify(loanData)
  })
}

export async function getPendingLoans() {
  return await api('/loans/pending')
}

export async function vetLoan(loanId, decision, reviewNotes = '') {
  return await api(`/loans/${loanId}/vet`, {
    method: 'POST',
    body: JSON.stringify({
      status: decision,
      review_notes: reviewNotes
    })
  })
}

export async function repayLoan(loanId, amount, reference = 'WEB_REPAY') {
  return await api('/loans/repay', {
    method: 'POST',
    body: JSON.stringify({
      loan_id: Number(loanId),
      amount: parseFloat(amount),
      payment_reference: reference
    })
  })
}

export async function getMemberLoans(memberId) {
  return await api(`/loans/member/${memberId}`)
}

export async function getAuditLogs(limit = 50) {
  return await api(`/audit/logs?limit=${limit}`)
}
