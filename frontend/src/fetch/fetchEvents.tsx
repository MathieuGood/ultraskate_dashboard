const API_URL = 'http://localhost:8000/'
const EVENTS_ENDPOINT = 'events'

export const fetchAllEvents = async () => {
  const response = await fetch(`${API_URL}${EVENTS_ENDPOINT}`)
  return response.json()
}

export const fetchEventByYear = async (year: number) => {
    const response = await fetch(`${API_URL}${EVENTS_ENDPOINT}/${year}`)
    return response.json()
}

export const fetchEventByNameYear = async (name: string, year: string) => {
    const response = await fetch(`${API_URL}${EVENTS_ENDPOINT}/${name}/${year}`)
    return response.json()
}

export const fetchEventGraphData = async (name: string, year: string) => {
    const response = await fetch(`${API_URL}${EVENTS_ENDPOINT}/${name}/${year}/graph`)
    return response.json()
}
