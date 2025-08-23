import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { AlertTriangle, ArrowLeft, Save } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import Navigation from "@/components/Navigation";
import ThemeToggle from "@/components/ThemeToggle";
import { useToast } from "@/hooks/use-toast";
import { urgentRequestsApi, CreateRequestData } from "@/services/api";

const AdminNewRequest = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    bloodType: "",
    location: "",
    requesterName: "",
    requesterPhone: "",
    hospital: "",
    urgency: "high" as const,
    expiryHours: "24"
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
      // Create the request data object
      const requestData: CreateRequestData = {
        title: formData.title,
        description: formData.description,
        bloodType: formData.bloodType,
        location: formData.location,
        requesterName: formData.requesterName,
        requesterPhone: formData.requesterPhone,
        hospital: formData.hospital,
        urgency: formData.urgency,
        expiryHours: parseInt(formData.expiryHours)
      };

      // Submit the request using the API service
      await urgentRequestsApi.create(requestData);

      // Show success message
      toast({
        title: "Request Submitted Successfully!",
        description: "Your urgent blood request has been posted and is now visible to potential donors.",
        variant: "default",
      });

      // Redirect to emergency requests page
      navigate("/emergency");
      
    } catch (error) {
      console.error("Error submitting request:", error);
      toast({
        title: "Error Submitting Request",
        description: "There was an error submitting your request. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const isFormValid = () => {
    return formData.title && 
           formData.description && 
           formData.bloodType && 
           formData.location && 
           formData.requesterName && 
           formData.requesterPhone && 
           formData.hospital;
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="fixed top-4 right-4 z-50">
        <ThemeToggle />
      </div>
      
      <div className="pt-20 pb-10">
        <div className="container mx-auto px-6 max-w-4xl">
          {/* Header */}
          <div className="flex items-center gap-4 mb-8">
            <Link to="/emergency">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="mr-2" size={16} />
                Back to Emergency Requests
              </Button>
            </Link>
          </div>

          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <AlertTriangle className="text-red-500 mr-3" size={32} />
              <h1 className="text-4xl md:text-5xl font-bold text-foreground">
                Submit New Urgent Request
              </h1>
            </div>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Submit an urgent blood request that will be immediately visible to potential donors across the network.
            </p>
          </div>

          {/* Form */}
          <Card className="border-l-4 border-l-red-500">
            <CardHeader>
              <CardTitle className="text-2xl text-foreground">
                Request Details
              </CardTitle>
              <CardDescription>
                Fill in all the required information to create an urgent blood request.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Basic Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="title">Request Title *</Label>
                    <Input
                      id="title"
                      placeholder="e.g., Urgent B+ Blood Required for Surgery"
                      value={formData.title}
                      onChange={(e) => handleInputChange("title", e.target.value)}
                      required
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="bloodType">Blood Type Required *</Label>
                    <Select value={formData.bloodType} onValueChange={(value) => handleInputChange("bloodType", value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select blood type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="A+">A+</SelectItem>
                        <SelectItem value="A-">A-</SelectItem>
                        <SelectItem value="B+">B+</SelectItem>
                        <SelectItem value="B-">B-</SelectItem>
                        <SelectItem value="AB+">AB+</SelectItem>
                        <SelectItem value="AB-">AB-</SelectItem>
                        <SelectItem value="O+">O+</SelectItem>
                        <SelectItem value="O-">O-</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Description *</Label>
                  <Textarea
                    id="description"
                    placeholder="Provide detailed information about the patient's condition, why blood is needed, and any specific requirements..."
                    value={formData.description}
                    onChange={(e) => handleInputChange("description", e.target.value)}
                    rows={4}
                    required
                  />
                </div>

                {/* Location and Hospital */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="location">Location *</Label>
                    <Input
                      id="location"
                      placeholder="e.g., Mumbai, Maharashtra"
                      value={formData.location}
                      onChange={(e) => handleInputChange("location", e.target.value)}
                      required
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="hospital">Hospital/Medical Center *</Label>
                    <Input
                      id="hospital"
                      placeholder="e.g., Apollo Hospital"
                      value={formData.hospital}
                      onChange={(e) => handleInputChange("hospital", e.target.value)}
                      required
                    />
                  </div>
                </div>

                {/* Requester Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="requesterName">Requester Name *</Label>
                    <Input
                      id="requesterName"
                      placeholder="e.g., Dr. Priya Sharma or Patient Name"
                      value={formData.requesterName}
                      onChange={(e) => handleInputChange("requesterName", e.target.value)}
                      required
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="requesterPhone">Contact Phone *</Label>
                    <Input
                      id="requesterPhone"
                      placeholder="e.g., +91-98765-43210"
                      value={formData.requesterPhone}
                      onChange={(e) => handleInputChange("requesterPhone", e.target.value)}
                      required
                    />
                  </div>
                </div>

                {/* Urgency and Expiry */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="urgency">Urgency Level *</Label>
                    <Select value={formData.urgency} onValueChange={(value) => handleInputChange("urgency", value)}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="critical">Critical (Immediate - within 1-3 hours)</SelectItem>
                        <SelectItem value="high">High (Today - within 24 hours)</SelectItem>
                        <SelectItem value="medium">Medium (1-5 days)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="expiryHours">Expiry Time (Hours) *</Label>
                    <Select value={formData.expiryHours} onValueChange={(value) => handleInputChange("expiryHours", value)}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="2">2 hours</SelectItem>
                        <SelectItem value="4">4 hours</SelectItem>
                        <SelectItem value="8">8 hours</SelectItem>
                        <SelectItem value="12">12 hours</SelectItem>
                        <SelectItem value="24">24 hours</SelectItem>
                        <SelectItem value="48">48 hours</SelectItem>
                        <SelectItem value="72">72 hours</SelectItem>
                        <SelectItem value="120">5 days</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {/* Important Notice */}
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="text-yellow-600 mt-1" size={20} />
                    <div>
                      <h4 className="font-semibold text-yellow-800">Important Information</h4>
                      <ul className="text-sm text-yellow-700 mt-2 space-y-1">
                        <li>• All requests are verified before being posted publicly</li>
                        <li>• Contact information will be visible to potential donors</li>
                        <li>• Requests automatically expire after the specified time</li>
                        <li>• You can update or cancel your request at any time</li>
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Submit Button */}
                <div className="flex justify-center pt-6">
                  <Button
                    type="submit"
                    size="lg"
                    disabled={!isFormValid() || isSubmitting}
                    className="min-w-[200px] bg-red-600 hover:bg-red-700"
                  >
                    {isSubmitting ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Submitting...
                      </>
                    ) : (
                      <>
                        <Save className="mr-2" size={20} />
                        Submit Request
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>

          {/* Additional Information */}
          <div className="mt-8 text-center">
            <p className="text-muted-foreground">
              Need help? Contact our support team at{" "}
              <a href="mailto:support@thalanet.org" className="text-primary hover:underline">
                support@thalanet.org
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminNewRequest;
