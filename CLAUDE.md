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
│       ├── pages/        # Route-level page components (Home, EventGrid, EventGraph, AthletesGrid)
│       ├── router/       # Vue Router configuration
│       ├── fetch/        # API client functions
│       ├── utils/        # Shared utilities (eventSlug)
│       └── css/          # Global styles (Tailwind imports)
├── backend/           # Python FastAPI application
│   ├── api/              # FastAPI app setup, routes, and data loader
│   │   └── routes/       # Endpoint definitions (base, events, performances, athletes)
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
| Charts | Apache ECharts via vue-echarts |
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
| GET | `/events` | List all events (metadata only, no performances) |
| GET | `/events/{city}/{year}` | Get event by city and year (with performances, no laps) |
| GET | `/events/{city}/{year}/graph` | Get ECharts-ready graph data (cumulative miles over time) |
| GET | `/events/by-city/{city}` | Get all events for a city |
| GET | `/events/{year}` | Get event by year (legacy) |
| GET | `/athletes` | All athletes with aggregated career stats |
| GET | `/athletes/{name}` | Single athlete with per-event performance breakdown |
| GET | `/performances/year/{year}` | All performances for a year |
| GET | `/performances/year/{year}/sport/{sport}` | Performances filtered by sport |
| GET | `/performances/year/{year}/top/{n}` | Top N performers by distance |

## Frontend Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Home.vue | Welcome page with navigation links |
| `/event` | EventGrid.vue | DataTable view of performances with multi-event selection and sport filter |
| `/athletes` | AthletesGrid.vue | DataTable of all athletes with aggregated career stats, search, sport/gender filters. Row-click navigates to detail. |
| `/athletes/:name` | AthleteDetail.vue | Single athlete profile with info, career totals, and per-event performance DataTable |
| `/event/graph` | EventGraph.vue | ECharts line chart with metric toggle (distance/speed), unit toggle (mi/km), and athlete selection panel |

### Multi-event selection pattern

Both EventGrid and EventGraph use the same selection pattern:
- **URL**: Query params like `/event?event=homestead_2024&event=homestead_2023`
- **Slug**: Frontend-only convention (`city_year`) derived via `toSlug()` from `utils/eventSlug.ts` — not stored in backend models
- **Dropdown**: PrimeVue MultiSelect with chip display
- **Sport filter**: PrimeVue SelectButton (Skateboard/Inline/Quad), disabled options based on available sports
- **Metric toggle** (graph only): SelectButton to switch between "Total distance" and "Average speed"
- **Unit toggle** (graph only): SelectButton to switch between imperial (mi/mph) and metric (km/km·h)
- **Default**: Redirects to most recent event if no query params

## Code Conventions

### Frontend

- **Component style**: Vue 3 Composition API with `<script setup lang="ts">`
- **File naming**: PascalCase for components and pages (`Header.vue`, `EventGrid.vue`)
- **Import aliases**: Use `@/` to reference `frontend/src/` (e.g., `import { fetchEventByCityYear } from '@/fetch/fetchEvents'`)
- **State management**: Local component state with `ref()` and `computed()` — no Pinia/Vuex store
- **Formatting** (Prettier):
  - No semicolons
  - Single quotes
  - 4-space indentation
  - 120 character line width
- **UI components**: Use PrimeVue for data tables, selects, buttons, checkboxes. Use Tailwind utility classes for layout and styling.
- **Charts**: Use vue-echarts (`VChart`) with manual ECharts module registration (tree-shaking). Import only needed chart types and components.
- **Theme colors**: Amber/orange primary (`#f59e0b`), Slate secondary. Use PrimeVue design tokens (`text-muted-color`, `border-surface`) over hardcoded Tailwind colors for theme compatibility.
- **PrimeVue components used**: DataTable, Column, MultiSelect, SelectButton, Button, Chip, InputText. Use `autoFilterFocus` on MultiSelect with filter for better UX.

### Backend

- **Import order**: stdlib, then third-party, then local modules
- **Type hints**: Use modern Python syntax (`str | None` not `Optional[str]`)
- **Models**: Classes with `to_dict()` / `from_dict()` serialization methods. `to_dict()` accepts `performances` and `laps` booleans to control output size.
- **Graph data**: `Performance.to_graph_dict()` returns ECharts-ready data with two arrays: `data` (`[hours, miles]`) for distance and `speed_data` (`[hours, avg_mph]`) for speed — backend pre-computes cumulative values so frontend doesn't transform data. Unit conversion (mi→km, mph→kph) is done client-side.
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
5. **Display**: Vue frontend fetches data via API client and renders with PrimeVue DataTable or ECharts

