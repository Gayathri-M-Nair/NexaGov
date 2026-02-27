# SahAI - Government Schemes Portal

A modern government schemes discovery portal built using **Vite + React + TypeScript + Tailwind CSS**.

This project allows users to:
- Browse government schemes
- Filter by category
- View scheme details
- Follow structured application roadmaps
- (Future) Check eligibility and track applications

---

## 🚀 Tech Stack

- ⚡ Vite
- ⚛️ React (TypeScript)
- 🎨 Tailwind CSS
- 🔀 React Router DOM

---

## 📁 Project Structure

```
src/
│
├── assets/          # Static assets
├── components/      # Reusable UI components
│   ├── layout/      # Navbar, footer, layout wrappers
│   ├── portal/      # Scheme-related components
│   └── ui/          # Buttons, inputs, cards, etc.
│
├── constants/       # Static configuration data
├── hooks/           # Custom React hooks
├── lib/             # Utility functions
│
├── pages/           # Route-based pages
│   ├── Home.tsx
│   ├── Login.tsx
│   ├── Profile.tsx
│
├── styles/          # Global styles
├── App.tsx          # Routing configuration
└── main.tsx         # App entry point
```

---

## 🛠 Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd nexagov
```

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

Open:

```
http://localhost:5173
```

---

## 🌐 Routing

Routing is handled using `react-router-dom`.

Example routes:

- `/` → Login
- `/home` → Home page
- `/profile` → User profile
- `/scheme/:id` → Scheme detail page

---

## 🎯 Current Features

- Responsive Login UI
- Hero Section
- Category-based scheme browsing
- Clean Navbar layout
- Structured scheme cards
- Tailwind-based design system

---

## 🔮 Upcoming Features

- Eligibility engine
- Application tracking system
- Backend API integration
- Authentication
- Admin dashboard
- Multilingual support

---

## 📌 Future Backend Plan

This frontend can be connected to:

- Node + Express API
- Next.js API routes
- Python (FastAPI)
- Government open data APIs

---

## 👩‍💻 Development Notes

- Built for hackathon-level scalability.
- Designed to be modular and extensible.
- Components are reusable and structured for large-scale growth.

---

## 📜 License

MIT License
