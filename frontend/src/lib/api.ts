import axios from 'axios'
import { supabase } from './supabase'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface JournalEntry {
  id: string
  created_at: string
  content: string
}

export interface CreateJournalEntry {
  content: string
}

// Create axios instance with interceptor for auth
const apiClient = axios.create({
  baseURL: API_URL,
})

// Add auth token to requests
apiClient.interceptors.request.use(async (config) => {
  const { data: { session } } = await supabase.auth.getSession()
  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`
  }
  return config
})

export const journalAPI = {
  async createEntry(entry: CreateJournalEntry): Promise<JournalEntry> {
    const response = await apiClient.post('/entries', entry)
    return response.data
  },

  async getEntries(): Promise<JournalEntry[]> {
    const response = await apiClient.get('/entries')
    return response.data
  },
} 