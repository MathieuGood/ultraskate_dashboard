# CLAUDE.md

Guide for AI assistants working on the UltraskateDashboard codebase.

## Project Overview

Full-stack dashboard for Ultraskate skateboarding race events. Displays event performance data (athletes, laps, distances, times) scraped from race result websites. The frontend is a Vue 3 SPA that consumes a FastAPI REST API backed by in-memory JSON data.

## Architecture

```
UltraskateDashboard/
├── frontend/          # Vue 3 + Vite + TypeScript SPA
│   └── src/
│       ├── components/   # Reusable Vue components (Header.vue)
│       ├── pages/        # Route-level page components (Home, Event, Athlete)
│       ├── router/       # Vue Router configuration
│       ├── fetch/        # API client functions
│       └── css/          # Global styles (Tailwind imports)
├── backend/           # Python FastAPI application
│   ├── api/              # FastAPI app setup, routes, and data loader
│   │   └── routes/       # Endpoint definitions (base, events, performances)
│   ├── models/           # Data models (Event, Athlete, Performance, Track, etc.)
│   ├── webscraper/       # Playwright + BeautifulSoup scrapers
│   └── scraped_events_save/  # JSON data files (loaded at API startup)
├── Dockerfile.frontend
├── Dockerfile.backend
└── docker-compose.yml
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend framework | Vue 3.5 (Composition API with `<script setup>`) |
| Build tool | Vite 7 |
| Language | TypeScript ~5.9 |
| CSS | Tailwind CSS 4 |
| UI components | PrimeVue 4 (MidnightAmber theme) |
| Routing | Vue Router 4 (history mode) |
| Backend framework | FastAPI 0.128+ |
| Python version | >= 3.13 |
| ASGI server | Uvicorn |
| Scraping | Playwright + BeautifulSoup4 |
| Package managers | npm (frontend), uv (backend) |
| Containerization | Docker + Docker Compose |

## Development Commands

### Frontend (run from `frontend/`)

```bash
npm run dev          # Start Vite dev server (port 5173)
npm run build        # Type-check + production build
npm run build-only   # Production build without type-check
npm run type-check   # Run vue-tsc type checking
npm run format       # Format code with Prettier
npm run preview      # Preview production build
```

### Backend (run from `backend/`)

```bash
uv run uvicorn api.app:app --reload --port 8000   # Start dev server
uv run python scraper.py                           # Run web scraper
uv run python main.py                              # Run standalone data processing
uv sync --frozen                                   # Install dependencies from lockfile
```

### Docker

```bash
docker compose up              # Start both services (frontend: 5173, backend: 8000)
docker compose up --build      # Rebuild and start
docker compose up backend      # Start backend only
docker compose up frontend     # Start frontend only
```

## API Endpoints

Base URL: `http://localhost:8000`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info / health check |
| GET | `/health` | Health status |
| GET | `/events` | List all events (without lap data) |
| GET | `/events/{year}` | Get event by year |
| GET | `/performances/year/{year}` | All performances for a year |
| GET | `/performances/year/{year}/sport/{sport}` | Performances filtered by sport |
| GET | `/performances/year/{year}/top/{n}` | Top N performers by distance |

## Code Conventions

### Frontend

- **Component style**: Vue 3 Composition API with `<script setup lang="ts">`
- **File naming**: PascalCase for components and pages (`Header.vue`, `Event.vue`)
- **Import aliases**: Use `@/` to reference `frontend/src/` (e.g., `import { fetchEventByYear } from '@/fetch/fetchEvents'`)
- **State management**: Local component state with `ref()` and `computed()` — no Pinia/Vuex store
- **Formatting** (Prettier):
  - No semicolons
  - Single quotes
  - 4-space indentation
  - 120 character line width
- **UI components**: Use PrimeVue for data tables, selects, buttons. Use Tailwind utility classes for layout and styling.
- **Theme colors**: Amber/orange primary (`#f59e0b`), Slate secondary, dark backgrounds (`bg-gray-900`)

### Backend

- **Import order**: stdlib, then third-party, then local modules
- **Type hints**: Use modern Python syntax (`str | None` not `Optional[str]`)
- **Models**: Classes with `to_dict()` / `from_dict()` serialization methods
- **Collections**: Registry pattern (`EventRegistry`, `AthleteRegistry`) for in-memory data
- **Route organization**: Separate router files per domain, mounted with prefix (e.g., `/events`, `/performances`)
- **Data loading**: JSON files from `scraped_events_save/` loaded at startup via `api/loader.py` into `EventRegistry`

### API Client (Frontend)

API calls live in `frontend/src/fetch/`. Each file exports async functions that return `Promise<JSON>`. The base URL is hardcoded to `http://localhost:8000/`.

## Data Flow

1. **Scraping**: `backend/webscraper/` uses Playwright to scrape race result websites
2. **Storage**: Scraped data saved as JSON in `backend/scraped_events_save/`
3. **Loading**: On API startup, `api/loader.py` reads all JSON files into `EventRegistry` (in-memory)
4. **Serving**: FastAPI routes serialize `Event`/`Performance` models to JSON responses
5. **Display**: Vue frontend fetches data via API client and renders with PrimeVue DataTable

## Key Files

| File | Purpose |
|------|---------|
| `frontend/src/main.ts` | Vue app initialization, PrimeVue theme setup |
| `frontend/src/App.vue` | Root component (Header + router-view) |
| `frontend/src/pages/Event.vue` | Main data display page with filtering |
| `frontend/src/router/index.ts` | Route definitions |
| `frontend/src/fetch/fetchEvents.tsx` | API client for event endpoints |
| `backend/api/app.py` | FastAPI app creation, CORS, router mounting |
| `backend/api/loader.py` | Startup data loading from JSON files |
| `backend/api/routes/events.py` | Event API endpoints |
| `backend/api/routes/performances.py` | Performance API endpoints |
| `backend/models/event.py` | Event data model |
| `backend/models/performance.py` | Performance data model |
| `backend/models/event_registry.py` | In-memory event collection |

## Testing

No test infrastructure is currently set up. There are no test files, test runners, or testing dependencies configured for either frontend or backend.

## Notes

- The `Athlete.vue` page is a stub — not yet implemented
- CORS is wide open (`allow_origins=["*"]`) — suitable for development only
- The frontend API URL is hardcoded, not environment-configurable
- Node.js version requirement: `^20.19.0 || >=22.12.0`
- The backend uses `uv` (not pip) for Python package management; lockfile is `uv.lock`
