import { Heart, Droplets, Users, Calendar, MapPin, Phone, Mail, Clock } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Navigation from "@/components/Navigation";
import ThemeToggle from "@/components/ThemeToggle";

const Donate = () => {
  const donationCenters = [
    {
      name: "Apollo Blood Bank",
      location: "Mumbai, Maharashtra",
      phone: "+91-22-2490-0000",
      email: "bloodbank@apollohospitals.com",
      hours: "24/7",
      bloodTypes: ["A+", "B+", "O+", "AB+"]
    },
    {
      name: "Safdarjung Hospital Blood Bank",
      location: "Delhi, NCR",
      phone: "+91-11-2670-7444",
      email: "bloodbank@safdarjung.nic.in",
      hours: "8:00 AM - 8:00 PM",
      bloodTypes: ["All Types"]
    },
    {
      name: "Manipal Blood Bank",
      location: "Bangalore, Karnataka",
      phone: "+91-80-2222-0000",
      email: "bloodbank@manipal.edu",
      hours: "9:00 AM - 6:00 PM",
      bloodTypes: ["A+", "B+", "O+", "AB+"]
    }
  ];

  const donationProcess = [
    {
      step: "1",
      title: "Registration",
      description: "Complete a brief registration form with your basic information and medical history."
    },
    {
      step: "2",
      title: "Screening",
      description: "Undergo a quick health check including blood pressure, hemoglobin, and temperature."
    },
    {
      step: "3",
      title: "Donation",
      description: "The actual donation process takes about 8-10 minutes and is completely safe."
    },
    {
      step: "4",
      title: "Recovery",
      description: "Rest for 15-20 minutes while enjoying refreshments before leaving."
    }
  ];

  const eligibilityCriteria = [
    "Age between 18-65 years",
    "Weight at least 50 kg (110 lbs)",
    "Hemoglobin level 12.5 g/dL or higher",
    "No recent illnesses or medications",
    "No tattoos or piercings in last 6 months",
    "No recent travel to malaria-endemic areas"
  ];

  const benefits = [
    {
      icon: Heart,
      title: "Save Lives",
      description: "Your donation can save up to 3 lives and help patients in critical need."
    },
    {
      icon: Users,
      title: "Community Impact",
      description: "Contribute to building a stronger, more supportive healthcare community."
    },
    {
      icon: Clock,
      title: "Regular Health Checks",
      description: "Free health screenings and blood tests with every donation."
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
            <div className="flex items-center justify-center mb-6">
              <Heart className="text-red-500 mr-3" size={48} />
              <h1 className="text-4xl md:text-6xl font-bold text-foreground">
                Donate Blood, <span className="text-primary">Save Lives</span>
              </h1>
            </div>
            <p className="text-xl md:text-2xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
              Every drop counts. Your blood donation can make the difference between life and death 
              for thalassemia patients and others in need. Join our network of lifesavers today.
            </p>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-16">
            <Card className="text-center border-l-4 border-l-red-500">
              <CardContent className="pt-6">
                <div className="text-3xl font-bold text-red-500 mb-2">Every 2 Seconds</div>
                <div className="text-muted-foreground">Someone needs blood</div>
              </CardContent>
            </Card>
            <Card className="text-center border-l-4 border-l-orange-500">
              <CardContent className="pt-6">
                <div className="text-3xl font-bold text-orange-500 mb-2">1 Donation</div>
                <div className="text-muted-foreground">Can save up to 3 lives</div>
              </CardContent>
            </Card>
            <Card className="text-center border-l-4 border-l-green-500">
              <CardContent className="pt-6">
                <div className="text-3xl font-bold text-green-500 mb-2">56 Days</div>
                <div className="text-muted-foreground">Between donations</div>
              </CardContent>
            </Card>
            <Card className="text-center border-l-4 border-l-blue-500">
              <CardContent className="pt-6">
                <div className="text-3xl font-bold text-blue-500 mb-2">8-10 Minutes</div>
                <div className="text-muted-foreground">Donation process</div>
              </CardContent>
            </Card>
          </div>

          {/* Why Donate */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              Why Your Donation Matters
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {benefits.map((benefit, index) => {
                const Icon = benefit.icon;
                return (
                  <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="mx-auto mb-4 p-3 rounded-full bg-primary/10 w-fit">
                        <Icon className="text-primary" size={24} />
                      </div>
                      <CardTitle className="text-xl font-semibold text-foreground">
                        {benefit.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-muted-foreground">
                        {benefit.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* Donation Process */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              The Donation Process
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {donationProcess.map((process, index) => (
                <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="bg-primary/10 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <span className="text-2xl font-bold text-primary">{process.step}</span>
                    </div>
                    <CardTitle className="text-lg font-semibold text-foreground">
                      {process.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-muted-foreground">
                      {process.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Eligibility */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              Are You Eligible?
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <Card>
                <CardHeader>
                  <CardTitle className="text-2xl text-foreground flex items-center gap-3">
                    <Droplets className="text-primary" size={28} />
                    Eligibility Criteria
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {eligibilityCriteria.map((criteria, index) => (
                      <li key={index} className="flex items-start gap-3">
                        <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-muted-foreground">{criteria}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-2xl text-foreground flex items-center gap-3">
                    <Calendar className="text-primary" size={28} />
                    Before You Donate
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <h4 className="font-semibold text-green-800 mb-2">✅ Do:</h4>
                      <ul className="text-sm text-green-700 space-y-1">
                        <li>• Get a good night's sleep</li>
                        <li>• Eat a healthy meal 3 hours before</li>
                        <li>• Drink plenty of water</li>
                        <li>• Bring a valid ID</li>
                      </ul>
                    </div>
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <h4 className="font-semibold text-red-800 mb-2">❌ Don't:</h4>
                      <ul className="text-sm text-red-700 space-y-1">
                        <li>• Donate on an empty stomach</li>
                        <li>• Exercise heavily before donation</li>
                        <li>• Take aspirin 48 hours before</li>
                        <li>• Drink alcohol 24 hours before</li>
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Donation Centers */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              Find a Donation Center
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {donationCenters.map((center, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <CardTitle className="text-xl text-foreground">{center.name}</CardTitle>
                    <CardDescription className="flex items-center gap-2">
                      <MapPin className="text-muted-foreground" size={16} />
                      {center.location}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center gap-2">
                      <Phone className="text-muted-foreground" size={16} />
                      <span className="text-sm text-muted-foreground">{center.phone}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Mail className="text-muted-foreground" size={16} />
                      <span className="text-sm text-muted-foreground">{center.email}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="text-muted-foreground" size={16} />
                      <span className="text-sm text-muted-foreground">{center.hours}</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {center.bloodTypes.map((type, typeIndex) => (
                        <Badge key={typeIndex} variant="outline" className="border-primary text-primary">
                          {type}
                        </Badge>
                      ))}
                    </div>
                    <Button className="w-full bg-primary hover:bg-primary/90">
                      Schedule Donation
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Call to Action */}
          <div className="text-center">
            <Card className="bg-gradient-to-r from-red-50 to-red-100 border-red-200">
              <CardContent className="pt-12 pb-12">
                <h3 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
                  Ready to Save Lives?
                </h3>
                <p className="text-muted-foreground text-lg mb-8 max-w-2xl mx-auto">
                  Your blood donation can make an immediate difference. Join thousands of donors 
                  who are already part of our lifesaving network.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button size="lg" className="bg-red-600 hover:bg-red-700 text-white px-8 py-3">
                    <Heart className="mr-2" size={20} />
                    Find a Center Near You
                  </Button>
                </div>
                <p className="text-sm text-muted-foreground mt-6">
                  Have questions? Call our donation hotline: <strong>+91-1800-123-4567</strong>
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Donate;
