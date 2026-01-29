export interface User {
  id: string
  email: string
  full_name?: string
}

export interface Session {
  id: string
  title: string
  created_at: string
  updated_at: string
  message_count: number
  last_message?: string
}

export interface Message {
  id: string
  role: "user" | "assistant" | "system"
  content: string
  created_at: string
  metadata?: MessageMetadata
}

export interface MessageMetadata {
  classification?: string
  confidence?: number
  sources?: Source[]
}

export interface Source {
  title: string
  section: string
  content: string
  source_url?: string
}

export interface ChatState {
  messages: Message[]
  isLoading: boolean
  error: string | null
  sessionId: string | null
}

export interface Classification {
  domain: string
  sub_domain: string
  confidence: number
}