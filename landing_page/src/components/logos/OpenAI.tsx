import { type SVGProps } from 'react'

export default function OpenAI(props: SVGProps<SVGSVGElement>) {
    return (
        <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            {...props}
        >
             <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" />
             <path d="M12 2V12L20 8" stroke="currentColor" strokeWidth="2" />
             <path d="M12 22V12L4 16" stroke="currentColor" strokeWidth="2" />
             <path d="M4 8L12 12" stroke="currentColor" strokeWidth="2" />
             <path d="M20 16L12 12" stroke="currentColor" strokeWidth="2" />
        </svg>
    )
}
