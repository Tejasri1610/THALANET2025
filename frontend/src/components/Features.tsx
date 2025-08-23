import { Bot, AlertTriangle, Users, Brain, Database, Heart } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const Features = () => {
  const features = [
    
    {
      icon: Users,
      title: "Donor & Patient Insights",
      description: "Quickly visualize and categorize donors and patients for efficient planning.",
      color: "text-green-500"
    },
    {
      icon: Brain,
      title: "Donor Availability Prediction",
      description: "AI-driven insights to predict and enhance donor participation rates.",
      color: "text-purple-500"
    },
    {
      icon: Heart,
      title: "Smart Donor Match",
      description: "AI-powered matching of patients and donors by blood groups, location, and needs",
      color: "text-red-500"
    }
  ];

  return (
    <section className="py-20 bg-background">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Powered by <span className="text-primary">Advanced AI</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Our comprehensive platform leverages cutting-edge technology to create a seamless support network for the thalassemia community.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card key={index} className="hover:shadow-soft transition-all duration-300 hover:scale-105 border-border/50">
                <CardHeader className="text-center">
                  <div className={`mx-auto mb-4 p-3 rounded-full bg-accent/50 w-fit ${feature.color}`}>
                    <Icon size={32} />
                  </div>
                  <CardTitle className="text-xl font-semibold text-foreground">
                    {feature.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-center text-muted-foreground leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            );
          })}
        </div>
        
        <div className="mt-20 text-center">
          <div className="max-w-4xl mx-auto p-8 rounded-2xl bg-gradient-subtle border border-border/50">
            <h3 className="text-2xl md:text-3xl font-bold text-foreground mb-4">
              BLOOD WARRIORS Vision
            </h3>
            <p className="text-lg text-muted-foreground italic">
              "A Country where all the Thalassemia Patients receive the medical Support and live a healthy life with zero patients born by 2035"
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;