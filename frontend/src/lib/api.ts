import { supabase } from "./supabase"

const API_BASE_URL = import.meta.env.VITE_API_URL || ""

interface ChatRequest {
  message: string
  session_id?: string
  llm_provider?: string
}

interface ChatResponse {
  response: string
  session_id: string
  classification: string | null
  sub_classification: string | null
  confidence: number
  needs_clarification: boolean
  sources: Array<{
    title: string
    section: string
    content: string
    source_url?: string
  }>
  disclaimer: string
}

interface Session {
  id: string
  title: string
  created_at: string
  updated_at: string
  message_count: number
  last_message?: string
}

interface Message {
  id: string
  role: "user" | "assistant" | "system"
  content: string
  created_at: string
  metadata?: Record<string, unknown>
}

async function getAuthHeaders(): Promise<HeadersInit> {
  const { data } = await supabase.auth.getSession()
  const token = data.session?.access_token

  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const headers = await getAuthHeaders()

  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers,
    body: JSON.stringify(request),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }))
    throw new Error(error.detail || "Failed to send message")
  }

  return response.json()
}

export async function getSessions(): Promise<Session[]> {
  const headers = await getAuthHeaders()

  const response = await fetch(`${API_BASE_URL}/api/sessions`, {
    method: "GET",
    headers,
  })

  if (!response.ok) {
    throw new Error("Failed to fetch sessions")
  }

  return response.json()
}

export async function getSession(sessionId: string): Promise<Session> {
  const headers = await getAuthHeaders()

  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`, {
    method: "GET",
    headers,
  })

  if (!response.ok) {
    throw new Error("Failed to fetch session")
  }

  return response.json()
}

export async function getSessionMessages(
  sessionId: string,
  limit = 50
): Promise<Message[]> {
  const headers = await getAuthHeaders()

  const response = await fetch(
    `${API_BASE_URL}/api/sessions/${sessionId}/messages?limit=${limit}`,
    {
      method: "GET",
      headers,
    }
  )

  if (!response.ok) {
    throw new Error("Failed to fetch messages")
  }

  return response.json()
}

export async function updateSession(
  sessionId: string,
  title: string
): Promise<Session> {
  const headers = await getAuthHeaders()

  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`, {
    method: "PUT",
    headers,
    body: JSON.stringify({ title }),
  })

  if (!response.ok) {
    throw new Error("Failed to update session")
  }

  return response.json()
}

export async function deleteSession(sessionId: string): Promise<void> {
  const headers = await getAuthHeaders()

  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`, {
    method: "DELETE",
    headers,
  })

  if (!response.ok) {
    throw new Error("Failed to delete session")
  }
}

export async function checkHealth(): Promise<{
  status: string
  version: string
}> {
  const response = await fetch(`${API_BASE_URL}/health`)
  return response.json()
}