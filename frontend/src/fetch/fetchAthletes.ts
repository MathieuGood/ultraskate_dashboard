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

export interface AthletePerformance {
    event_name: string
    year: number
    date: string
    sport: string
    category: string
    total_laps: number
    total_miles: number
    total_km: number
    average_speed_mph: number
    average_speed_kph: number
    total_time_hhmmss: string
}

export interface AthleteProfile {
    name: string
    gender: string
    city: string
    state: string
    country: string
    team: boolean
    event_count: number
    total_miles: number
    total_km: number
    performances: AthletePerformance[]
}

export const fetchAllAthletes = async (): Promise<AthleteStats[]> => {
    const response = await fetch(`${API_URL}${ATHLETES_ENDPOINT}/`)
    return response.json()
}

export const fetchAthleteByName = async (name: string): Promise<AthleteProfile> => {
    const response = await fetch(`${API_URL}${ATHLETES_ENDPOINT}/${encodeURIComponent(name)}`)
    return response.json()
}
