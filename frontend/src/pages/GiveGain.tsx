import { useState } from "react";

const benefitsBlood = [
  "Free Health Screening – mini checkup, early detection of issues",
  "Donor Credit Card / Blood Replacement (UP & WB)",
  "Refreshments & Allowances (snacks, juice, etc.)",
  "Recognition & Awards (certificates, medals, milestones)",
  "Special Leave / Social Benefits (paid leave in PSUs/companies)"
];

const benefitsMoney = [
  "80G Income Tax Deduction (50%/100%) under old regime",
  "100% Deduction for Govt. Funds (NBTC, PM Relief Fund, etc.)",
  "CSR Recognition for Companies (CSR Act compliance)",
  "Form 10BE & Valid Receipts ensure transparency",
  "Double Advantage: 80G Tax + CSR credit for businesses"
];

export default function GiveGain() {
  const [hover, setHover] = useState<string | null>(null);

  return (
    <section className="min-h-screen bg-white flex flex-col items-center pt-28 pb-16 px-6">
      {/* Heading */}
      <h1 className="text-4xl md:text-5xl font-bold text-center mb-14 text-red-600">
        Give & Gain: <span className="text-gray-800">Benefits of Donating</span>
      </h1>

      {/* Cards Grid */}
      <div className="grid md:grid-cols-2 gap-10 max-w-6xl w-full">
        
        {/* Blood Donors */}
        <div
          onMouseEnter={() => setHover("blood")}
          onMouseLeave={() => setHover(null)}
          className={`p-8 rounded-2xl shadow-md border transition-transform duration-300 cursor-pointer hover:shadow-xl ${
            hover === "blood"
              ? "bg-red-50 scale-105 border-red-500"
              : "bg-white border-gray-200"
          }`}
        >
          <h2 className="text-2xl font-semibold mb-6 text-red-700 flex items-center">
            🩸 Top 5 Benefits for Blood Donors
          </h2>
          <ul className="list-disc ml-6 space-y-3 text-gray-700 leading-relaxed">
            {benefitsBlood.map((b, i) => (
              <li key={i}>{b}</li>
            ))}
          </ul>
        </div>

        {/* Monetary Donors */}
        <div
          onMouseEnter={() => setHover("money")}
          onMouseLeave={() => setHover(null)}
          className={`p-8 rounded-2xl shadow-md border transition-transform duration-300 cursor-pointer hover:shadow-xl ${
            hover === "money"
              ? "bg-pink-50 scale-105 border-pink-500"
              : "bg-white border-gray-200"
          }`}
        >
          <h2 className="text-2xl font-semibold mb-6 text-pink-700 flex items-center">
            ❤️ Top 5 Benefits for Monetary Donors
          </h2>
          <ul className="list-disc ml-6 space-y-3 text-gray-700 leading-relaxed">
            {benefitsMoney.map((b, i) => (
              <li key={i}>{b}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
