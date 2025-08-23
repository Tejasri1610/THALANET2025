import { Heart, Users, Target, Award, Globe, Shield } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Navigation from "@/components/Navigation";
import ThemeToggle from "@/components/ThemeToggle";

const About = () => {
  const stats = [
    { icon: Heart, value: "1000+", label: "Lives Saved" },
    { icon: Users, value: "50,000+", label: "Active Donors" },
    { icon: Globe, value: "25+", label: "Cities Covered" },
    { icon: Award, value: "99.9%", label: "Success Rate" },
  ];

  const values = [
    {
      icon: Heart,
      title: "Compassion",
      description: "We believe every life is precious and deserves the best possible care and support."
    },
    {
      icon: Shield,
      title: "Trust & Safety",
      description: "All our processes are designed with patient and donor safety as the top priority."
    },
    {
      icon: Target,
      title: "Innovation",
      description: "We leverage cutting-edge AI technology to create efficient, life-saving connections."
    },
    {
      icon: Users,
      title: "Community",
      description: "Building a strong, supportive network of donors, patients, and healthcare providers."
    }
  ];

  const team = [
    {
      name: "Dr. Priya Sharma",
      role: "Medical Director",
      description: "Leading pediatrician with 15+ years experience in thalassemia care."
    },
    {
      name: "Rahul Verma",
      role: "Technology Lead",
      description: "AI/ML expert focused on healthcare technology solutions."
    },
    {
      name: "Dr. Amit Patel",
      role: "Operations Head",
      description: "Healthcare management professional with extensive network experience."
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="fixed top-4 right-4 z-50">
        <ThemeToggle />
      </div>
      
      <div className="pt-20 pb-10">
        <div className="container mx-auto px-6">
          {/* Hero Section */}
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6">
              About <span className="text-primary">ThalaNet</span>
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
              We are a mission-driven organization dedicated to creating a world where no thalassemia patient 
              suffers due to lack of blood or support. Our AI-powered platform connects donors, patients, 
              and healthcare providers in real-time.
            </p>
          </div>

          {/* Mission & Vision */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-20">
            <Card className="border-l-4 border-l-primary">
              <CardHeader>
                <CardTitle className="text-2xl text-foreground flex items-center gap-3">
                  <Target className="text-primary" size={28} />
                  Our Mission
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground text-lg leading-relaxed">
                  To eliminate blood shortage for thalassemia patients by creating an intelligent, 
                  real-time network that connects donors with patients within minutes, ensuring 
                  timely access to life-saving blood transfusions.
                </p>
              </CardContent>
            </Card>

            <Card className="border-l-4 border-l-primary">
              <CardHeader>
                <CardTitle className="text-2xl text-foreground flex items-center gap-3">
                  <Award className="text-primary" size={28} />
                  Our Vision
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground text-lg leading-relaxed">
                  A country where all thalassemia patients receive the medical support they need 
                  and live healthy lives, with zero new thalassemia patients born by 2035 through 
                  awareness and prevention programs.
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Stats */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              Our Impact
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => {
                const Icon = stat.icon;
                return (
                  <div key={index} className="text-center">
                    <div className="bg-primary/10 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                      <Icon className="text-primary" size={32} />
                    </div>
                    <div className="text-3xl font-bold text-primary mb-2">{stat.value}</div>
                    <div className="text-muted-foreground">{stat.label}</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Values */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              Our Values
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {values.map((value, index) => {
                const Icon = value.icon;
                return (
                  <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="mx-auto mb-4 p-3 rounded-full bg-primary/10 w-fit">
                        <Icon className="text-primary" size={24} />
                      </div>
                      <CardTitle className="text-xl font-semibold text-foreground">
                        {value.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-muted-foreground">
                        {value.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* How It Works */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              How ThalaNet Works
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="bg-primary/10 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">1</span>
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-3">Emergency Request</h3>
                <p className="text-muted-foreground">
                  Healthcare providers submit urgent blood requests through our platform with 
                  detailed patient information and urgency levels.
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-primary/10 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">2</span>
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-3">AI Matching</h3>
                <p className="text-muted-foreground">
                  Our AI system instantly matches requests with available donors based on 
                  blood type, location, and availability.
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-primary/10 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">3</span>
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-3">Connection</h3>
                <p className="text-muted-foreground">
                  Donors receive immediate notifications and can directly contact 
                  healthcare providers to arrange donation.
                </p>
              </div>
            </div>
          </div>

          {/* Team */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              Our Team
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {team.map((member, index) => (
                <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="w-24 h-24 bg-primary/10 rounded-full mx-auto mb-4 flex items-center justify-center">
                      <Users className="text-primary" size={32} />
                    </div>
                    <CardTitle className="text-xl font-semibold text-foreground">
                      {member.name}
                    </CardTitle>
                    <CardDescription className="text-primary font-medium">
                      {member.role}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground">
                      {member.description}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Call to Action */}
          <div className="text-center">
            <Card className="bg-gradient-to-r from-primary/10 to-primary/5 border-primary/20">
              <CardContent className="pt-8 pb-8">
                <h3 className="text-2xl md:text-3xl font-bold text-foreground mb-4">
                  Join Our Mission
                </h3>
                <p className="text-muted-foreground text-lg mb-6 max-w-2xl mx-auto">
                  Whether you're a potential donor, healthcare provider, or supporter, 
                  there are many ways you can help us save lives and build a stronger community.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <a href="/emergency" className="inline-block">
                    <button className="bg-primary hover:bg-primary/90 text-white px-8 py-3 rounded-lg font-semibold transition-colors">
                      View Emergency Requests
                    </button>
                  </a>
                  <a href="/contact" className="inline-block">
                    <button className="border border-primary text-primary hover:bg-primary hover:text-white px-8 py-3 rounded-lg font-semibold transition-colors">
                      Get in Touch
                    </button>
                  </a>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
