import { Message } from "@/lib/types"
import { cn } from "@/lib/utils"
import { Avatar, AvatarFallback } from "../ui/avatar"
import { User, Scale, FileText, ExternalLink } from "lucide-react"
import ReactMarkdown from "react-markdown"

interface ChatBubbleProps {
  message: Message
}

export default function ChatBubble({ message }: ChatBubbleProps) {
  const isUser = message.role === "user"
  const sources = message.metadata?.sources || []

  return (
    <div
      className={cn(
        "flex gap-3 message-enter message-enter-active",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      <Avatar className="h-8 w-8 shrink-0">
        <AvatarFallback
          className={cn(
            "text-xs",
            isUser
              ? "bg-primary text-primary-foreground"
              : "bg-secondary text-secondary-foreground"
          )}
        >
          {isUser ? <User className="h-4 w-4" /> : <Scale className="h-4 w-4" />}
        </AvatarFallback>
      </Avatar>

      <div
        className={cn(
          "flex flex-col max-w-[80%]",
          isUser ? "items-end" : "items-start"
        )}
      >
        <div
          className={cn(
            "rounded-lg px-4 py-2",
            isUser
              ? "bg-primary text-primary-foreground"
              : "bg-muted"
          )}
        >
          {isUser ? (
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="prose prose-sm dark:prose-invert max-w-none">
              <ReactMarkdown
                components={{
                  p: ({ children }) => (
                    <p className="mb-2 last:mb-0">{children}</p>
                  ),
                  ul: ({ children }) => (
                    <ul className="list-disc ml-4 mb-2">{children}</ul>
                  ),
                  ol: ({ children }) => (
                    <ol className="list-decimal ml-4 mb-2">{children}</ol>
                  ),
                  li: ({ children }) => <li className="mb-1">{children}</li>,
                  strong: ({ children }) => (
                    <strong className="font-semibold">{children}</strong>
                  ),
                  h1: ({ children }) => (
                    <h3 className="text-base font-semibold mt-3 mb-2">
                      {children}
                    </h3>
                  ),
                  h2: ({ children }) => (
                    <h4 className="text-sm font-semibold mt-2 mb-1">
                      {children}
                    </h4>
                  ),
                  h3: ({ children }) => (
                    <h5 className="text-sm font-medium mt-2 mb-1">
                      {children}
                    </h5>
                  ),
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-2 border-primary pl-3 italic my-2">
                      {children}
                    </blockquote>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          )}
        </div>

        {/* Classification badge */}
        {message.metadata?.classification && (
          <div className="mt-1 flex items-center gap-2">
            <span className="text-xs px-2 py-0.5 rounded-full bg-primary/10 text-primary">
              {message.metadata.classification}
            </span>
            {message.metadata.confidence !== undefined && (
              <span className="text-xs text-muted-foreground">
                {Math.round(message.metadata.confidence * 100)}% confidence
              </span>
            )}
          </div>
        )}

        {/* Sources */}
        {sources.length > 0 && (
          <div className="mt-2 space-y-1">
            <p className="text-xs text-muted-foreground flex items-center gap-1">
              <FileText className="h-3 w-3" />
              Sources:
            </p>
            {sources.map((source, index) => (
              <div
                key={index}
                className="text-xs p-2 rounded bg-background border"
              >
                <p className="font-medium">{source.title}</p>
                {source.section && (
                  <p className="text-muted-foreground">
                    Section: {source.section}
                  </p>
                )}
                {source.source_url && (
                  <a
                    href={source.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:underline inline-flex items-center gap-1 mt-1"
                  >
                    View source
                    <ExternalLink className="h-3 w-3" />
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}