"""Routes for event endpoints"""

from fastapi import APIRouter
from models.event_registry import EventRegistry
from event_stats import EventStats

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
async def get_all_events():
    """Get all events (metadata only, no performances)"""
    events = EventRegistry.events
    return [event.to_dict(performances=False) for event in events]


@router.get("/{name}/{year}")
async def get_event_by_name_year(name: str, year: int):
    """Get event by name and year"""
    event = EventRegistry.get_by_name_year(name, year)
    if event is None:
        return {"error": f"Event not found for name '{name}', year {year}"}
    return event.to_dict(laps=False)


@router.get("/{name}/{year}/graph")
async def get_event_graph_data(name: str, year: int):
    """Get ECharts-ready graph data for an event (cumulative miles over time)"""
    event = EventRegistry.get_by_name_year(name, year)
    if event is None:
        return {"error": f"Event not found for name '{name}', year {year}"}
    return {
        "performances": [
            perf.to_graph_dict() for perf in event.performances
        ]
    }


@router.get("/by-name/{name}")
async def get_events_by_name(name: str):
    """Get all events for a given name"""
    events = EventRegistry.get_by_name(name)
    if not events:
        return {"error": f"No events found for name '{name}'"}
    return [event.to_dict(laps=False) for event in events]


@router.get("/{year}")
async def get_event_by_year(year: int):
    """Get event by year"""
    for event in EventRegistry.events:
        if event.date.year == year:
            event_stats = EventStats(event)
            return event.to_dict(laps=False)
    return {"error": f"Event for year {year} not found"}
