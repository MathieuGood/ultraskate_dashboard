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

        :param event_params: Parameters for the event.
        :type event_params: EventParams | None
        """
        self.performances: list[Performance] = []
        self.name: str = ''

        if event_params is not None:
            self.date: datetime = event_params.date
            self.track: Track = event_params.track
            self.name: str = event_params.name

    @property
    def slug(self) -> str:
        name_part = self.name.lower().replace(' ', '-')
        return f'{name_part}_{self.date.year}'

    def add_performance(self, performance: Performance) -> None:
        self.performances.append(performance)

    def to_dict(self, performances: bool = True, laps: bool = True) -> dict:
        result = {
            "name": self.name,
            "date": self.date.isoformat(),
            "track": self.track.to_dict(),
        }
        if performances:
            result["performances"] = [
                p.to_dict(laps=laps) for p in self.performances
            ]
        return result

    def to_json_file(self, file_name: str) -> None:
        data = self.to_dict(laps=True)
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def from_json_file(cls, file_name: str) -> Event:
        with open(file_name, "r") as json_file:
            event_data = json.load(json_file)

        event = cls(event_params=None)
        event.name = event_data.get("name", "")
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
