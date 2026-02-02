import { type SVGProps } from 'react'

export default function HuggingFace(props: SVGProps<SVGSVGElement>) {
    return (
        <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            {...props}
        >
            <path
                d="M12 2L4 7V17L12 22L20 17V7L12 2Z"
                stroke="#FFD21E"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            <path d="M9 10H10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            <path d="M14 10H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            <path d="M9 15C9 15 10 17 12 17C14 17 15 15 15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
    )
}
