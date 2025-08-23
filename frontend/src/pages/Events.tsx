"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

const initialEvents = [
  {
    title: "Blood Warriors x Café Awareness Drive",
    date: "Sep 05, 2025",
    time: "10:00 AM",
    location: "Bengaluru, India",
    img: "/images/event1.jpg",
  },
  {
    title: "Thalassemia Screening Camp",
    date: "Sep 12, 2025",
    time: "9:00 AM",
    location: "Hyderabad, India",
    img: "/images/event2.jpg",
  },
  {
    title: "Blood Donation Marathon",
    date: "Oct 01, 2025",
    time: "8:00 AM",
    location: "Mumbai, India",
    img: "/images/event3.jpg",
  },
  {
    title: "Youth Talk on Thalassemia",
    date: "Oct 15, 2025",
    time: "5:00 PM",
    location: "Delhi, India",
    img: "/images/event4.jpg",
  },
  {
    title: "Fundraising Gala Night",
    date: "Nov 10, 2025",
    time: "7:00 PM",
    location: "Chennai, India",
    img: "/images/event5.jpg",
  },
];

export default function Events() {
  const [events, setEvents] = useState(initialEvents);
  const [newEvent, setNewEvent] = useState({
    title: "",
    date: "",
    time: "",
    location: "",
    img: "",
  });

  // Track registration state per event
  const [selectedEvent, setSelectedEvent] = useState<any>(null);
  const [formData, setFormData] = useState({ name: "", email: "", phone: "" });
  const [registeredEvents, setRegisteredEvents] = useState<string[]>([]);

  const handleShare = (event: typeof events[0]) => {
    const text = `📢 Join me at "${event.title}" on ${event.date} at ${event.location}! Let's make a difference together ❤️`;
    window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, "_blank");
  };

  const handleAddEvent = () => {
    if (!newEvent.title || !newEvent.date || !newEvent.time || !newEvent.location) {
      alert("Please fill all required fields");
      return;
    }
    setEvents([...events, newEvent]);
    setNewEvent({ title: "", date: "", time: "", location: "", img: "" });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedEvent) {
      setRegisteredEvents([...registeredEvents, selectedEvent.title]);
    }
    // Clear form
    setFormData({ name: "", email: "", phone: "" });
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-6 pt-20 pb-12 space-y-12">
        {/* Page Header */}
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            Thalassemia <span className="text-primary">Events</span>
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Join us in spreading awareness, supporting patients, and saving
            lives through our impactful events.
          </p>
        </div>

        {/* Host Event Button */}
        <div className="flex justify-center">
          <Dialog>
            <Button className="bg-primary hover:bg-primary/90 text-white px-6 py-2 rounded-xl shadow-md">
              Host an Event
            </Button>
            <DialogContent>
              <DialogHeader>
                <DialogTitle className="text-2xl font-semibold text-primary">
                  Host a New Event
                </DialogTitle>
              </DialogHeader>
              <div className="space-y-4 mt-4">
                <div>
                  <Label>Title</Label>
                  <Input
                    value={newEvent.title}
                    onChange={(e) =>
                      setNewEvent({ ...newEvent, title: e.target.value })
                    }
                    placeholder="Event title"
                  />
                </div>
                <div>
                  <Label>Date</Label>
                  <Input
                    type="date"
                    value={newEvent.date}
                    onChange={(e) =>
                      setNewEvent({ ...newEvent, date: e.target.value })
                    }
                  />
                </div>
                <div>
                  <Label>Time</Label>
                  <Input
                    type="time"
                    value={newEvent.time}
                    onChange={(e) =>
                      setNewEvent({ ...newEvent, time: e.target.value })
                    }
                  />
                </div>
                <div>
                  <Label>Location</Label>
                  <Input
                    value={newEvent.location}
                    onChange={(e) =>
                      setNewEvent({ ...newEvent, location: e.target.value })
                    }
                    placeholder="City, Country"
                  />
                </div>
                <div>
                  <Label>Image URL (optional)</Label>
                  <Input
                    value={newEvent.img}
                    onChange={(e) =>
                      setNewEvent({ ...newEvent, img: e.target.value })
                    }
                    placeholder="https://example.com/image.jpg"
                  />
                </div>
                <Button
                  onClick={handleAddEvent}
                  className="bg-green-600 hover:bg-green-700 text-white"
                >
                  Add Event
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/* Events Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {events.map((event, idx) => (
            <Card
              key={idx}
              className="overflow-hidden border hover:shadow-lg transition-all duration-300 rounded-2xl"
            >
              <img
                src={event.img || "/images/default-event.jpg"}
                alt={event.title}
                className="w-full h-48 object-cover"
              />
              <CardContent className="p-6">
                <h2 className="text-xl font-semibold text-foreground mb-2">
                  {event.title}
                </h2>
                <p className="text-sm text-muted-foreground mb-1">
                  📅 {event.date} • 🕒 {event.time}
                </p>
                <p className="text-sm text-muted-foreground mb-4">
                  📍 {event.location}
                </p>
                <div className="flex flex-wrap gap-3">
                  <Dialog
                    open={selectedEvent?.title === event.title}
                    onOpenChange={(open) =>
                      setSelectedEvent(open ? event : null)
                    }
                  >
                    <Button
                      className="bg-primary hover:bg-primary/90 text-white rounded-lg"
                      onClick={() => setSelectedEvent(event)}
                    >
                      Register
                    </Button>
                    <DialogContent>
                      {registeredEvents.includes(event.title) ? (
                        <div className="text-center py-6">
                          <h3 className="text-lg font-semibold text-green-600">
                            ✅ Successfully Registered!
                          </h3>
                          <p className="text-gray-600 mt-2">
                            You have registered for {event.title}.
                          </p>
                        </div>
                      ) : (
                        <>
                          <DialogHeader>
                            <DialogTitle className="text-lg font-semibold">
                              Register for {event.title}
                            </DialogTitle>
                          </DialogHeader>
                          <form
                            onSubmit={handleSubmit}
                            className="space-y-4 mt-4"
                          >
                            <div>
                              <Label>Your Name</Label>
                              <Input
                                value={formData.name}
                                onChange={(e) =>
                                  setFormData({
                                    ...formData,
                                    name: e.target.value,
                                  })
                                }
                                placeholder="Enter your name"
                                required
                              />
                            </div>
                            <div>
                              <Label>Your Email</Label>
                              <Input
                                type="email"
                                value={formData.email}
                                onChange={(e) =>
                                  setFormData({
                                    ...formData,
                                    email: e.target.value,
                                  })
                                }
                                placeholder="Enter your email"
                                required
                              />
                            </div>
                            <div>
                              <Label>Your Phone</Label>
                              <Input
                                type="tel"
                                value={formData.phone}
                                onChange={(e) =>
                                  setFormData({
                                    ...formData,
                                    phone: e.target.value,
                                  })
                                }
                                placeholder="Enter your phone"
                                required
                              />
                            </div>
                            <div className="flex justify-end gap-3">
                              <Button
                                type="button"
                                variant="outline"
                                onClick={() => setSelectedEvent(null)}
                              >
                                Cancel
                              </Button>
                              <Button
                                type="submit"
                                className="bg-primary text-white"
                              >
                                Submit
                              </Button>
                            </div>
                          </form>
                        </>
                      )}
                    </DialogContent>
                  </Dialog>
                  <Button
                    variant="outline"
                    onClick={() => handleShare(event)}
                    className="rounded-lg"
                  >
                    Share
                  </Button>
                  <Button className="bg-red-600 hover:bg-red-700 text-white rounded-lg">
                    Donate
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
