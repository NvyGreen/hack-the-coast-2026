export async function fetchDashboard() {
  const res = await fetch('/api/dashboard')
  if (!res.ok) throw new Error(`Dashboard fetch failed: ${res.status}`)
  return res.json()
}

export async function fetchBrowse() {
  const res = await fetch('/api/browse')
  if (!res.ok) throw new Error(`Browse fetch failed: ${res.status}`)
  return res.json()
}
