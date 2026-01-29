import { Session } from "@/lib/types"
import { ScrollArea } from "../ui/scroll-area"
import { Button } from "../ui/button"
import { formatDate, cn } from "@/lib/utils"
import { MessageSquare, Trash2, Pencil } from "lucide-react"
import { useState } from "react"
import { Input } from "../ui/input"

interface SessionListProps {
  sessions: Session[]
  loading: boolean
  currentSessionId?: string
  onSelect: (id: string) => void
  onDelete: (id: string) => void
  onRename: (id: string, title: string) => void
}

export default function SessionList({
  sessions,
  loading,
  currentSessionId,
  onSelect,
  onDelete,
  onRename,
}: SessionListProps) {
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState("")

  const handleStartEdit = (session: Session) => {
    setEditingId(session.id)
    setEditTitle(session.title)
  }

  const handleSaveEdit = (id: string) => {
    if (editTitle.trim()) {
      onRename(id, editTitle.trim())
    }
    setEditingId(null)
  }

  const handleCancelEdit = () => {
    setEditingId(null)
    setEditTitle("")
  }

  if (loading) {
    return (
      <div className="p-4 space-y-2">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className="h-12 bg-muted animate-pulse rounded-md"
          />
        ))}
      </div>
    )
  }

  if (sessions.length === 0) {
    return (
      <div className="p-4 text-center text-muted-foreground">
        <MessageSquare className="h-8 w-8 mx-auto mb-2 opacity-50" />
        <p className="text-sm">No conversations yet</p>
        <p className="text-xs">Start a new chat to get help</p>
      </div>
    )
  }

  return (
    <ScrollArea className="h-full">
      <div className="p-2 space-y-1">
        {sessions.map((session) => (
          <div
            key={session.id}
            className={cn(
              "group flex items-center gap-2 rounded-md p-2 hover:bg-accent cursor-pointer",
              currentSessionId === session.id && "bg-accent"
            )}
            onClick={() => onSelect(session.id)}
          >
            <MessageSquare className="h-4 w-4 shrink-0 text-muted-foreground" />
            
            <div className="flex-1 min-w-0">
              {editingId === session.id ? (
                <Input
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  onBlur={() => handleSaveEdit(session.id)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") handleSaveEdit(session.id)
                    if (e.key === "Escape") handleCancelEdit()
                  }}
                  className="h-6 text-sm"
                  autoFocus
                  onClick={(e) => e.stopPropagation()}
                />
              ) : (
                <>
                  <p className="text-sm font-medium truncate">
                    {session.title}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {formatDate(session.updated_at)}
                  </p>
                </>
              )}
            </div>

            <div className="hidden group-hover:flex items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                className="h-6 w-6"
                onClick={(e) => {
                  e.stopPropagation()
                  handleStartEdit(session)
                }}
              >
                <Pencil className="h-3 w-3" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-6 w-6 text-destructive hover:text-destructive"
                onClick={(e) => {
                  e.stopPropagation()
                  onDelete(session.id)
                }}
              >
                <Trash2 className="h-3 w-3" />
              </Button>
            </div>
          </div>
        ))}
      </div>
    </ScrollArea>
  )
}