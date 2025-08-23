import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MessageCircle, Phone, Mail, MapPin, Clock, Send, Users, Heart } from "lucide-react";
import Navigation from "@/components/Navigation";
import ThemeToggle from "@/components/ThemeToggle";
import { useToast } from "@/hooks/use-toast";
import { contactApi, ContactFormData } from "@/services/api";

const Contact = () => {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [formData, setFormData] = useState<ContactFormData>({
    name: "",
    email: "",
    phone: "",
    subject: "",
    message: "",
    inquiryType: ""
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Submit the contact form using the API service
      const response = await contactApi.submit(formData);

      if (response.success) {
        // Show success message
        toast({
          title: "Message Sent Successfully!",
          description: response.message,
          variant: "default",
        });

        // Reset form
        setFormData({
          name: "",
          email: "",
          phone: "",
          subject: "",
          message: "",
          inquiryType: ""
        });
      } else {
        throw new Error(response.message);
      }
      
    } catch (error) {
      console.error("Error sending message:", error);
      toast({
        title: "Error Sending Message",
        description: "There was an error sending your message. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const contactInfo = [
    {
      icon: Phone,
      title: "Phone",
      details: [
        "+91-1800-123-4567 (Toll Free)",
        "+91-98765-43210 (Emergency)"
      ],
      color: "text-blue-500"
    },
    {
      icon: Mail,
      title: "Email",
      details: [
        "info@thalanet.org",
        "support@thalanet.org",
        "emergency@thalanet.org"
      ],
      color: "text-green-500"
    },
    {
      icon: MapPin,
      title: "Address",
      details: [
        "ThalaNet Foundation",
        "123 Healthcare Avenue",
        "Mumbai, Maharashtra 400001",
        "India"
      ],
      color: "text-red-500"
    },
    {
      icon: Clock,
      title: "Working Hours",
      details: [
        "Monday - Friday: 9:00 AM - 6:00 PM",
        "Saturday: 9:00 AM - 2:00 PM",
        "Emergency Support: 24/7"
      ],
      color: "text-purple-500"
    }
  ];

  const faqs = [
    {
      question: "How can I become a blood donor?",
      answer: "You can register as a donor through our website or by calling our toll-free number. We'll guide you through the eligibility criteria and donation process."
    },
    {
      question: "How quickly can you respond to emergency requests?",
      answer: "Our AI system processes emergency requests within minutes and notifies potential donors immediately. Response times vary by location but typically range from 15 minutes to 2 hours."
    },
    {
      question: "Is my personal information safe?",
      answer: "Yes, we follow strict data protection protocols and comply with all healthcare privacy regulations. Your information is only shared with verified healthcare providers when necessary."
    },
    {
      question: "Can I volunteer with ThalaNet?",
      answer: "Absolutely! We welcome volunteers for various roles including community outreach, event coordination, and administrative support. Contact us to learn about current opportunities."
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
              <MessageCircle className="text-primary mr-3" size={48} />
              <h1 className="text-4xl md:text-6xl font-bold text-foreground">
                Get in <span className="text-primary">Touch</span>
              </h1>
            </div>
            <p className="text-xl md:text-2xl text-muted-foreground max-w-4xl mx-auto leading-relaxed">
              Have questions about blood donation, need emergency assistance, or want to partner with us? 
              We're here to help. Reach out to our team anytime.
            </p>
          </div>

          {/* Contact Information */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              Contact Information
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {contactInfo.map((info, index) => {
                const Icon = info.icon;
                return (
                  <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className={`mx-auto mb-4 p-3 rounded-full bg-accent/50 w-fit ${info.color}`}>
                        <Icon size={24} />
                      </div>
                      <CardTitle className="text-lg font-semibold text-foreground">
                        {info.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        {info.details.map((detail, detailIndex) => (
                          <p key={detailIndex} className="text-sm text-muted-foreground">
                            {detail}
                          </p>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* Contact Form and Map */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-20">
            {/* Contact Form */}
            <div>
              <h2 className="text-3xl font-bold text-foreground mb-8">
                Send us a Message
              </h2>
              <Card>
                <CardContent className="pt-6">
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label htmlFor="name">Full Name *</Label>
                        <Input
                          id="name"
                          placeholder="Your full name"
                          value={formData.name}
                          onChange={(e) => handleInputChange("name", e.target.value)}
                          required
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="email">Email *</Label>
                        <Input
                          id="email"
                          type="email"
                          placeholder="your.email@example.com"
                          value={formData.email}
                          onChange={(e) => handleInputChange("email", e.target.value)}
                          required
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label htmlFor="phone">Phone Number</Label>
                        <Input
                          id="phone"
                          placeholder="+91-98765-43210"
                          value={formData.phone}
                          onChange={(e) => handleInputChange("phone", e.target.value)}
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="inquiryType">Inquiry Type</Label>
                        <Select value={formData.inquiryType} onValueChange={(value) => handleInputChange("inquiryType", value)}>
                          <SelectTrigger>
                            <SelectValue placeholder="Select inquiry type" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="general">General Inquiry</SelectItem>
                            <SelectItem value="blood-request">Blood Request</SelectItem>
                            <SelectItem value="donation">Blood Donation</SelectItem>
                            <SelectItem value="volunteer">Volunteering</SelectItem>
                            <SelectItem value="partnership">Partnership</SelectItem>
                            <SelectItem value="support">Technical Support</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="subject">Subject *</Label>
                      <Input
                        id="subject"
                        placeholder="Brief description of your inquiry"
                        value={formData.subject}
                        onChange={(e) => handleInputChange("subject", e.target.value)}
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="message">Message *</Label>
                      <Textarea
                        id="message"
                        placeholder="Please provide detailed information about your inquiry..."
                        value={formData.message}
                        onChange={(e) => handleInputChange("message", e.target.value)}
                        rows={5}
                        required
                      />
                    </div>

                    <Button
                      type="submit"
                      size="lg"
                      disabled={isSubmitting}
                      className="w-full bg-primary hover:bg-primary/90"
                    >
                      {isSubmitting ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Sending Message...
                        </>
                      ) : (
                        <>
                          <Send className="mr-2" size={20} />
                          Send Message
                        </>
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Map and Additional Info */}
            <div>
              <h2 className="text-3xl font-bold text-foreground mb-8">
                Visit Our Office
              </h2>
              
              {/* Map Placeholder */}
              <Card className="mb-6">
                <CardContent className="pt-6">
                  <div className="bg-muted rounded-lg h-64 flex items-center justify-center">
                    <div className="text-center">
                      <MapPin className="mx-auto text-muted-foreground mb-2" size={32} />
                      <p className="text-muted-foreground">Interactive Map</p>
                      <p className="text-sm text-muted-foreground">Coming Soon</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Quick Actions */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-xl text-foreground">
                    Quick Actions
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button variant="outline" className="w-full justify-start" onClick={() => window.open("tel:+91-1800-123-4567")}>
                    <Phone className="mr-2" size={16} />
                    Call Toll Free
                  </Button>
                  <Button variant="outline" className="w-full justify-start" onClick={() => window.open("mailto:emergency@thalanet.org")}>
                    <Mail className="mr-2" size={16} />
                    Emergency Email
                  </Button>
                  <Button variant="outline" className="w-full justify-start" onClick={() => window.open("https://wa.me/919876543210?text=Hi, I need assistance with ThalaNet", "_blank")}>
                    <MessageCircle className="mr-2" size={16} />
                    WhatsApp Support
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* FAQs */}
          <div className="mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
              Frequently Asked Questions
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {faqs.map((faq, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <CardTitle className="text-lg font-semibold text-foreground">
                      {faq.question}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-muted-foreground">
                      {faq.answer}
                    </CardDescription>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Call to Action */}
          <div className="text-center">
            <Card className="bg-gradient-to-r from-primary/10 to-primary/5 border-primary/20">
              <CardContent className="pt-12 pb-12">
                <h3 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
                  Ready to Make a Difference?
                </h3>
                <p className="text-muted-foreground text-lg mb-8 max-w-2xl mx-auto">
                  Join our community of lifesavers. Whether you want to donate blood, 
                  volunteer, or partner with us, we're here to support your journey.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button size="lg" className="bg-primary hover:bg-primary/90 text-white px-8 py-3">
                    <Heart className="mr-2" size={20} />
                    Become a Donor
                  </Button>
                  <Button size="lg" variant="outline" className="border-primary text-primary hover:bg-primary hover:text-white px-8 py-3">
                    <Users className="mr-2" size={20} />
                    Volunteer With Us
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
