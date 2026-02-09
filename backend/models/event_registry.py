from models.event import Event


class EventRegistry:
    events: list[Event] = []

    @classmethod
    def add_event(cls, event: Event) -> bool:
        cls.events.append(event)
        cls.events.sort(key=lambda e: e.date)
        return True
