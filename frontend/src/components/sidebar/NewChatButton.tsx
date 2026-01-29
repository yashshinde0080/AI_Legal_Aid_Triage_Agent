import { Button } from "../ui/button"
import { Plus } from "lucide-react"

interface NewChatButtonProps {
  onClick: () => void
}

export default function NewChatButton({ onClick }: NewChatButtonProps) {
  return (
    <Button
      onClick={onClick}
      className="w-full justify-start gap-2"
      variant="outline"
    >
      <Plus className="h-4 w-4" />
      New Chat
    </Button>
  )
}