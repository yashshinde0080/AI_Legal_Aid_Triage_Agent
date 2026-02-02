'use client'

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Clock, CreditCard, Truck, Globe, Package, type LucideIcon } from 'lucide-react'

type FAQItem = {
    id: string
    icon: LucideIcon
    question: string
    answer: string
}

export default function FAQsThree() {
    const faqItems: FAQItem[] = [
        {
            id: 'item-1',
            icon: Clock,
            question: 'Is this just a chatbot?',
            answer: 'No. This is a stateful, agentic triage system. Unlike a chatbot, it maintains persistent memory of the conversation, classifies legal issues into specific domains, and follows a strict determinisic procedural graph to ensure accuracy.',
        },
        {
            id: 'item-2',
            icon: CreditCard,
            question: 'Does it provide legal advice?',
            answer: 'No. The system provides "Procedural Guidance" only. It retrieves verified laws to explain "how" to proceed (e.g., "File Form X at Court Y"), but never advises "what" to do strategically. It includes strict guardrails to prevent unauthorized advice.',
        },
        {
            id: 'item-3',
            icon: Truck,
            question: 'Where does the legal data come from?',
            answer: 'The system uses RAG (Retrieval Augmented Generation) over a verified index of official legal documents (e.g., Consumer Protection Act, IPC). It cites specific sections and never hallucinates laws from the internet.',
        },
        {
            id: 'item-4',
            icon: Globe,
            question: 'Is user data secure?',
            answer: 'Yes. All sessions are authenticated via Supabase. Conversation history is stored in a structured Postgres database with Row Level Security (RLS), ensuring that only the user can access their case history.',
        },
        {
            id: 'item-5',
            icon: Package,
            question: 'How is it auditable?',
            answer: 'Every step the agent takes—classification, retrieval, and response generation—is logged. This creates a transparent audit trail, allowing human reviewers to verify why the agent gave a specific piece of guidance.',
        },
    ]

    return (
        <section className="bg-muted dark:bg-background py-20">
            <div className="mx-auto max-w-5xl px-4 md:px-6">
                <div className="flex flex-col gap-10 md:flex-row md:gap-16">
                    <div className="md:w-1/3">
                        <div className="sticky top-20">
                            <h2 className="mt-4 text-3xl font-bold">Frequently Asked Questions</h2>
                            <p className="text-muted-foreground mt-4">
                                Can't find what you're looking for? Contact our{' '}
                                <a
                                    href="#"
                                    className="text-primary font-medium hover:underline">
                                    customer support team
                                </a>
                            </p>
                        </div>
                    </div>
                    <div className="md:w-2/3">
                        <Accordion
                            type="single"
                            collapsible
                            className="w-full space-y-2">
                            {faqItems.map((item) => (
                                <AccordionItem
                                    key={item.id}
                                    value={item.id}
                                    className="bg-background shadow-xs rounded-lg border px-4 last:border-b">
                                    <AccordionTrigger className="cursor-pointer items-center py-5 hover:no-underline">
                                        <div className="flex items-center gap-3">
                                            <div className="flex size-6">
                                                <item.icon
                                                    className="m-auto size-4"
                                                />
                                            </div>
                                            <span className="text-base">{item.question}</span>
                                        </div>
                                    </AccordionTrigger>
                                    <AccordionContent className="pb-5">
                                        <div className="px-9">
                                            <p className="text-base">{item.answer}</p>
                                        </div>
                                    </AccordionContent>
                                </AccordionItem>
                            ))}
                        </Accordion>
                    </div>
                </div>
            </div>
        </section>
    )
}
