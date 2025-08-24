import { Button } from "@/components/ui/button";
import { MessageCircle, Heart, AlertTriangle } from "lucide-react";
import { Link } from "react-router-dom";
import heroImage from "@/assets/hero-image.jpg";

const Hero = () => {
  return (
    <section className="relative flex items-center justify-center bg-gradient-subtle overflow-hidden pt-24 pb-16 min-h-[calc(100vh-100px)]">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <img
          src={heroImage}
          alt="ThalaNet Community"
          className="w-full h-full object-cover opacity-20"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-background/80 to-background/60"></div>
      </div>

      {/* Floating Hearts Animation */}
      <div className="absolute inset-0 z-1">
        <Heart className="absolute top-20 left-20 text-primary/20 animate-float" size={24} />
        <Heart className="absolute top-40 right-32 text-primary/15 animate-pulse-soft" size={32} />
        <Heart className="absolute bottom-40 left-16 text-primary/25 animate-float" size={20} />
      </div>

      <div className="relative z-10 container mx-auto px-6 text-center">
        <div className="max-w-4xl mx-auto">
          {/* Main Headline */}
          <h1 className="text-5xl md:text-7xl font-bold text-foreground mb-6 leading-tight">
            Life-Saving Support,{" "}
            <span className="text-primary bg-gradient-hero bg-clip-text text-transparent">
              One Chat Away
            </span>
          </h1>

          {/* Subtext */}
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 leading-relaxed max-w-3xl mx-auto">
            ThalaNet connects patients, donors, and hospitals in real-time using AI and Intelligent Chatbots.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Button
              variant="whatsapp"
              size="xl"
              className="min-w-[250px]"
              onClick={() => window.open("https://wa.me/14155238886?text=join%20practical-package", "_blank")}
            >
              <MessageCircle className="mr-2" size={24} />
              Start Chat on WhatsApp
            </Button>
            <Link to="/emergency">
              <Button
                variant="destructive"
                size="xl"
                className="min-w-[250px] bg-red-600 hover:bg-red-700"
              >
                <AlertTriangle className="mr-2" size={24} />
                Emergency Requests
              </Button>
            </Link>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-2">24/7</div>
              <div className="text-muted-foreground">AI Support Available</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-2">1000+</div>
              <div className="text-muted-foreground">Lives Connected</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-2">5 Min</div>
              <div className="text-muted-foreground">Average Response Time</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
