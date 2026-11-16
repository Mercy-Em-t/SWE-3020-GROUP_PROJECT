import { api } from './client.js'

export async function getMembers(skip = 0, limit = 100) {
  return await api(`/members?skip=${skip}&limit=${limit}`)
}

export async function getMemberDirectory() {
  return await api('/members/directory')
}

export async function createMember({ fullName, phoneNumber, email, role = 'member' }) {
  return await api('/members', {
    method: 'POST',
    body: JSON.stringify({
      full_name: fullName,
      phone_number: phoneNumber,
      email: email || null,
      role: role.toLowerCase()
    })
  })
}
