import { useEffect } from "react"
import { useParams } from "react-router-dom"
import { useChat } from "@/hooks/useChat"
import ChatWindow from "@/components/chat/ChatWindow"
import MessageInput from "@/components/chat/MessageInput"
import { useToast } from "@/hooks/useToast"

export default function Chat() {
  const { sessionId } = useParams()
  const { messages, isLoading, error, send, loadMessages, setSessionId } =
    useChat(sessionId)
  const { toast } = useToast()

  useEffect(() => {
    if (sessionId) {
      loadMessages(sessionId)
    } else {
      setSessionId(null)
    }
  }, [sessionId, loadMessages, setSessionId])

  useEffect(() => {
    if (error) {
      toast({
        title: "Error",
        description: error,
        variant: "destructive",
      })
    }
  }, [error, toast])

  const handleSend = async (message: string) => {
    try {
      await send(message)
    } catch (err) {
      // Error is handled in useChat and displayed via toast
    }
  }

  return (
    <div className="flex flex-col h-full">
      <ChatWindow messages={messages} isLoading={isLoading} />
      <MessageInput onSend={handleSend} disabled={isLoading} />
    </div>
  )
}