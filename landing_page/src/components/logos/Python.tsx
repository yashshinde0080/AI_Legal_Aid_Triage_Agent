import { type SVGProps } from 'react'

export default function Python(props: SVGProps<SVGSVGElement>) {
    return (
        <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            {...props}
        >
            <path
                d="M12 2C8 2 8 4 8 4H12V6H6V12H4C4 12 2 12 2 8C2 4 4 2 8 2ZM12 22C16 22 16 20 16 20H12V18H18V12H20C20 12 22 12 22 16C22 20 20 22 16 22Z"
                fill="#3776AB"
            />
            <path
                d="M10 8H14V14H10V8Z"
                fill="#FFD343"
            />
        </svg>
    )
}
