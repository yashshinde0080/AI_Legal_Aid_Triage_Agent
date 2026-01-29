import { Avatar, AvatarFallback } from "../ui/avatar"
import { Scale } from "lucide-react"

export default function TypingIndicator() {
  return (
    <div className="flex gap-3">
      <Avatar className="h-8 w-8 shrink-0">
        <AvatarFallback className="bg-secondary text-secondary-foreground text-xs">
          <Scale className="h-4 w-4" />
        </AvatarFallback>
      </Avatar>

      <div className="bg-muted rounded-lg px-4 py-3">
        <div className="flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-muted-foreground typing-dot" />
          <div className="w-2 h-2 rounded-full bg-muted-foreground typing-dot" />
          <div className="w-2 h-2 rounded-full bg-muted-foreground typing-dot" />
        </div>
      </div>
    </div>
  )
}