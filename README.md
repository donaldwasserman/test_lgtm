# GeoEvents

A creative, horizontally complex full-stack event discovery platform built for testing GitHub Actions plugins.

## Tech Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, React Router, TanStack Query, Zustand
- **Backend**: FastAPI, SQLAlchemy (async), Pydantic v2, Alembic, JWT auth
- **Database**: PostgreSQL 16
- **Containerization**: Docker, Docker Compose

## Features (Horizontal Complexity)

- 🔐 Authentication (JWT, role-based: attendee, organizer, moderator, admin)
- 👥 User profiles & management
- 🎉 Event creation, management, and discovery
- 🏛️ Venues with location data
- 🏷️ Categories and tags
- ✅ RSVP system (attending/maybe/not attending)
- ⭐ Reviews & ratings
- 🔔 Notifications
- 💝 Wishlist functionality
- 🏆 Badge system
- 📧 Invitations
- 📊 Organizer dashboard with analytics
- 🔍 Search & filtering
- ✨ Featured events

## Getting Started

### Prerequisites
- Docker and Docker Compose installed

### Running with Docker Compose

```bash
cd geoevents
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc

## Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Testing GitHub Actions

This app is designed as a test harness for GitHub Actions plugins. Create workflows in `.github/workflows/` to test your plugin's functionality.
