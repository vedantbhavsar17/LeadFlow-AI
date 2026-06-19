# LeadFlow Frontend 🎨

The frontend interface for LeadFlow AI is built using **Next.js 15**, **React 19**, **TypeScript**, and **Tailwind CSS v4**. It features a modern, responsive layout conforming to the *Modern Corporate with Glassmorphic Accents* design system.

---

## 🛠️ Frontend Tech Stack

* **Core**: Next.js 15 (App Router), React 19, TypeScript
* **Styling**: Tailwind CSS v4 (configured via `@import "tailwindcss";` and CSS `@theme` declarations)
* **Data Charts**: Recharts (PieChart, AreaChart, LineChart)
* **Icons**: Lucide React
* **Type Safety**: Full TypeScript compiler type checking enabled (`npm run typecheck`)

---

## 📂 Routes & Folder Structure

The application routes are divided into two main groups using Next.js route groups:

### 1. Marketing Routes `(marketing)/`
* **`/` (Landing Page)**: Main promotional page showcasing value propositions, interactive storytelling, and a modal walkthrough overlay. Uses `landing.css`.
* **`/pricing` (Pricing Page)**: Plan selector page with an annual/monthly billing toggle and pricing FAQ accordion cards.

### 2. Application Core Routes `(app)/`
* **`/dashboard` (Dashboard)**: Core metrics display (Total Leads, Qualified Leads, Conversations, and Conversion Rate sparklines), the horizontal Lead Pipeline chevron step visualizer, Recent Activity panel, Top Channels pie chart, and AI Insights area chart card.
* **`/leads` (Leads Repository)**: Full database table listing current leads, featuring text query search, HOT/WARM/COLD status filters, and a CSV import dialog with uploader.
* **`/pipeline` (Kanban Board)**: Drag-and-drop or button-triggered Kanban matrix representing deal movement from Raw Leads, Qualified, Engaged, to Converted stages.
* **`/settings` (Configuration)**: Forms for defining the AI representative identity (name, outreach style, cadence) and storing encrypted API keys for HubSpot, Salesforce, and OpenAI.

---

## 🚀 How to Run Locally

### 1. Install Dependencies
Open your terminal inside the `frontend` directory and run:
```bash
npm install
```

### 2. Run the Development Server
```bash
npm run dev
```
This runs the local development server on:
```text
http://localhost:3000
```

### 3. Verify Types & Build
Before deploying or committing, you can verify that the code passes TypeScript checks and compiles correctly:
```bash
npm run typecheck
npm run build
```

---

## 🧪 Testing with TestSprite
Integration and browser end-to-end tests are housed in the `testsprite_tests` directory.

To run automated browser tests, first ensure the local server is running on `http://localhost:3000`, then execute the test scripts under `frontend/testsprite_tests`:
```bash
cd testsprite_tests
python TC001_Visit_landing_page_and_enter_the_app.py
```
Test results, logs, and coverage reports are outputted to the `frontend/testsprite_tests/tmp/` folder.
