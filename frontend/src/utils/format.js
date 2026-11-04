export const formatKES = (n) => `KES ${Number(n).toLocaleString('en-US')}`

// Accepts 07XXXXXXXX, 01XXXXXXXX, +2547XXXXXXXX, +2541XXXXXXXX (spaces allowed)
export const isValidKenyanPhone = (value) =>
  /^(\+254|0)[17]\d{8}$/.test(value.replace(/\s/g, ''))

export const nextId = (list) => Math.max(0, ...list.map((item) => item.id)) + 1
