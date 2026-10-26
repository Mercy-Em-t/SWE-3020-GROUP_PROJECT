import { api } from './client.js'

export async function login({ phone, email, password }) {
  const cleanPhone = phone ? phone.replace(/\s+/g, '') : null
  const payload = email
    ? { email, password }
    : { phone_number: cleanPhone, password }

  const data = await api('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload)
  })

  if (data.access_token) {
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify({
      id: data.member_id,
      email: data.email,
      role: data.role,
      name: data.email.split('@')[0]
    }))
  }
  return {
    ...data,
    name: data.email.split('@')[0]
  }
}

export async function register(data) {
  const email = data.email || `${(data.phone || 'member').replace(/[^0-9]/g, '')}@sacco.internal`
  return await api('/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      email,
      full_name: data.name || data.full_name || 'SACCO Member',
      phone_number: data.phone || data.phone_number,
      password: data.password,
      role: data.role || 'member'
    })
  })
}

export async function getProfile() {
  return await api('/auth/me')
}

export function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

export function currentUser() {
  try {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : { name: 'Member', role: 'member' }
  } catch {
    return { name: 'Member', role: 'member' }
  }
}

export const getCurrentUser = currentUser