## Key Files

| File | Purpose |
|------|---------|
| `frontend/src/main.ts` | Vue app initialization, PrimeVue theme setup |
| `frontend/src/App.vue` | Root component (Header + router-view) |
| `frontend/src/pages/EventGrid.vue` | DataTable view with multi-event selection |
| `frontend/src/pages/EventGraph.vue` | ECharts line chart with metric/unit toggles and athlete panel |
| `frontend/src/utils/eventSlug.ts` | Shared `toSlug()` utility for event slug generation |
| `frontend/src/router/index.ts` | Route definitions |
| `frontend/src/pages/AthletesGrid.vue` | Athletes DataTable with career stats |
| `frontend/src/pages/AthleteDetail.vue` | Single athlete profile with per-event performances |
| `frontend/src/fetch/fetchAthletes.ts` | API client for athletes endpoint |
| `frontend/src/fetch/fetchEvents.tsx` | API client for event endpoints |
| `backend/api/app.py` | FastAPI app creation, CORS, router mounting |
| `backend/api/loader.py` | Startup data loading from JSON files |
| `backend/api/routes/events.py` | Event API endpoints (list, by city/year, graph) |
| `backend/api/routes/performances.py` | Performance API endpoints |
| `backend/api/routes/athletes.py` | Athletes endpoint with career stat aggregation |
| `backend/models/event.py` | Event data model |
| `backend/models/performance.py` | Performance data model (includes `to_graph_dict()`) |
| `backend/models/event_registry.py` | In-memory event collection with lookup methods |

## Testing

No test infrastructure is currently set up. There are no test files, test runners, or testing dependencies configured for either frontend or backend.

## Future: Live Data Implementation

### Overview

Display real-time race results during a live Ultraskate event by polling MyRaceResult's JSON API and pushing updates to the frontend.

### Architecture (MVP — polling-based)

```
[MyRaceResult API] --poll every 60s--> [FastAPI background task]
                                            |
                                    Update EventRegistry in-memory
                                            |
                                    [Existing API endpoints]
                                            |
                          [Frontend polls /events/{name}/{year} every 60s]
```

### Backend

- **Background task**: `asyncio` task in FastAPI that periodically calls MyRaceResult's participant/lap endpoints during a live event
- **Incremental updates**: detect new laps (compare lap count) and new athletes (new participants appearing mid-race), append to existing `Event` in `EventRegistry` in-place
- **Live event detection**: needs a mechanism to mark an event as "live" (manual flag, date-based, or API trigger)
- **Scraper reuse**: `event_scraper.__fetch_participant_performance()` already fetches per-athlete lap data — call it repeatedly in the polling loop

### Frontend

- Reuse EventGrid/EventGraph with auto-refresh (`setInterval` calling existing fetch functions)
- Visual indicator for "live" status
- Consider: auto-scroll, position change notifications

### Upgrade path

- **Phase 1**: Frontend polling + backend background task (simplest, no new infra)
- **Phase 2**: WebSockets or SSE for backend → frontend push (better UX, no wasted requests)
- FastAPI supports both WebSockets and SSE natively

### Key considerations

- MyRaceResult has no webhooks — polling is the only option
- Current scraper builds full `Event` objects from scratch — live mode needs incremental lap appending
- In-memory update (EventRegistry) is the natural fit; no need to write/reload JSON during live events
- Poll interval: 30-60 seconds is reasonable to avoid rate-limiting

## Notes

- CORS: currently wide open (`allow_origins=["*"]`). To lock down for production, use env var in `app.py`:
  ```python
  import os
  origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
  app.add_middleware(CORSMiddleware, allow_origins=origins, ...)
  ```
  Then set `ALLOWED_ORIGINS=https://yourdomain.com` in production.
- The frontend API URL is hardcoded, not environment-configurable
- Node.js version requirement: `^20.19.0 || >=22.12.0`
- The backend uses `uv` (not pip) for Python package management; lockfile is `uv.lock`
- Development runs via Docker Compose with volume mounts for hot-reloading
