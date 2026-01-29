import { useEffect, useRef } from "react"
import { Message } from "@/lib/types"
import ChatBubble from "./ChatBubble"
import TypingIndicator from "./TypingIndicator"
import { ScrollArea } from "../ui/scroll-area"
import { Scale } from "lucide-react"

interface ChatWindowProps {
  messages: Message[]
  isLoading: boolean
}

export default function ChatWindow({ messages, isLoading }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, isLoading])

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="mx-auto w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
            <Scale className="h-8 w-8 text-primary" />
          </div>
          <h2 className="text-xl font-semibold mb-2">
            AI Legal Aid Assistant
          </h2>
          <p className="text-muted-foreground text-sm mb-6">
            I can help you understand legal procedures in India. Describe your
            situation, and I'll guide you through the relevant steps.
          </p>
          <div className="grid gap-2 text-left text-sm">
            <div className="p-3 rounded-lg bg-muted">
              💼 "I bought a phone online and it's defective. What can I do?"
            </div>
            <div className="p-3 rounded-lg bg-muted">
              🏠 "My landlord is not returning my security deposit."
            </div>
            <div className="p-3 rounded-lg bg-muted">
              💰 "My employer hasn't paid my salary for 3 months."
            </div>
          </div>
          <p className="text-xs text-muted-foreground mt-6">
            ⚠️ This provides procedural guidance only, not legal advice.
          </p>
        </div>
      </div>
    )
  }

  return (
    <ScrollArea className="flex-1">
      <div className="max-w-3xl mx-auto p-4 space-y-4">
        {messages.map((message) => (
          <ChatBubble key={message.id} message={message} />
        ))}
        
        {isLoading && <TypingIndicator />}
        
        <div ref={bottomRef} />
      </div>
    </ScrollArea>
  )
}