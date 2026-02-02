import { Scale } from 'lucide-react'
import { cn } from '@/lib/utils'

export const Logo = ({ className }: { className?: string; uniColor?: boolean }) => {
    return (
        <div className={cn("flex items-center gap-2", className)}>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
                <Scale className="h-5 w-5 text-primary" />
            </div>
            <span className="text-lg font-bold tracking-tight text-foreground">
                AI Legal Aid
            </span>
        </div>
    )
}

export const LogoIcon = ({ className }: { className?: string; uniColor?: boolean }) => {
    return (
        <div className={cn("flex items-center justify-center", className)}>
            <Scale className="h-6 w-6 text-primary" />
        </div>
    )
}

export const LogoStroke = ({ className }: { className?: string }) => {
    return (
        <div className={cn("flex items-center justify-center", className)}>
            <Scale className="h-8 w-8 text-muted-foreground/20" />
        </div>
    )
}
