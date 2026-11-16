import { api } from './client.js'

export async function makeDeposit(memberId, amount, phoneNumber, channel = 'mpesa') {
  return await api('/savings/deposit', {
    method: 'POST',
    body: JSON.stringify({
      member_id: Number(memberId),
      amount: parseFloat(amount),
      phone_number: phoneNumber,
      payment_channel: channel
    })
  })
}

export async function getSavingsSummary(memberId) {
  return await api(`/savings/account/${memberId}`)
}

export async function getLedgerJournal(memberId) {
  return await api(`/savings/ledger/${memberId}`)
}

export async function getAllTransactions(limit = 100) {
  return await api(`/savings/transactions?limit=${limit}`)
}

export async function getGroupSummary() {
  return await api('/savings/summary')
}
