import { api } from './client.js'

export async function login(email, password) {
  const data = await api('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  })
  if (data.access_token) {
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data))
  }
  return data
}

export async function register(userData) {
  return await api('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData)
  })
}

export async function getProfile() {
  return await api('/auth/me')
}

export function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

export function getCurrentUser() {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
}
