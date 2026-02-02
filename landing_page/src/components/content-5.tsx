import { Cpu, Lock, Sparkles, Zap } from 'lucide-react'

export default function ContentSection() {
    return (
        <section className="py-16 md:py-32">
            <div className="mx-auto max-w-5xl space-y-8 px-6 md:space-y-12">
                <div className="mx-auto max-w-xl space-y-6 text-center md:space-y-12">
                    <h2 className="text-balance text-4xl font-medium lg:text-5xl">Why Most AI Legal Bots Fail</h2>
                    <p>Standard chatbots hallucinate, forget context, and lack safety. We built a system to solve access-to-justice, not just a demo.</p>
                </div>
                <img className="rounded-(--radius) grayscale" src="https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=2940&auto=format&fit=crop" alt="Legal Justice" loading="lazy" />

                <div className="relative mx-auto grid grid-cols-2 gap-x-3 gap-y-6 sm:gap-8 lg:grid-cols-4">
                    <div className="space-y-3">
                        <div className="flex items-center gap-2">
                            <Zap className="size-4" />
                            <h3 className="text-sm font-medium">Context Aware</h3>
                        </div>
                        <p className="text-muted-foreground text-sm">Maintains full conversation history, unlike stateless chatbots.</p>
                    </div>
                    <div className="space-y-2">
                        <div className="flex items-center gap-2">
                            <Cpu className="size-4" />
                            <h3 className="text-sm font-medium">Deterministic</h3>
                        </div>
                        <p className="text-muted-foreground text-sm">Follows a strict LangGraph state machine, not random token generation.</p>
                    </div>
                    <div className="space-y-2">
                        <div className="flex items-center gap-2">
                            <Lock className="size-4" />
                            <h3 className="text-sm font-medium">Verified Sources</h3>
                        </div>
                        <p className="text-muted-foreground text-sm">Uses RAG to cite specific laws, never internet blogs.</p>
                    </div>
                    <div className="space-y-2">
                        <div className="flex items-center gap-2">
                            <Sparkles className="size-4" />

                            <h3 className="text-sm font-medium">Auditable</h3>
                        </div>
                        <p className="text-muted-foreground text-sm">Every decision and retrieval is logged for human review.</p>
                    </div>
                </div>
            </div>
        </section>
    )
}
