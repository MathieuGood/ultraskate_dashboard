from __future__ import annotations
from typing import TYPE_CHECKING

from models.athlete import Athlete
from models.lap_stats import LapStats
from utils import Utils

if TYPE_CHECKING:
    from models.event import Event


class Performance:
    """Class representing an athlete's performance in an event."""

    def __init__(
        self,
        athlete: Athlete,
        laps: list[LapStats],
        event: Event,
        category: str = "",
        age_group: str = "",
    ):
        self.athlete = athlete
        self.laps = laps
        self.category = category
        self.age_group = age_group
        self.event = event
        self.total_time_ss = self._total_time_ss()
        self.__set_team()
        self.__set_sport()

    def __str__(self) -> str:
        return f"{self.athlete.name} - {self.total_miles():.2f} miles - {self.total_laps()} laps - {self.average_speed_kph():.2f} kph - {self.sport} - {self.category} - {self.age_group}"

    def __set_team(self):
        if "team" in self.category.lower() or "team" in self.athlete.name.lower():
            self.athlete.team = True

    def __set_sport(self):
        if self.category == "24 Hour":
            self.category = "Skateboard"
            self.sport = "Skateboard"
            return
        if "ages" in self.category.lower():
            self.age_group = self.category
            self.category = "Skateboard"
            self.sport = "Skateboard"
            return
        if "paddle" in self.category.lower() and "push" in self.category.lower():
            self.sport = "Paddle Push"
            return
        if "paddle" in self.category.lower():
            self.sport = "Paddle"
            return
        elif "inline" in self.category.lower() or "roller" in self.category.lower():
            self.sport = "Inline Skating"
            return
        elif "quad" in self.category.lower():
            self.sport = "Quad Skating"
            return
        else:
            self.sport = "Skateboard"

    def total_time_hhmmss(self) -> str:
        """
        Get the total performance time formatted as HH:MM:SS.

        Returns:
            str: Total time in HH:MM:SS format
        """
        return Utils.seconds_to_hhmmss(self.total_time_ss)

    def _total_time_ss(self) -> int:
        """
        Calculate the total performance time in seconds by summing all lap times.

        Returns:
            int: Total time in seconds
        """
        return sum(lap.lap_time_ss for lap in self.laps)

    def total_laps(self) -> int:
        """
        Get the total number of laps completed.

        Returns:
            int: Number of laps
        """
        return len(self.laps)

    def total_miles(self) -> float:
        """
        Get the total distance covered in miles.

        Returns:
            float: Total distance in miles
        """
        return self.event.track.length_miles * self.total_laps()

    def total_km(self) -> float:
        """
        Get the total distance covered in kilometers.

        Returns:
            float: Total distance in kilometers
        """
        return self.total_miles() * 1.60934

    def total_miles_at_lap(self, lap_number: int) -> float:
        """
        Get the total distance covered in miles up to and including the specified lap.

        Args:
            lap_number (int): The lap number to calculate distance through (1-indexed)
        Returns:
            float: Total distance in miles up to the specified lap
        """
        if lap_number > self.total_laps() or lap_number <= 0:
            return 0.0
        return self.event.track.length_miles * lap_number

    def total_km_at_lap(self, lap_number: int) -> float:
        """
        Get the total distance covered in kilometers up to and including the specified lap.

        Args:
            lap_number (int): The lap number to calculate distance through (1-indexed)
        Returns:
            float: Total distance in kilometers up to the specified lap
        """
        return self.total_miles_at_lap(lap_number) * 1.60934

    def average_lap_time_ss(self) -> float:
        """
        Get the average time per lap in seconds.

        Returns:
            float: Average lap time in seconds, or 0.0 if no laps completed
        """
        if self.total_laps() == 0:
            return 0.0
        return self.total_time_ss / self.total_laps()

    def _calculate_average_speed(
        self, total_miles: float, total_time_ss: int, unit: str = "mph"
    ) -> float:
        """
        Calculate average speed given distance and time.

        Args:
            total_miles (float): Total distance covered in miles
            total_time_ss (int): Total time in seconds
            unit (str): Speed unit, either "mph" or "kph" (default: "mph")

        Returns:
            float: Average speed in the specified unit, or 0.0 if time is zero
        """
        total_hours = total_time_ss / 3600
        if total_hours == 0:
            return 0.0

        speed_mph = total_miles / total_hours
        return speed_mph if unit == "mph" else speed_mph * 1.60934

    def average_speed_mph(self) -> float:
        """
        Get the average speed for the entire performance in miles per hour.

        Returns:
            float: Average speed in mph, or 0.0 if no time elapsed
        """
        return self._calculate_average_speed(
            self.total_miles(), self.total_time_ss, "mph"
        )

    def average_speed_kph(self) -> float:
        """
        Get the average speed for the entire performance in kilometers per hour.

        Returns:
            float: Average speed in kph, or 0.0 if no time elapsed
        """
        return self._calculate_average_speed(
            self.total_miles(), self.total_time_ss, "kph"
        )

    def average_speed_kph_at_lap(self, lap_number: int) -> float:
        """
        Get the cumulative average speed up to and including the specified lap.

        Args:
            lap_number (int): The lap number to calculate cumulative average speed through (1-indexed)

        Returns:
            float: Cumulative average speed in kph, or 0.0 if lap_number is invalid
        """
        if lap_number > self.total_laps() or lap_number <= 0:
            return 0.0
        total_time_ss = sum(self.laps[i].lap_time_ss for i in range(lap_number))
        total_miles = self.event.track.length_miles * lap_number
        return self._calculate_average_speed(total_miles, total_time_ss, "kph")

    def average_speed_kph_for_lap(self, lap_number: int) -> float:
        """
        Get the average speed for a specific single lap in kilometers per hour.

        Args:
            lap_number (int): The lap number to get average speed for (1-indexed)

        Returns:
            float: Average speed for that lap in kph, or 0.0 if lap_number is invalid
        """
        if lap_number > self.total_laps() or lap_number <= 0:
            return 0.0
        lap_time_ss = self.laps[lap_number - 1].lap_time_ss
        total_miles = self.event.track.length_miles
        return self._calculate_average_speed(total_miles, lap_time_ss, "kph")

    def to_dict(self) -> dict:
        return {
            "athlete": self.athlete.to_dict(),
            "category": self.category,
            "age_group": self.age_group,
            "total_time_hhmmss": self.total_time_hhmmss(),
            "total_laps": self.total_laps(),
            "total_miles": self.total_miles(),
            "total_km": self.total_km(),
            "laps": [
                {"number": lap.lap_number, "time": lap.get_lap_time_hhmmss()}
                for lap in self.laps
            ],
        }

    @classmethod
    def from_dict(cls, performance_data: dict, event: Event) -> Performance:
        athlete = Athlete.from_dict(performance_data["athlete"])
        laps = []
        for lap_data in performance_data["laps"]:
            lap_time = Utils.convert_time_str_to_seconds(lap_data["time"])
            if lap_time is not None:
                laps.append(
                    LapStats(
                        lap_number=lap_data["number"],
                        lap_time_ss=lap_time,
                    )
                )
        return cls(
            athlete=athlete,
            laps=laps,
            event=event,
            category=performance_data["category"],
            age_group=performance_data["age_group"],
        )
