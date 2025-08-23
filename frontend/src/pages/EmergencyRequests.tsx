import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  AlertTriangle,
  Clock,
  User,
  MapPin,
  Filter,
  Plus,
  Share2,
  Twitter,
  Linkedin,
  Instagram,
  MessageCircle,
  Send,
  Copy,
} from "lucide-react";
import { Link } from "react-router-dom";
import Navigation from "@/components/Navigation";
import ThemeToggle from "@/components/ThemeToggle";
import { urgentRequestsApi, UrgentRequest } from "@/services/api";

/* ------------------ SHARE BUTTON ------------------ */
const ShareButton = ({ request }: { request: UrgentRequest }) => {
  const [open, setOpen] = useState(false);

  const shareText = `🚨 Urgent Blood Required 🚨
Blood Type: ${request.bloodType}
Location: ${request.location}
Hospital: ${request.hospital}
Requester: ${request.requesterName} (${request.requesterPhone})
Details: ${request.title} - ${request.description}
Please help/save a life! 🙏`;

  const encodedText = encodeURIComponent(shareText);

  const socials = [
    {
      name: "WhatsApp",
      icon: <MessageCircle size={18} />,
      url: `https://wa.me/?text=${encodedText}`,
    },
    {
      name: "Twitter",
      icon: <Twitter size={18} />,
      url: `https://twitter.com/intent/tweet?text=${encodedText}`,
    },
    {
      name: "LinkedIn",
      icon: <Linkedin size={18} />,
      url: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(
        "https://yourapp.com/share?text=" + shareText
      )}`,
    },
    {
      name: "Instagram",
      icon: <Instagram size={18} />,
      url: `https://www.instagram.com/`, // fallback only
    },
    {
      name: "Telegram",
      icon: <Send size={18} />,
      url: `https://t.me/share/url?url=${encodedText}&text=${encodedText}`,
    },
  ];

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shareText);
      console.log("Copied request details to clipboard!");
    } catch (err) {
      console.error("Failed to copy text", err);
    }
    setOpen(false);
  };

  return (
    <div className="relative">
      <Button
        variant="outline"
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2"
      >
        <Share2 size={16} />
        Share
      </Button>

      {open && (
        <div className="absolute mt-2 bg-background border rounded-xl shadow-lg p-2 z-50 flex flex-col gap-1 w-44">
          {socials.map((s) => (
            <a
              key={s.name}
              href={s.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 p-2 rounded text-sm text-foreground hover:bg-muted transition"
            >
              {s.icon}
              {s.name}
            </a>
          ))}
          <button
            onClick={copyToClipboard}
            className="flex items-center gap-2 p-2 rounded text-sm text-foreground hover:bg-muted transition"
          >
            <Copy size={16} />
            Copy Text
          </button>
        </div>
      )}
    </div>
  );
};

