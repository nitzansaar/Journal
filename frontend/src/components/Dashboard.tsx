'use client'

import { useState, useEffect } from 'react'
import { User } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase'
import { journalAPI, JournalEntry } from '@/lib/api'
import JournalEntryForm from './JournalEntryForm'
import JournalEntryList from './JournalEntryList'

interface DashboardProps {
  user: User
}

export default function Dashboard({ user }: DashboardProps) {
  const [entries, setEntries] = useState<JournalEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchEntries = async () => {
    try {
      setLoading(true)
      const data = await journalAPI.getEntries()
      setEntries(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch entries')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEntries()
  }, [])

  const handleSignOut = async () => {
    await supabase.auth.signOut()
  }

  const handleEntryCreated = (newEntry: JournalEntry) => {
    setEntries(prev => [newEntry, ...prev])
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Daily Journal</h1>
          <p className="text-gray-600">Welcome back, {user.email}</p>
        </div>
        <button
          onClick={handleSignOut}
          className="btn btn-secondary"
        >
          Sign Out
        </button>
      </div>

      {/* New Entry Form */}
      <div className="mb-8">
        <JournalEntryForm onEntryCreated={handleEntryCreated} />
      </div>

      {/* Entries List */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Entries</h2>
        
        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded-md mb-4 border border-red-200">
            {error}
          </div>
        )}
        
        {loading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <JournalEntryList entries={entries} />
        )}
      </div>
    </div>
  )
} 