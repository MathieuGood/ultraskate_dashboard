# API FastAPI - UltraskateDashboard

Une API asynchrone pour accéder aux données des événements Ultraskate.

## Démarrage

```bash
# Démarrer le serveur en mode développement (pré-chargement automatique des événements)
uv run uvicorn api.app:app --reload

# Alternative : utiliser le script helper qui charge d'abord les événements puis démarre uvicorn
uv run python run_api.py

# Le serveur sera accessible à http://localhost:8000
```

Note: l'application FastAPI exécute désormais `load_events()` lors de l'événement `startup`,
donc lancer `uv run uvicorn api.app:app --reload` pré-charge automatiquement les événements depuis
`scraped_events_save/` pour que les routes retournent des données immédiatement.

## Documentation Interactive

Une fois le serveur lancé, accédez à:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## Endpoints

### Health Check

#### GET `/`

Vérifier l'état de l'API.

**Response:**

```json
{
  "message": "UltraskateDashboard API",
  "version": "0.1.0",
  "status": "online"
}
```

#### GET `/health`

Health check simple.

**Response:**

```json
{
  "status": "healthy"
}
```

### Events

#### GET `/events/`

Récupère la liste de tous les événements.

**Response:**

```json
{
  "count": 13,
  "events": [
    {
      "date": "2013-01-07",
      "track": {
        "name": "Homestead Speedway",
        "city": "Homestead",
        "country": "USA",
        "length_miles": 1.46
      },
      "performances_count": 150
    }
  ]
}
```

#### GET `/events/{year}`

Récupère les détails d'un événement pour une année spécifique.

**Parameters:**

- `year` (int): L'année de l'événement (ex: 2023)

**Response:**

```json
{
  "date": "2023-01-07",
  "track": {
    "name": "Homestead Speedway",
    "city": "Homestead",
    "country": "USA",
    "length_miles": 1.46
  },
  "total_participants": 150,
  "performances": [
    {
      "athlete": {
        "name": "John Doe",
        "gender": "M",
        "city": "Miami",
        "state": "FL",
        "country": "USA"
      },
      "category": "Skateboard",
      "age_group": "Open",
      "sport": "Skateboard",
      "total_miles": 145.8,
      "total_laps": 100,
      "total_time": "24:15:30",
      "average_speed_kph": 6.02
    }
  ]
}
```

### Performances

#### GET `/performances/year/{year}`

Récupère toutes les performances d'une année.

**Parameters:**

- `year` (int): L'année (ex: 2023)

**Response:** Voir exemple ci-dessus

#### GET `/performances/year/{year}/sport/{sport}`

Récupère les performances filtrées par sport.

**Parameters:**

- `year` (int): L'année
- `sport` (str): Type de sport (Skateboard, Inline Skating, Paddle, etc.)

**Response:**

```json
{
  "year": 2023,
  "sport": "Skateboard",
  "count": 80,
  "performances": [...]
}
```

#### GET `/performances/year/{year}/top/{n}`

Récupère les top N meilleures performances d'une année.

**Parameters:**

- `year` (int): L'année
- `n` (int): Nombre de top performances (default: 10)

**Response:**

```json
{
  "year": 2023,
  "top_count": 10,
  "performances": [
    {
      "position": 1,
      "athlete": {...},
      "total_miles": 145.8,
      ...
    }
  ]
}
```

## Architecture

```
api/
├── __init__.py
├── app.py              # Configuration FastAPI et middleware
├── main.py             # Entry point du serveur
└── routes/
    ├── __init__.py
    ├── events.py       # Routes pour les événements
    └── performances.py # Routes pour les performances
```
