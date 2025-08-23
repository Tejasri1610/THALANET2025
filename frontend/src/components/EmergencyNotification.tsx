import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, X, Clock, Heart } from "lucide-react";
import { Link } from "react-router-dom";

interface EmergencyNotificationProps {
  isVisible: boolean;
  onClose: () => void;
  request?: {
    id: string;
    title: string;
    bloodType: string;
    urgency: string;
    timeRemaining: string;
  };
}

const EmergencyNotification = ({ isVisible, onClose, request }: EmergencyNotificationProps) => {
  useEffect(() => {
    if (isVisible) {
      // Auto-hide after 10 seconds
      const timer = setTimeout(() => {
        onClose();
      }, 10000);

      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  if (!isVisible) return null;

  // Mock data for demonstration - replace with real data from API
  const mockRequest = request || {
    id: "new-1",
    title: "Urgent A+ Blood Required",
    bloodType: "A+",
    urgency: "critical",
    timeRemaining: "2 hours"
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'critical': return 'bg-red-500 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-black';
      default: return 'bg-gray-500 text-white';
    }
  };

  const getUrgencyLabel = (urgency: string) => {
    switch (urgency) {
      case 'critical': return 'Critical';
      case 'high': return 'High';
      case 'medium': return 'Medium';
      default: return 'Unknown';
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-in slide-in-from-bottom-2 duration-300">
      <Card className="w-80 shadow-2xl border-l-4 border-l-red-500 bg-background/95 backdrop-blur-md">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <div className="p-2 bg-red-100 rounded-full">
                <AlertTriangle className="text-red-600" size={20} />
              </div>
              <div>
                <CardTitle className="text-lg text-foreground">
                  New Emergency Request
                </CardTitle>
                <CardDescription className="text-sm text-muted-foreground">
                  A patient needs your help
                </CardDescription>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="h-8 w-8 p-0 hover:bg-red-50"
            >
              <X size={16} />
            </Button>
          </div>
        </CardHeader>
        
        <CardContent className="pt-0">
          <div className="space-y-3">
            <div>
              <h4 className="font-semibold text-foreground text-base">
                {mockRequest.title}
              </h4>
              <p className="text-sm text-muted-foreground">
                Blood type: <span className="font-medium text-primary">{mockRequest.bloodType}</span>
              </p>
            </div>
            
            <div className="flex items-center gap-2">
              <Badge className={getUrgencyColor(mockRequest.urgency)}>
                {getUrgencyLabel(mockRequest.urgency)}
              </Badge>
              <div className="flex items-center gap-1 text-sm text-muted-foreground">
                <Clock size={14} />
                {mockRequest.timeRemaining}
              </div>
            </div>
            
            <div className="flex gap-2">
              <Button 
                size="sm" 
                className="flex-1 bg-primary hover:bg-primary/90"
                onClick={() => {
                  onClose();
                  // Navigate to emergency page
                  window.location.href = "/emergency";
                }}
              >
                <Heart className="mr-2" size={14} />
                View Details
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={onClose}
              >
                Dismiss
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default EmergencyNotification;
