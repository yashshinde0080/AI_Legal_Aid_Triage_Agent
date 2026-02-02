import { type SVGProps } from 'react'

export default function Supabase(props: SVGProps<SVGSVGElement>) {
    return (
        <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            {...props}
        >
            <path
                d="M12 2L4 12H12L10 22L20 10H12L12 2Z"
                fill="#3ECF8E"
                stroke="#3ECF8E"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
        </svg>
    )
}
