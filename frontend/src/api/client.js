export async function api (path, options = {}){
    const token = localStorage.getItem("token")
    const response = await fetch(`/api${path}`, {
        headers:{
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        },
        ...options
    })
    if (!response.ok) throw new Error((await response.json()).detail || 'Request failed')
    return response.json()
}