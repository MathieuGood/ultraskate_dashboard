const API_URL = 'http://localhost:8000/'
const ATHLETES_ENDPOINT = 'athletes'

export interface AthleteStats {
    name: string
    gender: string
    city: string
    state: string
    country: string
    team: boolean
    event_count: number
    total_miles: number
    best_event_miles: number
    sports: string[]
}

export const fetchAllAthletes = async (): Promise<AthleteStats[]> => {
    const response = await fetch(`${API_URL}${ATHLETES_ENDPOINT}`)
    return response.json()
}
