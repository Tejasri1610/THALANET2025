import { useState } from "react";

type Request = {
  id: number;
  category: string;
  description: string;
  location: string;
  phone: string;
  urgency: string;
};

export default function EmergencyHub() {
  const [requests, setRequests] = useState<Request[]>([]);
  const [form, setForm] = useState<Request>({
    id: 0,
    category: "",
    description: "",
    location: "",
    phone: "",
    urgency: "Normal",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const maskPhone = (phone: string) => {
    if (phone.length <= 5) return "****";
    return phone.slice(0, 3) + "*****" + phone.slice(-2);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setRequests([...requests, { ...form, id: Date.now() }]);
    setForm({
      id: 0,
      category: "",
      description: "",
      location: "",
      phone: "",
      urgency: "Normal",
    });
  };

  const urgencyColor = (urgency: string) => {
    switch (urgency) {
      case "Critical":
        return "text-red-600";
      case "Urgent":
        return "text-yellow-600";
      default:
        return "text-green-600";
    }
  };

  return (
    <section className="min-h-screen bg-white px-6 flex flex-col items-center pt-24">
      {/* Heading */}
      <h1 className="text-4xl font-bold text-red-600 mb-4">🚨 Emergency Hub</h1>
      <p className="text-gray-600 text-center max-w-2xl mb-10">
        In moments of crisis, help should be simple, fast, and reliable. Submit your
        urgent request and our team will connect you with the right support.
      </p>

      {/* Form */}
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-xl bg-gray-50 p-6 rounded-2xl shadow-md"
      >
        <label className="block mb-2 font-semibold">Select Category</label>
        <select
          name="category"
          value={form.category}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-4 focus:ring-2 focus:ring-red-500 outline-none"
          required
        >
          <option value="">-- Select --</option>
          <option value="Mental Health">🧠 Mental Health</option>
          <option value="Medical Help">🏥 Medical Help</option>
          <option value="Legal Aid">⚖️ Legal Aid</option>
          <option value="Other">📌 Other</option>
        </select>

        <label className="block mb-2 font-semibold">Describe Your Need</label>
        <textarea
          name="description"
          value={form.description}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-4 focus:ring-2 focus:ring-red-500 outline-none"
          placeholder="Explain your urgent need..."
          required
        />

        <label className="block mb-2 font-semibold">Location</label>
        <input
          type="text"
          name="location"
          value={form.location}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-4 focus:ring-2 focus:ring-red-500 outline-none"
          placeholder="City, State"
          required
        />

        <label className="block mb-2 font-semibold">Phone Number</label>
        <input
          type="tel"
          name="phone"
          value={form.phone}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-4 focus:ring-2 focus:ring-red-500 outline-none"
          placeholder="Enter phone number"
          required
        />

        <label className="block mb-2 font-semibold">Urgency</label>
        <select
          name="urgency"
          value={form.urgency}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-6 focus:ring-2 focus:ring-red-500 outline-none"
        >
          <option>Normal</option>
          <option>Urgent</option>
          <option>Critical</option>
        </select>

        <button
          type="submit"
          className="w-full bg-red-600 text-white py-3 rounded-xl font-semibold hover:bg-red-700 transition"
        >
          Post Request
        </button>
      </form>

      {/* Requests List */}
      <div className="w-full max-w-4xl mt-12 space-y-6">
        {requests.map((req) => (
          <div
            key={req.id}
            className="border rounded-2xl shadow-sm p-6 bg-white flex flex-col gap-2 hover:shadow-md transition"
          >
            <h2
              className={`text-xl font-bold ${urgencyColor(
                req.urgency
              )} flex items-center gap-2`}
            >
              {req.urgency === "Critical" && "⚠️"}
              {req.urgency === "Urgent" && "⏳"}
              {req.urgency === "Normal" && "✅"} {req.urgency} - {req.category}
            </h2>
            <p className="text-gray-700">{req.description}</p>
            <p>
              📍 <span className="font-semibold">Location:</span> {req.location}
            </p>
            <p>
              📞 <span className="font-semibold">Phone:</span> {maskPhone(req.phone)}
            </p>
            <div className="flex gap-3 mt-3">
              <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition">
                Contact via Org
              </button>
              <button className="bg-gray-100 px-4 py-2 rounded-lg hover:bg-gray-200 transition">
                Share
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
