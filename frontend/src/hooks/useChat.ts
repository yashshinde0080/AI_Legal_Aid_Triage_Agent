import { useState, useCallback } from "react"
import { sendMessage, getSessionMessages } from "@/lib/api"
import { Message, ChatState } from "@/lib/types"
import { generateId } from "@/lib/utils"

export function useChat(initialSessionId?: string) {
  const [state, setState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    error: null,
    sessionId: initialSessionId || null,
  })

  const loadMessages = useCallback(async (sessionId: string) => {
    try {
      setState((prev) => ({ ...prev, isLoading: true, error: null }))
      const messages = await getSessionMessages(sessionId)
      setState((prev) => ({
        ...prev,
        messages,
        sessionId,
        isLoading: false,
      }))
    } catch (error) {
      setState((prev) => ({
        ...prev,
        error: error instanceof Error ? error.message : "Failed to load messages",
        isLoading: false,
      }))
    }
  }, [])

  const send = useCallback(
    async (content: string) => {
      // Add user message immediately for optimistic UI
      const userMessage: Message = {
        id: generateId(),
        role: "user",
        content,
        created_at: new Date().toISOString(),
      }

            setState((prev) => ({
        ...prev,
        messages: [...prev.messages, userMessage],
        isLoading: true,
        error: null,
      }))

      try {
        const response = await sendMessage({
          message: content,
          session_id: state.sessionId || undefined,
        })

        // Add assistant message
        const assistantMessage: Message = {
          id: generateId(),
          role: "assistant",
          content: response.response,
          created_at: new Date().toISOString(),
          metadata: {
            classification: response.classification || undefined,
            confidence: response.confidence,
            sources: response.sources,
          },
        }

        setState((prev) => ({
          ...prev,
          messages: [...prev.messages, assistantMessage],
          sessionId: response.session_id,
          isLoading: false,
        }))

        return response
      } catch (error) {
        setState((prev) => ({
          ...prev,
          error: error instanceof Error ? error.message : "Failed to send message",
          isLoading: false,
        }))
        throw error
      }
    },
    [state.sessionId]
  )

  const clearMessages = useCallback(() => {
    setState({
      messages: [],
      isLoading: false,
      error: null,
      sessionId: null,
    })
  }, [])

  const setSessionId = useCallback((sessionId: string | null) => {
    setState((prev) => ({ ...prev, sessionId }))
  }, [])

  return {
    messages: state.messages,
    isLoading: state.isLoading,
    error: state.error,
    sessionId: state.sessionId,
    send,
    loadMessages,
    clearMessages,
    setSessionId,
  }
}