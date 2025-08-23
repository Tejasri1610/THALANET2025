import Hero from "@/components/Hero";
import Features from "@/components/Features";
import Contact from "@/components/Contact";
import Crowdfunding from "@/components/Crowdfunding";
import Navigation from "@/components/Navigation";
import ThemeToggle from "@/components/ThemeToggle";

const Index = () => {
  return (
    <div className="min-h-screen">
      <Navigation />
      <div className="fixed top-4 right-4 z-50">
        <ThemeToggle />
      </div>
      <div id="hero">
        <Hero />
      </div>
      <div id="features">
        <Features />
      </div>
      <Crowdfunding />
      <div id="contact">
        <Contact />
      </div>
    </div>
  );
};

export default Index;
