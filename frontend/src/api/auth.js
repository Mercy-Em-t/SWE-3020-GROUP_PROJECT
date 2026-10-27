// MOCK AUTH. Replace the bodies with real calls to the FastAPI backend
// (for example POST /api/auth/login) once the endpoints are confirmed.
// Demo: a phone number ending in 000 logs in as an admin/treasurer.
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export function currentUser() {
  try {
    return JSON.parse(localStorage.getItem('user'))
  } catch {
    return null
  }
}

export async function login({ phone, password }) {
  await delay(300)
  if (!phone.trim() || !password) {
    throw new Error('Enter your phone number and password.')
  }
  const isAdmin = phone.replace(/\s/g, '').endsWith('000')
  const user = isAdmin
    ? { name: 'Grace Achieng', role: 'admin' }
    : { name: 'Peter Otieno', role: 'member' }
  localStorage.setItem('user', JSON.stringify(user))
  return user
}

export async function register(data) {
  await delay(300)
  if (data.password.length < 8) {
    throw new Error('Password must be at least 8 characters.')
  }
  return { ok: true }
}

export function logout() {
  localStorage.removeItem('user')
}
