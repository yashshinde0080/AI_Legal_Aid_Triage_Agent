"use client";

import { motion, type Variants } from "framer-motion";
import { ArrowUpRight, PlayCircle, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";



interface Metric {
  label: string;
  value: string;
  caption: string;
}

interface ProcessStep {
  label: string;
  progress: number;
}

interface GalleryImage {
  src: string;
  alt: string;
}

interface ReelStat {
  label: string;
}

const keyMetrics: Metric[] = [
  {
    label: "Procedural accuracy",
    value: "99%",
    caption: "Against golden set",
  },
  {
    label: "Response latency",
    value: "<2s",
    caption: "Streamed output",
  },
  {
    label: "Auditability",
    value: "100%",
    caption: "Every step logged",
  },
];

const motionProcess: ProcessStep[] = [
  {
    label: "Intake & Classification",
    progress: 100,
  },
  {
    label: "RAG Retrieval",
    progress: 100,
  },
  {
    label: "Safety Validation",
    progress: 100,
  },
];

const inspirationGallery: GalleryImage[] = [
  {
    src: "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?w=400&h=320&fit=crop&q=80",
    alt: "Collage of lighting references for motion design",
  },
  {
    src: "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400&h=320&fit=crop&q=80",
    alt: "Creative workspace with monitors and sketchbook",
  },
  {
    src: "https://images.unsplash.com/photo-1515169067865-5387ec356754?w=400&h=320&fit=crop&q=80",
    alt: "Colorful motion design storyboard pinned to a wall",
  },
  {
    src: "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=400&h=320&fit=crop&q=80",
    alt: "Designer adjusting camera lighting in a studio",
  },
];

const reelStats: ReelStat[] = [
  { label: "IPC" },
  { label: "Consumer Law" },
  { label: "Labour Laws" },
];

const sectionVariants: Variants = {
  hidden: { opacity: 0, y: 32 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" },
  },
};

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 32 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" },
  },
};

