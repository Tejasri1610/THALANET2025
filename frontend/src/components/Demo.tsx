import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageCircle, Smartphone } from "lucide-react";
import whatsappMockup from "@/assets/whatsapp-mockup.jpg";

const Demo = () => {
  return (
    <section className="py-20 bg-accent/30">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Experience ThalaNet <span className="text-primary">Live Demo</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
            Try our intelligent chatbot now and see how AI can revolutionize healthcare support.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center max-w-6xl mx-auto">
          {/* Demo Interface */}
          <div className="relative">
            <div className="relative overflow-hidden rounded-2xl shadow-soft">
              <img 
                src={whatsappMockup} 
                alt="WhatsApp Chat Interface Demo" 
                className="w-full h-auto object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
            </div>
          </div>

          {/* Demo Content */}
          <div className="space-y-8">
            <Card className="border-primary/20 bg-card/80 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-2xl font-semibold text-foreground">
                  Try the Demo on Your Phone
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <p className="text-muted-foreground">
                  Send <strong className="text-primary">"Hi"</strong> to our WhatsApp number and experience the AI-powered support system firsthand.
                </p>
                
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <MessageCircle className="text-primary" size={20} />
                    <span className="text-foreground">Instant response from our AI assistant</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Smartphone className="text-primary" size={20} />
                    <span className="text-foreground">Smart questionnaire for quick assessment</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <MessageCircle className="text-primary" size={20} />
                    <span className="text-foreground">Real-time donor matching and alerts</span>
                  </div>
                </div>

                <div className="bg-accent/50 p-4 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-2">Example Questions:</p>
                  <div className="space-y-2 text-sm">
                    <div className="bg-primary/10 p-2 rounded text-primary">
                      "What is the patient's location?"
                    </div>
                    <div className="bg-primary/10 p-2 rounded text-primary">
                      "Are you looking to donate blood?"
                    </div>
                    <div className="bg-primary/10 p-2 rounded text-primary">
                      "What blood type is needed?"
                    </div>
                  </div>
                </div>

                <Button 
                  variant="whatsapp" 
                  size="lg" 
                  className="w-full"
                  onClick={() => window.open("https://wa.me/14155238886?text=Hi", "_blank")}
                >
                  <MessageCircle className="mr-2" size={20} />
                  Start Demo Chat
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Demo;