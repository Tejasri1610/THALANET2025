import Navigation from "@/components/Navigation";
import { ReactNode } from "react";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation */}
      <Navigation />

      {/* Page content - no gap above, full width */}
      <main className="flex-1 m-0 p-0">{children}</main>
    </div>
  );
}
