"""Routes for performance endpoints"""

from fastapi import APIRouter
from models.event_registry import EventRegistry
from event_stats import EventStats

router = APIRouter(prefix="/performances", tags=["performances"])


@router.get("/year/{year}")
async def get_performances_by_year(year: int):
    """Get all performances for a specific year"""
    for event in EventRegistry.events:
        if event.date.year == year:
            event_stats = EventStats(event)
            return {
                "year": year,
                "track": event.track.to_dict(),
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
    return {"error": f"No performances found for year {year}"}


@router.get("/year/{year}/sport/{sport}")
async def get_performances_by_sport(year: int, sport: str):
    """Get performances filtered by sport for a specific year"""
    for event in EventRegistry.events:
        if event.date.year == year:
            event_stats = EventStats(event)
            filtered = event_stats.by_sport(sport)
            return {
                "year": year,
                "sport": sport,
                "count": len(filtered),
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
                    for perf in filtered
                ],
            }
    return {"error": f"No performances found for year {year}"}


@router.get("/year/{year}/top/{n}")
async def get_top_performances(year: int, n: int = 10):
    """Get top N performances for a specific year"""
    for event in EventRegistry.events:
        if event.date.year == year:
            event_stats = EventStats(event)
            top_performances = event_stats.top(n)
            return {
                "year": year,
                "top_count": n,
                "performances": [
                    {
                        "position": i + 1,
                        "athlete": perf.athlete.to_dict(),
                        "category": perf.category,
                        "age_group": perf.age_group,
                        "sport": perf.sport,
                        "total_miles": perf.total_miles(),
                        "total_laps": perf.total_laps(),
                        "total_time": perf.total_time_hhmmss(),
                        "average_speed_kph": perf.average_speed_kph(),
                    }
                    for i, perf in enumerate(top_performances)
                ],
            }
    return {"error": f"No performances found for year {year}"}
