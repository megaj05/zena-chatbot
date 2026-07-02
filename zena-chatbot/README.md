# ZeNA AI Assistant — ZeAI Soft Chatbot Widget

A production-ready, embeddable chatbot widget for the ZeAI Soft website.

- **Frontend:** React + Vite, pure CSS, Axios
- **Backend:** Python Flask + Flask-CORS + SQLite

It implements the full conversation flow: main menu → Explore Services,
Training Programs, Business Collaboration, and Other Enquiries (with
keyword-based NLP fallback), lead capture forms, and a "stay connected"
social-link prompt — all themed in ZeAI Soft's purple brand colors.

---

## 1. Project Structure

```
zena-chatbot/
├── backend/
│   ├── app.py                 # Flask app entry point
│   ├── chatbot_data.py        # All conversation copy: menus, services, programs, NLP keywords
│   ├── requirements.txt
│   ├── database/
│   │   └── db.py              # SQLite connection + schema (users, chat_history, session_requests)
│   ├── models/
│   │   └── lead.py            # CRUD helpers for leads & session requests
│   └── routes/
│       └── chat.py            # /api/chat, /api/lead, /api/history — the flow engine
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx                    # Placeholder host page + <ChatWidget />
        ├── main.jsx
        ├── components/
        │   ├── ChatWidget.jsx          # Floating button + state machine + window
        │   ├── ChatHeader.jsx          # Logo, title, minimize/close icons
        │   ├── ChatMessages.jsx        # Scrollable transcript + typing indicator
        │   ├── MessageBubble.jsx       # Single bot/user bubble (+ link buttons)
        │   ├── QuickReplies.jsx        # Pill-shaped quick-reply buttons
        │   └── UserForm.jsx            # Lead / Collaboration / Session form
        ├── services/
        │   └── api.js                  # Axios calls to the Flask backend
        └── styles/
            └── chatbot.css              # All widget + theme styling
```

---

## 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The server starts at **http://localhost:5000**. On first run it creates
`backend/database/zena.db` automatically with three tables:

| Table              | Purpose                                            |
|---------------------|----------------------------------------------------|
| `users`             | Leads from Explore Services & Business Collaboration |
| `chat_history`      | Every message/response pair                        |
| `session_requests`  | "Connect with Kirthika" booking requests            |

### API Endpoints

| Method | Endpoint        | Description                                            |
|--------|------------------|---------------------------------------------------------|
| POST   | `/api/chat`      | Drives the conversation. Body: `{ node, type, value }` |
| POST   | `/api/lead`      | Submits a lead/collaboration/session form               |
| GET    | `/api/history`   | Returns recent chat history (`?limit=50`)                |

---

## 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The widget runs at **http://localhost:5173** and talks to the backend
at `http://localhost:5000/api` by default.

To point at a different backend URL (e.g. in production), create a
`.env` file in `frontend/`:

```
VITE_API_URL=https://your-api-domain.com/api
```

### Build for production

```bash
npm run build
```

Output goes to `frontend/dist/` — deploy it as static files, or copy
just the `ChatWidget` component + `chatbot.css` into your existing
ZeAI Soft website codebase to embed the widget there instead.

---

## 4. Conversation Flow Summary

```
Main Menu
├── Explore Services
│   └── [service] → description → "Discuss requirements?" → Yes → Lead Form → Stay Connected (IG / WhatsApp / LinkedIn)
├── Training Programs
│   ├── ZeAI Skill-Up On Campus → learning area → Lead Form
│   ├── Global Immersion Program → interested? → Lead Form
│   ├── Hackathon 2026 → domains + registration link
│   └── Connect with Kirthika → Book Session / Know More / Career / Startup / Resume / Project Discussions → Session Form
├── Business Collaboration → Collaboration Form → Stay Connected
└── Other Enquiries → free text (keyword NLP: greeting, company info, services,
    internship, careers, contact, technical support) → fallback with quick replies
```

---

## 5. Notes

- All conversational copy lives in `backend/chatbot_data.py` — edit it
  there to change wording without touching any flow logic.
- The logo in the header/launcher is an inline SVG placeholder for the
  ZeNA robot mark; swap it for your real logo asset in
  `ChatHeader.jsx` and `ChatWidget.jsx` whenever you have the artwork.
- CORS is wide open (`origins: "*"`) for local development — restrict
  it to your real domain in `backend/app.py` before deploying.
