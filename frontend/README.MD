# ThalaNet Emergency Blood Management Platform - Frontend

A modern, responsive web application for emergency blood management, featuring real-time blood requests, donor matching, and AI-powered notifications.

## 🚀 Features

- **Live Emergency Requests:** View and respond to urgent blood requests with real-time updates.
- **Intelligent Donor Matching:** Location and urgency-based recommendations for donors.
- **Share Requests:** Easily share blood requests via WhatsApp, LinkedIn, Instagram, and Twitter.
- **Interactive Map:** Visualize hospital and request locations.
- **Secure Authentication:** Login and registration for donors and hospitals.
- **User Dashboard:** Track donation history, requests, and notifications.
- **Dark/Light Theme Toggle:** Accessible and user-friendly interface.

## 🏗️ Project Structure

```
frontend/
├── public/                  # Static files and images
├── src/
│   ├── assets/              # Images and media
│   ├── components/          # Reusable UI components
│   │   └── ui/              # UI primitives (buttons, cards, etc.)
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utility functions and shared logic
│   ├── pages/               # Main application pages (Home, EmergencyRequests, Profile, etc.)
│   ├── services/            # API service functions
│   ├── App.tsx              # App root component
│   └── main.tsx             # Entry point
├── index.html               # Main HTML file
├── package.json             # Project dependencies and scripts
├── tailwind.config.ts       # Tailwind CSS configuration
├── vite.config.ts           # Vite configuration
└── README.md                # Project documentation
```

## 🛠️ Getting Started

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run the development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

## 🔗 Environment Variables

Create a `.env` file in the root and configure as needed:
```
VITE_API_URL=https://your-backend-api-url
```

## 🧪 Testing

Run unit and integration tests:
```bash
npm run test
```

## 📦 Deployment

See [Azure Static Web Apps](https://docs.microsoft.com/en-us/azure/static-web-apps/) for deployment instructions.

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests.

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

For support or questions,