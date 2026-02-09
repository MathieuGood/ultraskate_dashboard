from __future__ import annotations


class Track:
    """
    Class representing a track
    """

    def __init__(self, name: str, city: str, country: str, length_miles: float):
        """
        Initialize a Track instance.

        :param name: Name of the track
        :type name: str
        :param city: City where the track is located
        :type city: str
        :param length_km: Length of the track in miles
        :type length_km: float
        """
        self.name: str = name
        self.city: str = city
        self.country: str = country
        self.length_miles: float = length_miles

    def __str__(self) -> str:
        return f"Track {self.name} ({self.city}, {self.country})"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "city": self.city,
            "country": self.country,
            "length_miles": self.length_miles,
        }

    @classmethod
    def from_dict(cls, track_data: dict) -> Track:
        return cls(
            name=track_data["name"],
            city=track_data["city"],
            country=track_data["country"],
            length_miles=track_data["length_miles"],
        )
