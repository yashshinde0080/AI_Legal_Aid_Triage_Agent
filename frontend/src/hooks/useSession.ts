import { useState, useEffect, useCallback } from "react"
import { getSessions, deleteSession, updateSession } from "@/lib/api"
import { Session } from "@/lib/types"

export function useSession() {
  const [sessions, setSessions] = useState<Session[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchSessions = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getSessions()
      setSessions(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch sessions")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchSessions()
  }, [fetchSessions])

  const removeSession = useCallback(async (sessionId: string) => {
    try {
      await deleteSession(sessionId)
      setSessions((prev) => prev.filter((s) => s.id !== sessionId))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete session")
      throw err
    }
  }, [])

  const renameSession = useCallback(
    async (sessionId: string, title: string) => {
      try {
        await updateSession(sessionId, title)
        setSessions((prev) =>
          prev.map((s) => (s.id === sessionId ? { ...s, title } : s))
        )
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to update session")
        throw err
      }
    },
    []
  )

  const addSession = useCallback((session: Session) => {
    setSessions((prev) => [session, ...prev])
  }, [])

  return {
    sessions,
    loading,
    error,
    fetchSessions,
    removeSession,
    renameSession,
    addSession,
  }
}