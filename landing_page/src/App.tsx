import FeaturesSection from "@/components/features-9"
import ContentSection from "@/components/content-5"
import IntegrationsSection from "@/components/integrations-7"
import FAQsThree from "@/components/faqs-3"
import CallToAction from "@/components/call-to-action"
import ContactSection from "@/components/contact"
import FooterSection from "@/components/footer"
import { GlowyWavesHero } from "@/components/uitripled/glowy-waves-hero-shadcnui"
import { N8nWorkflowBlock } from "@/components/uitripled/n8n-workflow-block-shadcnui"
import { StatsCounterBlock } from "@/components/uitripled/stats-counter-block-shadcnui"
import { BentoGridBlock } from "./components/uitripled/bento-grid-block-shadcnui"

function App() {
  return (
    <>
      <GlowyWavesHero />
      <StatsCounterBlock />
      <FeaturesSection />
      <N8nWorkflowBlock />
      <BentoGridBlock />
      <ContentSection />
      <IntegrationsSection />
      <FAQsThree />
      <CallToAction />
      <ContactSection />
      <FooterSection />
    </>
  )
}

export default App