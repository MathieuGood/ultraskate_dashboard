"""Routes for athlete endpoints"""

from fastapi import APIRouter
from models.athlete_registry import AthleteRegistry
from models.event_registry import EventRegistry

router = APIRouter(prefix="/athletes", tags=["athletes"])


@router.get("/")
async def get_all_athletes():
    """Get all athletes with aggregated career stats across all events."""
    # Build performance stats keyed by canonical_name
    stats: dict[str, dict] = {}
    for event in EventRegistry.events:
        event_key = f"{event.name}_{event.date.year}"
        for perf in event.performances:
            key = perf.athlete.canonical_name
            if key not in stats:
                stats[key] = {
                    "total_miles": 0.0,
                    "best_event_miles": 0.0,
                    "sports": set(),
                    "_events": set(),
                }
            entry = stats[key]
            miles = perf.total_miles()
            entry["total_miles"] += miles
            if miles > entry["best_event_miles"]:
                entry["best_event_miles"] = miles
            entry["sports"].add(perf.sport)
            entry["_events"].add(event_key)

    # Join registry athletes with their computed stats
    result = []
    for athlete in AthleteRegistry.athletes:
        entry = stats.get(athlete.canonical_name, {})
        result.append({
            "name": athlete.name,
            "gender": athlete.gender,
            "city": athlete.city,
            "state": athlete.state,
            "country": athlete.country,
            "team": athlete.team,
            "event_count": len(entry.get("_events", [])),
            "total_miles": round(entry.get("total_miles", 0.0), 2),
            "best_event_miles": round(entry.get("best_event_miles", 0.0), 2),
            "sports": sorted(entry.get("sports", [])),
        })

    result.sort(key=lambda a: a["total_miles"], reverse=True)
    return result


@router.get("/{name}")
async def get_athlete_by_name(name: str):
    """Get a single athlete's info with per-event performance breakdown."""
    athlete = AthleteRegistry.get_by_name(name)
    if athlete is None:
        return {"error": f"Athlete '{name}' not found"}

    performances = []
    events_seen: set[str] = set()
    total_miles = 0.0
    total_km = 0.0

    for event in EventRegistry.events:
        for perf in event.performances:
            if perf.athlete.canonical_name != athlete.canonical_name:
                continue
            miles = perf.total_miles()
            km = perf.total_km()
            total_miles += miles
            total_km += km
            event_key = f"{event.name}_{event.date.year}"
            events_seen.add(event_key)
            performances.append({
                "event_name": event.name,
                "year": event.date.year,
                "date": event.date.isoformat(),
                "sport": perf.sport,
                "category": perf.category,
                "total_laps": perf.total_laps(),
                "total_miles": miles,
                "total_km": km,
                "average_speed_mph": round(perf.average_speed_mph(), 2),
                "average_speed_kph": round(perf.average_speed_kph(), 2),
                "total_time_hhmmss": perf.total_time_hhmmss(),
            })

    performances.sort(key=lambda p: p["date"])

    return {
        "name": athlete.name,
        "gender": athlete.gender,
        "city": athlete.city,
        "state": athlete.state,
        "country": athlete.country,
        "team": athlete.team,
        "event_count": len(events_seen),
        "total_miles": round(total_miles, 2),
        "total_km": round(total_km, 2),
        "performances": performances,
    }