/* ------------------ EMERGENCY REQUESTS PAGE ------------------ */
const EmergencyRequests = () => {
  const [requests, setRequests] = useState<UrgentRequest[]>([]);
  const [filteredRequests, setFilteredRequests] = useState<UrgentRequest[]>([]);
  const [urgencyFilter, setUrgencyFilter] = useState<string>("all");
  const [bloodTypeFilter, setBloodTypeFilter] = useState<string>("all");
  const [locationFilter, setLocationFilter] = useState<string>("all");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      setIsLoading(true);
      const data = await urgentRequestsApi.getAll();
      setRequests(data);
      setFilteredRequests(data);
    } catch (error) {
      console.error("Error fetching requests:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const filtered = requests.filter((request) => {
      const matchesUrgency =
        urgencyFilter === "all" || request.urgency === urgencyFilter;
      const matchesBloodType =
        bloodTypeFilter === "all" || request.bloodType === bloodTypeFilter;
      const matchesLocation =
        locationFilter === "all" || request.location === locationFilter;
      return matchesUrgency && matchesBloodType && matchesLocation;
    });
    setFilteredRequests(filtered);
  }, [requests, urgencyFilter, bloodTypeFilter, locationFilter]);

  const getTimeRemaining = (expiryTime: Date) => {
    const now = new Date();
    const diff = new Date(expiryTime).getTime() - now.getTime();
    if (diff <= 0) return "Expired";
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    if (hours < 1) return `${minutes}m remaining`;
    if (hours < 24) return `${hours}h ${minutes}m remaining`;
    const days = Math.floor(hours / 24);
    return `${days}d ${hours % 24}h remaining`;
  };

  const urgencyColors: Record<string, string> = {
    critical: "bg-red-500 text-white",
    high: "bg-orange-500 text-white",
    medium: "bg-yellow-500 text-black",
    default: "bg-gray-500 text-white",
  };

  const urgencyLabels: Record<string, string> = {
    critical: "Critical",
    high: "High",
    medium: "Medium",
    default: "Unknown",
  };

  const clearFilters = () => {
    setUrgencyFilter("all");
    setBloodTypeFilter("all");
    setLocationFilter("all");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="fixed top-4 right-4 z-50">
          <ThemeToggle />
        </div>
        <div className="pt-20 pb-10 flex justify-center items-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">
              Loading emergency requests...
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <div className="fixed top-4 right-4 z-50">
        <ThemeToggle />
      </div>

      <div className="pt-20 pb-10 container mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <AlertTriangle className="text-red-500 mr-3" size={32} />
            <h1 className="text-4xl md:text-5xl font-bold text-foreground">
              Emergency Blood Requests
            </h1>
          </div>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Urgent blood requirements from patients across the country. Every
            minute counts.
          </p>
        </div>

        {/* Admin Button */}
        <div className="text-center mb-8">
          <Link to="/admin/new-request">
            <Button className="bg-primary hover:bg-primary/90">
              <Plus className="mr-2" size={20} />
              Submit New Request
            </Button>
          </Link>
        </div>

        {/* Filters */}
        <div className="bg-muted rounded-xl p-6 mb-10">
          <div className="flex flex-col md:flex-row gap-4 md:items-end">
            {/* Urgency */}
            <div className="flex-1">
              <label className="text-sm font-medium text-muted-foreground">
                Urgency
              </label>
              <Select value={urgencyFilter} onValueChange={setUrgencyFilter}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select urgency" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All urgency levels</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Blood Type */}
            <div className="flex-1">
              <label className="text-sm font-medium text-muted-foreground">
                Blood Type
              </label>
              <Select value={bloodTypeFilter} onValueChange={setBloodTypeFilter}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select blood type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All blood types</SelectItem>
                  {["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].map(
                    (bt) => (
                      <SelectItem key={bt} value={bt}>
                        {bt}
                      </SelectItem>
                    )
                  )}
                </SelectContent>
              </Select>
            </div>

            {/* Location */}
            <div className="flex-1">
              <label className="text-sm font-medium text-muted-foreground">
                Location
              </label>
              <Select value={locationFilter} onValueChange={setLocationFilter}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select location" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All locations</SelectItem>
                  {Array.from(new Set(requests.map((req) => req.location))).map(
                    (loc) => (
                      <SelectItem key={loc} value={loc}>
                        {loc}
                      </SelectItem>
                    )
                  )}
                </SelectContent>
              </Select>
            </div>

            {/* Clear Filters */}
            <Button
              variant="outline"
              onClick={clearFilters}
              className="flex items-center gap-2"
            >
              <Filter size={16} />
              Clear Filters
            </Button>
          </div>
        </div>

        {/* Requests List */}
        <div className="space-y-6">
          {filteredRequests.map((request) => (
            <Card
              key={request.id}
              className="border-l-4 border-l-red-500 hover:shadow-lg transition-shadow"
            >
              <CardHeader>
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div>
                    <CardTitle className="text-xl text-foreground">
                      {request.title}
                    </CardTitle>
                    <CardDescription className="text-base mt-2">
                      {request.description}
                    </CardDescription>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Badge
                      className={
                        urgencyColors[request.urgency] || urgencyColors.default
                      }
                    >
                      {urgencyLabels[request.urgency] ||
                        urgencyLabels.default}
                    </Badge>
                    <Badge
                      variant="outline"
                      className="border-primary text-primary"
                    >
                      {request.bloodType}
                    </Badge>
                    <Badge
                      variant="outline"
                      className="border-orange-500 text-orange-600"
                    >
                      <Clock className="mr-1" size={14} />
                      {getTimeRemaining(request.expiryTime)}
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="flex items-center gap-2">
                    <User className="text-muted-foreground" size={16} />
                    <span className="text-sm text-muted-foreground">
                      <strong>Requester:</strong> {request.requesterName}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="text-muted-foreground" size={16} />
                    <span className="text-sm text-muted-foreground">
                      <strong>Location:</strong> {request.location}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">
                      <strong>Hospital:</strong> {request.hospital}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">
                      <strong>Phone:</strong> {request.requesterPhone}
                    </span>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="mt-6 flex flex-col sm:flex-row gap-3">
                  <Button
                    className="bg-red-600 hover:bg-red-700"
                    onClick={() =>
                      window.open(`tel:${request.requesterPhone}`)
                    }
                  >
                    Call Requester
                  </Button>

                  <ShareButton request={request} />

                  <Button
                    variant="outline"
                    onClick={() =>
                      window.open(
                        `https://maps.google.com/?q=${encodeURIComponent(
                          request.hospital + ", " + request.location
                        )}`,
                        "_blank"
                      )
                    }
                  >
                    View on Map
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EmergencyRequests;

