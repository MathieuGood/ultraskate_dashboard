"""Routes for event endpoints"""

from fastapi import APIRouter
from models.event_registry import EventRegistry
from event_stats import EventStats

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
async def get_all_events():
    """Get all events"""
    events = EventRegistry.events
    return [event.to_dict(laps=False) for event in events]


@router.get("/{year}")
async def get_event_by_year(year: int):
    """Get event by year"""
    for event in EventRegistry.events:
        if event.date.year == year:
            event_stats = EventStats(event)
            return event.to_dict(laps=False)
    return {"error": f"Event for year {year} not found"}
