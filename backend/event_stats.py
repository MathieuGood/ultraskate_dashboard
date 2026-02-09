from __future__ import annotations

from models.event import Event
from models.performance import Performance


class EventStats:
    def __init__(self, event: Event) -> None:
        self.event: Event = event

    def _sorted_performances(self) -> list[Performance]:
        return sorted(
            self.event.performances,
            key=lambda performance: performance.total_miles(),
            reverse=True,
        )

    def by_sport(self, sport: str) -> list[Performance]:
        sport = sport.lower()

        return [
            performance
            for performance in self._sorted_performances()
            if sport in performance.sport.lower()
        ]

    def top(
        self, n: int, performances: list[Performance] | None = None
    ) -> list[Performance]:
        if not performances:
            performances = self._sorted_performances()
        return performances[:n]

    def get_all(self) -> list[Performance]:
        return self._sorted_performances()

    def print_all(self, performances: list[Performance] | None = None) -> None:
        if not performances:
            performances = self._sorted_performances()
        for performance in performances:
            print(performance)
