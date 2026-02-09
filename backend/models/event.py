from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING

from models.track import Track
from models.event_params import EventParams


from models.performance import Performance


class Event:
    """
    Class representing an event
    """

    def __init__(self, event_params: EventParams | None = None) -> None:
        """
        Initialize an Event instance.

        :param date: The date of the event in 'YYYY-MM-DD' format.
        :type date: str
        :param track: The track where the event takes place.
        :type track: Track
        :param url: URL of the rankings page
        :type url : str
        """
        self.performances: list[Performance] = []

        if event_params is not None:
            self.date: datetime = event_params.date
            self.track: Track = event_params.track

    def add_performance(self, performance: Performance) -> None:
        self.performances.append(performance)

    def to_dict(self) -> dict:
        performances_list: list[dict] = []
        for performance in self.performances:
            performances_list.append(performance.to_dict())
        return {
            "date": self.date.isoformat(),
            "track": self.track.to_dict(),
            "performances": performances_list,
        }

    def to_json_file(self, file_name: str) -> None:
        with open(file_name, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def from_json_file(cls, file_name: str) -> Event:
        with open(file_name, "r") as json_file:
            event_data = json.load(json_file)

        event = cls(event_params=None)
        event.track = Track.from_dict(track_data=event_data["track"])
        event.date = datetime.fromisoformat(event_data["date"])
        for performance_data in event_data["performances"]:
            performance = Performance.from_dict(
                performance_data=performance_data, event=event
            )
            event.add_performance(performance)

        return event

    def __str__(self) -> str:
        summary_lines = [
            "-----",
            f"Event on {self.date} at {self.track.name}, {self.track.city}, {self.track.country}",
        ]

        if len(self.performances) == 0:
            summary_lines.append("No performances recorded for this event.")
            summary_lines.append("-----\n")
            return "\n".join(summary_lines)

        summary_lines.append(f"🥇 {self.performances[0]}")
        if len(self.performances) > 1:
            summary_lines.append(f"🥈 {self.performances[1]}")
        if len(self.performances) > 2:
            summary_lines.append(f"🥉 {self.performances[2]}")
        summary_lines.append("-----\n")

        return "\n".join(summary_lines)
