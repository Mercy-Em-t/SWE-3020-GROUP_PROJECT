import { api } from './client.js'

export function currentUser() {
  try {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : { id: null, name: 'Member', role: 'member' }
  } catch {
    return { id: null, name: 'Member', role: 'member' }
  }
}

export const getCurrentUser = currentUser

export async function login({ phone, email, password }) {
  if (!password || (!phone && !email)) {
    throw new Error('Enter your phone number (or email) and password.')
  }

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
    const displayName = data.full_name || (data.email ? data.email.split('@')[0] : 'Member')
    const user = {
      id: data.member_id,
      email: data.email,
      role: data.role === 'treasurer' ? 'admin' : data.role,
      name: displayName
    }
    localStorage.setItem('user', JSON.stringify(user))
    return user
  }

  throw new Error('Login failed: invalid response from server.')
}

export async function register(data) {
  if (data.password && data.password.length < 6) {
    throw new Error('Password must be at least 6 characters.')
  }

  const cleanPhone = (data.phone || data.phone_number || '').replace(/\s+/g, '')
  const email = data.email || `${cleanPhone.replace(/[^0-9]/g, '')}@sacco.internal`

  return await api('/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      email,
      full_name: data.fullName || data.name || data.full_name || 'SACCO Member',
      phone_number: cleanPhone,
      password: data.password,
      role: 'member'
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
