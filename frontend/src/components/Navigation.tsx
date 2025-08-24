"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Heart, Home, AlertTriangle, Users, Calendar, MessageCircle, Gift, LifeBuoy } from "lucide-react";
import { Link, useLocation } from "react-router-dom";

import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

const Navigation = () => {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const location = useLocation();
  const active = location.pathname;

  const navItems = [
    { id: "/", icon: <Home size={20} />, label: "Home", path: "/" },
    { id: "/emergency", icon: <AlertTriangle size={20} />, label: "Emergency Requests", path: "/emergency" },
    { id: "/give-gain", icon: <Gift size={20} />, label: "Give & Gain", path: "/give-gain" },
    { id: "/emergency-hub", icon: <LifeBuoy size={20} />, label: "Emergency Hub", path: "/emergency-hub" },
    { id: "/about", icon: <Users size={20} />, label: "About", path: "/about" },
    { id: "/events", icon: <Calendar size={20} />, label: "Events", path: "/events" },
    { id: "/donate", icon: <Heart size={20} />, label: "Donate", path: "/donate" },
    { id: "/contact", icon: <MessageCircle size={20} />, label: "Contact", path: "/contact" },
  ];

  return (
    <>
      <TooltipProvider delayDuration={100}>
        {/* Desktop Horizontal Nav */}
        <nav className="hidden md:flex fixed z-50 top-4 left-1/2 transform -translate-x-1/2 bg-background/80 backdrop-blur-md border border-border/50 shadow-lg p-2 rounded-full space-x-2">
          {navItems.map(({ id, icon, label, path }) => (
            <Tooltip key={id}>
              <TooltipTrigger asChild>
                <Link to={path} onClick={() => setIsMobileOpen(false)}>
                  <Button
                    variant={active === path ? "default" : "ghost"}
                    size="icon"
                    aria-label={label}
                    className="rounded-full hover:bg-primary/10"
                  >
                    {icon}
                  </Button>
                </Link>
              </TooltipTrigger>
              <TooltipContent side="bottom" className="animate-[slideFade_0.2s_ease-out]">
                {label}
              </TooltipContent>
            </Tooltip>
          ))}
        </nav>
      </TooltipProvider>

      {/* Mobile Hamburger Button */}
      <button
        onClick={() => setIsMobileOpen(!isMobileOpen)}
        className="md:hidden fixed top-4 left-4 z-50 p-2 rounded-md bg-background/80 backdrop-blur-md border shadow-md"
        aria-label="Toggle navigation"
      >
        ☰
      </button>

      {/* Mobile Sidebar */}
      <nav
        className={`fixed top-0 left-0 h-full w-56 z-40 bg-background/95 backdrop-blur-md border-r border-border/50 shadow-lg transform transition-transform duration-300 md:hidden
        ${isMobileOpen ? "translate-x-0" : "-translate-x-full"}`}
      >
        <div className="flex flex-col items-center mt-16 space-y-6">
          {navItems.map(({ id, icon, label, path }) => (
            <Link
              key={id}
              to={path}
              onClick={() => { setIsMobileOpen(false); }}
            >
              <Button
                variant={active === path ? "default" : "ghost"}
                size="sm"
                aria-label={label}
                className="rounded-full hover:bg-primary/10 flex items-center gap-2"
              >
                {icon}
                <span>{label}</span>
              </Button>
            </Link>
          ))}
        </div>
      </nav>

      <main className="md:pt-16 max-md:pb-5"></main>

      {/* Tailwind keyframes */}
      <style>{`
        @keyframes slideFade {
          0% { opacity: 0; transform: translateX(-4px); }
          100% { opacity: 1; transform: translateX(0); }
        }
      `}</style>
    </>
  );
};

export default Navigation;
