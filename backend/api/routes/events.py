"""Routes for event endpoints"""

from fastapi import APIRouter
from models.event_registry import EventRegistry
from event_stats import EventStats

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
async def list_events():
    """Get all events"""
    events = EventRegistry.events
    return {
        "count": len(events),
        "events": [
            {
                "date": event.date.isoformat(),
                "track": event.track.to_dict(),
                "performances_count": len(event.performances),
            }
            for event in events
        ],
    }


@router.get("/{year}")
async def get_event_by_year(year: int):
    """Get event by year"""
    for event in EventRegistry.events:
        if event.date.year == year:
            event_stats = EventStats(event)
            return {
                "date": event.date.isoformat(),
                "track": event.track.to_dict(),
                "total_participants": len(event.performances),
                "performances": [
                    {
                        "athlete": perf.athlete.to_dict(),
                        "category": perf.category,
                        "age_group": perf.age_group,
                        "sport": perf.sport,
                        "total_miles": perf.total_miles(),
                        "total_laps": perf.total_laps(),
                        "total_time": perf.total_time_hhmmss(),
                        "average_speed_kph": perf.average_speed_kph(),
                    }
                    for perf in event_stats.get_all()
                ],
            }
    return {"error": f"Event for year {year} not found"}
