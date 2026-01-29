import { ReactNode, useState } from "react"
import Header from "./Header"
import SessionList from "../sidebar/SessionList"
import NewChatButton from "../sidebar/NewChatButton"
import { useSession } from "@/hooks/useSession"
import { useNavigate, useParams } from "react-router-dom"
import { cn } from "@/lib/utils"
import { Menu, X } from "lucide-react"
import { Button } from "../ui/button"

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { sessions, loading, removeSession, renameSession } = useSession()
  const navigate = useNavigate()
  const { sessionId } = useParams()

  const handleNewChat = () => {
    navigate("/")
    setSidebarOpen(false)
  }

  const handleSelectSession = (id: string) => {
    navigate(`/chat/${id}`)
    setSidebarOpen(false)
  }

  const handleDeleteSession = async (id: string) => {
    await removeSession(id)
    if (sessionId === id) {
      navigate("/")
    }
  }

  return (
    <div className="flex h-screen bg-background">
      {/* Mobile sidebar toggle */}
      <Button
        variant="ghost"
        size="icon"
        className="fixed top-4 left-4 z-50 md:hidden"
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
      </Button>

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 w-64 transform bg-muted/50 border-r transition-transform duration-200 ease-in-out md:relative md:translate-x-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex flex-col h-full">
          <div className="p-4 border-b">
            <h1 className="text-lg font-semibold">Legal Aid</h1>
            <p className="text-xs text-muted-foreground">AI Triage Assistant</p>
          </div>

          <div className="p-3">
            <NewChatButton onClick={handleNewChat} />
          </div>

          <div className="flex-1 overflow-hidden">
            <SessionList
              sessions={sessions}
              loading={loading}
              currentSessionId={sessionId}
              onSelect={handleSelectSession}
              onDelete={handleDeleteSession}
              onRename={renameSession}
            />
          </div>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <div className="flex-1 overflow-hidden">{children}</div>
      </main>
    </div>
  )
}