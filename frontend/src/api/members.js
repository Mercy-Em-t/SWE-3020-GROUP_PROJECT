import { api } from './client.js'

export async function getMembers(skip = 0, limit = 100) {
  return await api(`/members?skip=${skip}&limit=${limit}`)
}
