// MOCK AUTH. 
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const NAMES_KEY = 'mock_names'
const normalize = (phone) => phone.replace(/\s/g, '')

function getNames() {
  try {
    return JSON.parse(localStorage.getItem(NAMES_KEY)) || {}
  } catch {
    return {}
  }
}

export async function login({ phone, password }) {
  await delay(300)
  if (!phone.trim() || !password) {
    throw new Error('Enter your phone number and password.')
  }
  const key = normalize(phone)
  const isAdmin = key.endsWith('000')
  const role = isAdmin ? 'admin' : 'member'
  const name = getNames()[key] || (isAdmin ? 'Admin' : 'Member')

  const user = { name, role }
  localStorage.setItem('user', JSON.stringify(user))
  return user
}

export async function register(data) {
  await delay(300)
  if (data.password.length < 8) {
    throw new Error('Password must be at least 8 characters.')
  }
  const names = getNames()
  names[normalize(data.phone)] = data.name // match your form's field name
  localStorage.setItem(NAMES_KEY, JSON.stringify(names))
  return { ok: true }
}