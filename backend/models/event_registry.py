from models.event import Event


class EventRegistry:
    events: list[Event] = []

    @classmethod
    def add_event(cls, event: Event) -> bool:
        cls.events.append(event)
        cls.events.sort(key=lambda e: e.date)
        return True

    @classmethod
    def get_by_city_year(cls, city: str, year: int) -> Event | None:
        for event in cls.events:
            if event.track.city.lower() == city.lower() and event.date.year == year:
                return event
        return None

    @classmethod
    def get_by_city(cls, city: str) -> list[Event]:
        return [
            event for event in cls.events
            if event.track.city.lower() == city.lower()
        ]

    @classmethod
    def sort_all_performances(cls) -> None:
        for event in cls.events:
            event.performances.sort(key=lambda p: p.total_miles(), reverse=True)
