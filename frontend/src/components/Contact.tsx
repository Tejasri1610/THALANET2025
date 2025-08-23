import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Mail, MessageCircle, Users, Heart } from "lucide-react";

const Contact = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const [message, setMessage] = useState("");

  const handleSendEmail = () => {
    const subject = "Join ThalaNet Community";
    const body = `Hello ThalaNet Team,

I would like to join the ThalaNet community and contribute.

Here are my details:
- Name: ${firstName} ${lastName}
- Email: ${email}
- Role: ${role}
- Message: ${message}

Regards,
${firstName} ${lastName}`;

    window.location.href = `mailto:contact@thalanet.org?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  };

  return (
    <section className="py-20 bg-accent/30">
      <div className="container mx-auto px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
              Join the <span className="text-primary">ThalaNet Community</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Be part of a life-saving network. Whether you're a patient, donor, healthcare provider, 
              or volunteer, there's a place for you in our community.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <Card className="shadow-soft border-border/50">
              <CardHeader>
                <CardTitle className="text-2xl font-semibold text-foreground flex items-center">
                  <Heart className="mr-3 text-primary" size={28} />
                  Get Involved
                </CardTitle>
                <CardDescription className="text-muted-foreground">
                  Join our mission to revolutionize healthcare support through technology and compassion.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="firstName" className="text-foreground">First Name</Label>
                    <Input 
                      id="firstName" 
                      placeholder="Enter your first name" 
                      className="mt-1"
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                    />
                  </div>
                  <div>
                    <Label htmlFor="lastName" className="text-foreground">Last Name</Label>
                    <Input 
                      id="lastName" 
                      placeholder="Enter your last name" 
                      className="mt-1"
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)}
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="email" className="text-foreground">Email Address</Label>
                  <Input 
                    id="email" 
                    type="email" 
                    placeholder="your.email@example.com" 
                    className="mt-1"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>

                <div>
                  <Label htmlFor="role" className="text-foreground">How would you like to contribute?</Label>
                  <select 
                    id="role" 
                    className="w-full mt-1 p-2 border border-input rounded-md bg-background text-foreground"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                  >
                    <option value="">Select your role</option>
                    <option value="Blood Donor">Blood Donor</option>
                    <option value="Patient/Caregiver">Patient/Caregiver</option>
                    <option value="Healthcare Provider">Healthcare Provider</option>
                    <option value="Volunteer">Volunteer</option>
                    <option value="Developer/Contributor">Developer/Contributor</option>
                  </select>
                </div>

                <div>
                  <Label htmlFor="message" className="text-foreground">Message</Label>
                  <Textarea 
                    id="message" 
                    placeholder="Tell us about your interest in ThalaNet and how you'd like to contribute..."
                    className="mt-1"
                    rows={4}
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                  />
                </div>

                <Button 
                  variant="hero" 
                  size="lg" 
                  className="w-full"
                  onClick={handleSendEmail}
                >
                  <Mail className="mr-2" size={20} />
                  Join ThalaNet Community
                </Button>
              </CardContent>
            </Card>

            {/* Contact Options */}
            <div className="space-y-8">
              <Card className="shadow-soft border-border/50">
                <CardHeader>
                  <CardTitle className="text-xl font-semibold text-foreground flex items-center">
                    <MessageCircle className="mr-3 text-primary" size={24} />
                    Start Using ThalaNet
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4">
                    Ready to experience AI-powered healthcare support? Connect with our WhatsApp chatbot now.
                  </p>
                  <Button 
                    variant="whatsapp" 
                    size="lg" 
                    className="w-full"
                    onClick={() => window.open("https://wa.me/1234567890", "_blank")}
                  >
                    <MessageCircle className="mr-2" size={20} />
                    Chat with ThalaNet Bot
                  </Button>
                </CardContent>
              </Card>

              <Card className="shadow-soft border-border/50">
                <CardHeader>
                  <CardTitle className="text-xl font-semibold text-foreground flex items-center">
                    <Users className="mr-3 text-primary" size={24} />
                    Connect With Us
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <Mail className="text-primary" size={20} />
                    <span className="text-muted-foreground">contact@thalanet.org</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <MessageCircle className="text-primary" size={20} />
                    <span className="text-muted-foreground">+91 98765 43210</span>
                  </div>
                  
                  <div className="pt-4">
                    <p className="text-sm text-muted-foreground mb-3">Follow our journey:</p>
                    <div className="flex space-x-4">
                      <Button variant="outline" size="sm">Twitter</Button>
                      <Button variant="outline" size="sm">LinkedIn</Button>
                      <Button variant="outline" size="sm">GitHub</Button>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="bg-gradient-hero p-6 rounded-xl text-center">
                <h3 className="text-xl font-semibold text-primary-foreground mb-2">
                  Every Connection Saves Lives
                </h3>
                <p className="text-primary-foreground/90 text-sm">
                  Join thousands of donors, patients, and healthcare heroes making a difference.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