export function BentoGridBlock() {
  return (
    <section className="relative w-full overflow-hidden bg-background">
      <div className="pointer-events-none absolute inset-0 -z-10">
        <div className="absolute left-1/2 top-0 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-foreground/[0.035] blur-[140px]" />
        <div className="absolute bottom-0 right-0 h-[360px] w-[360px] rounded-full bg-primary/[0.035] blur-[120px]" />
        <div className="absolute left-1/4 top-1/2 h-[400px] w-[400px] rounded-full bg-foreground/[0.02] blur-[150px]" />
      </div>

      <div className="relative mx-auto max-w-7xl px-4 py-16 md:px-6 md:py-24">
        <motion.header
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
          className="flex flex-col items-center gap-4 text-center"
        >
          <Badge
            variant="outline"
            className="inline-flex items-center gap-2 rounded-full border-border/50 bg-background/60 px-4 py-1.5 text-xs uppercase tracking-[0.2em] text-foreground/70 backdrop-blur"
          >
            System Capabilities
            <span
              className="h-2 w-2 rounded-full bg-primary"
              aria-hidden="true"
            />
          </Badge>
          <h2 className="text-3xl font-semibold tracking-tight text-foreground md:text-4xl lg:text-5xl">
            Reliable, explainable, and secure legal triage
          </h2>
          <p className="max-w-2xl text-base text-foreground/70 md:text-lg">
            Explore the core components that make this agentic system robust.
            From semantic search to LangGraph state management, every module is designed for accuracy.
          </p>
        </motion.header>

        <motion.div
          className="mt-12 grid auto-rows-[minmax(200px,auto)] gap-4 sm:grid-cols-2 md:gap-6 lg:grid-cols-4"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
          variants={{
            hidden: { opacity: 0, y: 24 },
            visible: {
              opacity: 1,
              y: 0,
              transition: {
                duration: 0.6,
                ease: "easeOut",
                staggerChildren: 0.08,
                delayChildren: 0.12,
              },
            },
          }}
        >
          <motion.article
            variants={cardVariants}
            whileHover={{ y: -4 }}
            transition={{ duration: 0.2 }}
            className="group relative col-span-1 flex h-full flex-col justify-between overflow-hidden rounded-2xl border border-border/40 bg-background/70 p-6 backdrop-blur transition-all hover:border-border/60 hover:shadow-lg sm:col-span-2 lg:row-span-2"
            role="article"
            aria-label="Featured case study"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-foreground/[0.05] via-transparent to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
            <div className="relative flex h-full flex-col justify-between">
              <div className="space-y-4">
                <Badge
                  variant="secondary"
                  className="w-fit rounded-full border-border/40 bg-background/80 px-3 py-1 text-xs uppercase tracking-[0.2em] text-foreground/70"
                >
                  Core Feature
                </Badge>
                <h3 className="text-2xl font-semibold leading-tight text-foreground md:text-3xl">
                  Conversational Intelligence
                </h3>
                <p className="text-sm text-foreground/70 md:text-base">
                  The agent uses LangChain's memory modules to maintain context throughout the entire session.
                  It knows what you said five turns ago, ensuring a natural and efficient triage process.
                </p>
              </div>
              <div className="mt-8 flex items-center justify-between gap-4">
                <Button
                  variant="ghost"
                  className="group/cta gap-2 rounded-lg bg-background/70 px-4 py-2 text-sm text-foreground hover:bg-background/80"
                  aria-label="View architecture"
                >
                  View Architecture
                  <ArrowUpRight className="h-4 w-4 transition-transform group-hover/cta:translate-x-1" />
                </Button>
              </div>
            </div>
          </motion.article>

          <motion.article
            variants={cardVariants}
            whileHover={{ y: -4 }}
            transition={{ duration: 0.2 }}
            className="group col-span-1 flex h-full flex-col rounded-2xl border border-border/40 bg-background/70 p-6 backdrop-blur transition-all hover:border-border/60 hover:shadow-lg sm:col-span-2"
            role="article"
            aria-label="Key performance metrics"
          >
            <div className="flex items-center justify-between">
              <Badge
                variant="secondary"
                className="w-fit rounded-full px-3 py-1 text-xs uppercase tracking-[0.2em] text-primary"
              >
                Performance
              </Badge>
              <motion.div
                animate={{ rotate: [0, -6, 0, 6, 0] }}
                transition={{
                  repeat: Infinity,
                  duration: 10,
                  ease: "easeInOut",
                }}
              >
                <Sparkles className="h-5 w-5 text-primary" aria-hidden="true" />
              </motion.div>
            </div>
            <div className="mt-6 grid gap-4 sm:grid-cols-3">
              {keyMetrics.map((metric) => (
                <div key={metric.label} className="">
                  <p className="text-xs uppercase tracking-[0.18em] text-foreground/60">
                    {metric.label}
                  </p>
                  <p className="mt-2 text-2xl font-semibold tracking-tight text-foreground md:text-3xl">
                    {metric.value}
                  </p>
                  <p className="mt-1 inline-flex items-center gap-2 px-2 py-1 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
                    {metric.caption}
                  </p>
                </div>
              ))}
            </div>
          </motion.article>

          <motion.article
            variants={cardVariants}
            whileHover={{ y: -4 }}
            transition={{ duration: 0.2 }}
            className="group relative col-span-1 overflow-hidden rounded-2xl border border-border/40 bg-background/70 backdrop-blur hover:border-border/60 hover:shadow-lg sm:col-span-2 lg:row-span-3"
            role="article"
            aria-label="Behind the scenes studio imagery"
          >
            <div className="absolute inset-0">
              <img
                src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80"
                alt="Designer workstation lit with cinematic lighting"
                className="h-full w-full object-cover opacity-80"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-background via-background/60 to-transparent" />
            </div>
            <div className="relative flex h-full flex-col justify-end space-y-4 p-6 md:p-8">
              <Badge
                variant="outline"
                className="w-fit rounded-full border-border/60 bg-background/80 px-3 py-1 text-xs uppercase tracking-[0.2em] text-foreground/70"
              >
                RAG Technology
              </Badge>
              <h3 className="text-xl font-semibold tracking-tight text-foreground md:text-2xl">
                Verified Legal Sources via Vector Search
              </h3>
              <p className="max-w-sm text-sm text-foreground/70 md:text-base">
                We leverage pgvector to perform semantic search over a curated database
                of official legal documents. The agent cites the exact section of the law.
              </p>
              <div className="flex flex-wrap gap-2 pt-2">
                {["Embeddings", "Vector DB", "Source Citation"].map(
                  (tag) => (
                    <span
                      key={tag}
                      className="rounded-full border border-border/40 bg-background/70 px-3 py-1 text-xs uppercase tracking-[0.18em] text-foreground/60"
                    >
                      {tag}
                    </span>
                  )
                )}
              </div>
            </div>
          </motion.article>

          <motion.article
            variants={cardVariants}
            whileHover={{ y: -4 }}
            transition={{ duration: 0.2 }}
            className="group col-span-1 flex h-full flex-col rounded-2xl border border-border/40 bg-background/70 p-6 backdrop-blur transition-all hover:border-border/60 hover:shadow-lg sm:col-span-2 lg:row-span-2"
            role="article"
            aria-label="Motion sprint process overview"
          >
            <div className="space-y-4">
              <Badge
                variant="outline"
                className="w-fit rounded-full border-primary/50 bg-background/70 px-3 py-1 text-xs uppercase tracking-[0.2em] text-primary"
              >
                Triage Flow
              </Badge>
              <h3 className="text-xl font-semibold tracking-tight text-foreground md:text-2xl">
                From user input to actionable guidance
              </h3>
              <p className="text-sm text-foreground/70 md:text-base">
                The agent parses your issue, classifies it into a legal domain,
                retrieves relevant procedures, and validates the response for safety.
              </p>
            </div>
            <div className="mt-6 space-y-4">
              {motionProcess.map((step, index) => (
                <div key={step.label} className="space-y-2">
                  <div className="flex items-center justify-between text-xs uppercase tracking-[0.18em] text-foreground/60">
                    <span>{step.label}</span>
                    <span aria-label={`${step.progress}% complete`}>
                      {step.progress}%
                    </span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-foreground/10">
                    <motion.div
                      initial={{ width: 0 }}
                      whileInView={{ width: `${step.progress}%` }}
                      viewport={{ once: true }}
                      transition={{
                        duration: 0.8,
                        ease: "easeOut",
                        delay: index * 0.1,
                      }}
                      className="h-full rounded-full bg-primary"
                    />
                  </div>
                </div>
              ))}
            </div>
            <Button
              variant="ghost"
              className="mt-8 w-fit gap-2 px-0 text-sm text-primary hover:text-primary/90"
              aria-label="Play sprint walkthrough video"
            >
              <PlayCircle className="h-4 w-4" aria-hidden="true" />
              Play walkthrough
            </Button>
          </motion.article>

          <motion.article
            variants={cardVariants}
            whileHover={{ y: -4 }}
            transition={{ duration: 0.2 }}
            className="group col-span-1 flex h-full flex-col overflow-hidden rounded-2xl border border-border/40 bg-gradient-to-br from-primary/15 via-background/70 to-background/90 p-0 backdrop-blur transition-all hover:border-border/60 hover:shadow-lg sm:col-span-2"
            role="article"
            aria-label="Motion showcase video"
          >
            <div className="relative h-full">
              <img
                src="https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=1200&h=600&fit=crop&q=80"
                alt="Motion design workspace with monitors"
                className="absolute inset-0 h-full w-full object-cover opacity-30 transition-opacity duration-500 group-hover:opacity-40"
              />
              <div className="relative flex h-full flex-col justify-between bg-gradient-to-br from-background/90 via-background/70 to-transparent p-6 md:p-8">
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                  <Badge
                      variant="outline"
                      className="w-fit rounded-full border-border/50 bg-background/70 px-3 py-1 text-xs uppercase tracking-[0.2em] text-foreground/70"
                    >
                      Safety Guardrails
                    </Badge>
                    <motion.div
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{
                        repeat: Infinity,
                        duration: 2.4,
                        ease: "easeInOut",
                      }}
                      className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/20"
                    >
                      <PlayCircle
                        className="h-4 w-4 text-primary"
                        aria-hidden="true"
                      />
                    </motion.div>
                  </div>
                  <h3 className="text-xl font-semibold tracking-tight text-foreground md:text-2xl">
                    Strict adherence to procedural guidance
                  </h3>
                  <p className="max-w-md text-sm text-foreground/70 md:text-base">
                    The agent is programmed to never provide legal advice. It strictly
                    refuses requests for predictions, strategy, or lawyer recommendations.
                  </p>
                </div>
                <div className="flex flex-wrap items-center justify-between gap-3 pt-4 text-xs text-foreground/60">
                  <div className="flex flex-wrap gap-2">
                    {reelStats.map((stat) => (
                      <span
                        key={stat.label}
                        className="rounded-full bg-background/80 px-3 py-1 uppercase tracking-[0.18em]"
                      >
                        {stat.label}
                      </span>
                    ))}
                  </div>
                  <Button size="sm" className="gap-2">
                    Watch now
                    <PlayCircle className="h-4 w-4" aria-hidden="true" />
                  </Button>
                </div>
              </div>
            </div>
          </motion.article>

          <motion.article
            variants={cardVariants}
            whileHover={{ y: -4 }}
            transition={{ duration: 0.2 }}
            className="group col-span-1 flex h-full flex-col rounded-2xl border border-border/40 bg-background/70 p-6 backdrop-blur transition-all hover:border-border/60 hover:shadow-lg sm:col-span-2"
            role="article"
            aria-label="Visual research gallery"
          >
            <div className="space-y-3">
              <Badge
                variant="outline"
                className="w-fit rounded-full border-border/50 bg-background/70 px-3 py-1 text-xs uppercase tracking-[0.2em] text-foreground/60"
              >
                Transparent Logging
              </Badge>
              <h3 className="text-lg font-semibold tracking-tight text-foreground md:text-xl">
                Full audit trail of every agent decision
              </h3>
              <p className="text-sm text-foreground/70 md:text-base">
                Every step—from classification to retrieval—is logged in Supabase.
                This ensures accountability and allows for continuous system improvement.
              </p>
            </div>
            <div className="mt-6 grid grid-cols-2 gap-3">
              {inspirationGallery.map((image) => (
                <div
                  key={image.src}
                  className="relative aspect-[4/3] overflow-hidden rounded-xl border border-border/30 bg-background/60"
                >
                  <img
                    src={image.src}
                    alt={image.alt}
                    className="absolute inset-0 h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                </div>
              ))}
            </div>
            <Button
              variant="ghost"
              className="mt-6 w-fit gap-2 px-0 text-sm text-primary hover:text-primary/90"
              aria-label="Open the visual inspiration archive"
            >
              Open inspiration archive
              <ArrowUpRight className="h-4 w-4" aria-hidden="true" />
            </Button>
          </motion.article>
        </motion.div>
      </div>
    </section>
  );
}
