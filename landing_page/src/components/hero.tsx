import { useEffect } from "react";
import { ArrowUpRight, CirclePlay } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export default function Hero() {
  useEffect(() => {
    // Initialize Unicorn Studio
    const loadUnicorn = () => {
      const script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v2.0.4/dist/unicornStudio.umd.js";
      script.onload = () => {
        // @ts-ignore
        if (window.UnicornStudio) {
           // @ts-ignore
          window.UnicornStudio.init();
        }
      };
      document.body.appendChild(script);
    };

    // @ts-ignore
    if (!window.UnicornStudio) {
      loadUnicorn();
    } else {
      // @ts-ignore
      window.UnicornStudio.init();
    }
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center overflow-hidden">
      <div className="mx-auto grid w-full max-w-(--breakpoint-xl) gap-12 px-6 py-12 lg:grid-cols-2 lg:py-0">
        <div className="my-auto">
          <Badge
            asChild
            className="rounded-full border-border py-1"
            variant="secondary"
          >
            <a href="#">
              Just released v1.0.0 <ArrowUpRight className="ml-1 size-4" />
            </a>
          </Badge>
          <h1 className="mt-6 max-w-[17ch] font-semibold text-4xl leading-[1.2]! tracking-[-0.035em] md:text-5xl lg:text-[2.75rem] xl:text-[3.25rem]">
            Customized Shadcn UI Blocks & Components
          </h1>
          <p className="mt-6 max-w-[60ch] text-foreground/80 text-lg">
            Explore a collection of Shadcn UI blocks and components, ready to
            preview and copy. Streamline your development workflow with
            easy-to-implement examples.
          </p>
          <div className="mt-12 flex items-center gap-4">
            <Button className="rounded-full text-base" size="lg">
              Get Started <ArrowUpRight className="h-5! w-5!" />
            </Button>
            <Button
              className="rounded-full text-base shadow-none"
              size="lg"
              variant="outline"
            >
              <CirclePlay className="h-5! w-5!" /> Watch Demo
            </Button>
          </div>
        </div>
        <div className="aspect-video w-full rounded-xl lg:aspect-auto lg:h-screen lg:w-[1000px] lg:rounded-none overflow-hidden flex items-center justify-center">
            <div data-us-project="67Al8czdXlytAneACcol" style={{ width: '100%', height: '100%', minHeight: '500px' }}></div>
        </div>
      </div>
    </div>
  );
}
