'use client'
import { LogoIcon } from '@/components/logo'
import { Activity, Map as MapIcon, MessageCircle } from 'lucide-react'
import DottedMap from 'dotted-map'
import { Area, AreaChart, CartesianGrid } from 'recharts'
import { type ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from '@/components/ui/chart'

export default function FeaturesSection() {
    return (
        <section className="px-4 py-16 md:py-32">
            <div className="mx-auto grid max-w-5xl border md:grid-cols-2">
                <div>
                    <div className="p-6 sm:p-12">
                        <span className="text-muted-foreground flex items-center gap-2">
                            <MapIcon className="size-4" />
                            Stateful Conversation Memory
                        </span>

                        <p className="mt-8 text-2xl font-semibold">Remembers context across the entire session. No more repeating facts.</p>
                    </div>

                    <div
                        aria-hidden
                        className="relative">
                        <div className="absolute inset-0 z-10 m-auto size-fit">
                            <div className="rounded-(--radius) bg-background z-1 dark:bg-muted relative flex size-fit w-fit items-center gap-2 border px-3 py-1 text-xs font-medium shadow-md shadow-zinc-950/5">
                                <span className="text-lg">⚖️</span> Jurisdiction: Civil Law
                            </div>
                            <div className="rounded-(--radius) bg-background absolute inset-2 -bottom-2 mx-auto border px-3 py-4 text-xs font-medium shadow-md shadow-zinc-950/5 dark:bg-zinc-900"></div>
                        </div>

                        <div className="relative overflow-hidden">
                            <div className="bg-radial z-1 to-background absolute inset-0 from-transparent to-75%"></div>
                            <Map />
                        </div>
                    </div>
                </div>
                <div className="overflow-hidden border-t bg-zinc-50 p-6 sm:p-12 md:border-0 md:border-l dark:bg-transparent">
                    <div className="relative z-10">
                        <span className="text-muted-foreground flex items-center gap-2">
                            <MessageCircle className="size-4" />
                            AI Issue Classification
                        </span>

                        <p className="my-8 text-2xl font-semibold">Deep analysis of user queries to identify specific legal domains.</p>
                    </div>
                    <div
                        aria-hidden
                        className="flex flex-col gap-8">
                        <div>
                            <div className="flex items-center gap-2">
                                <span className="flex size-5 rounded-full border">
                                    <LogoIcon className="m-auto size-3 [&>svg]:!size-full" />
                                </span>
                                <span className="text-muted-foreground text-xs">System</span>
                            </div>
                            <div className="rounded-(--radius) bg-background mt-1.5 w-3/5 border p-3 text-xs">Which state did the purchase occur in?</div>
                        </div>

                        <div>
                            <div className="rounded-(--radius) mb-1 ml-auto w-3/5 bg-blue-600 p-3 text-xs text-white">Maharashtra, last Tuesday.</div>
                            <span className="text-muted-foreground block text-right text-xs">User</span>
                        </div>
                    </div>
                </div>
                <div className="col-span-full border-y p-12">
                    <p className="text-center text-4xl font-semibold lg:text-7xl">100% Auditable Log</p>
                </div>
                <div className="relative col-span-full">
                    <div className="absolute z-10 max-w-lg px-6 pr-12 pt-6 md:px-12 md:pt-12">
                        <span className="text-muted-foreground flex items-center gap-2">
                            <Activity className="size-4" />
                            Guardrails & Safety
                        </span>

                        <p className="my-8 text-2xl font-semibold">
                            Strict safety checks on every output. <span className="text-muted-foreground"> Procedural guidance only, no legal advice.</span>
                        </p>
                    </div>
                    <MonitoringChart />
                </div>
            </div>
        </section>
    )
}

const map = new DottedMap({ height: 55, grid: 'diagonal' })

const points = map.getPoints()

const svgOptions = {
    backgroundColor: 'var(--color-background)',
    color: 'currentColor',
    radius: 0.15,
}

const Map = () => {
    const viewBox = `0 0 120 60`
    return (
        <svg
            viewBox={viewBox}
            style={{ background: svgOptions.backgroundColor }}>
            {points.map((point, index) => (
                <circle
                    key={index}
                    cx={point.x}
                    cy={point.y}
                    r={svgOptions.radius}
                    fill={svgOptions.color}
                />
            ))}
        </svg>
    )
}

const chartConfig = {
    events: {
        label: 'Logged Events',
        color: '#2563eb',
    },
    alerts: {
        label: 'Safety Alerts',
        color: '#60a5fa',
    },
} satisfies ChartConfig

const chartData = [
    { month: 'May', events: 56, alerts: 24 },
    { month: 'June', events: 120, alerts: 45 },
    { month: 'January', events: 250, alerts: 80 },
    { month: 'February', events: 400, alerts: 120 },
    { month: 'March', events: 200, alerts: 50 },
    { month: 'April', events: 600, alerts: 100 },
]

const MonitoringChart = () => {
    return (
        <ChartContainer
            className="h-120 aspect-auto md:h-96"
            config={chartConfig}>
            <AreaChart
                accessibilityLayer
                data={chartData}
                margin={{
                    left: 0,
                    right: 0,
                }}>
                <defs>
                    <linearGradient
                        id="fillEvents"
                        x1="0"
                        y1="0"
                        x2="0"
                        y2="1">
                        <stop
                            offset="0%"
                            stopColor="var(--color-events)"
                            stopOpacity={0.8}
                        />
                        <stop
                            offset="55%"
                            stopColor="var(--color-events)"
                            stopOpacity={0.1}
                        />
                    </linearGradient>
                    <linearGradient
                        id="fillAlerts"
                        x1="0"
                        y1="0"
                        x2="0"
                        y2="1">
                        <stop
                            offset="0%"
                            stopColor="var(--color-alerts)"
                            stopOpacity={0.8}
                        />
                        <stop
                            offset="55%"
                            stopColor="var(--color-alerts)"
                            stopOpacity={0.1}
                        />
                    </linearGradient>
                </defs>
                <CartesianGrid vertical={false} />
                <ChartTooltip
                    active
                    cursor={false}
                    content={<ChartTooltipContent className="dark:bg-muted" />}
                />
                <Area
                    strokeWidth={2}
                    dataKey="alerts"
                    type="stepBefore"
                    fill="url(#fillAlerts)"
                    fillOpacity={0.1}
                    stroke="var(--color-alerts)"
                    stackId="a"
                />
                <Area
                    strokeWidth={2}
                    dataKey="events"
                    type="stepBefore"
                    fill="url(#fillEvents)"
                    fillOpacity={0.1}
                    stroke="var(--color-events)"
                    stackId="a"
                />
            </AreaChart>
        </ChartContainer>
    )
}
