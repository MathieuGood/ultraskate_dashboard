from __future__ import annotations


class Athlete:
    def __init__(
        self,
        name: str,
        gender: str = "",
        city: str = "",
        state: str = "",
        country: str = "",
    ):
        if name == "":
            raise ValueError("Athlete name cannot be empty")
        self.name = name
        self.gender = gender
        self.city = city
        self.state = state
        self.country = country
        self.team = False

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "gender": self.gender,
            "city": self.city,
            "state": self.state,
            "country": self.country,
        }

    @classmethod
    def from_dict(cls, athlete_data: dict[str, str]) -> Athlete:
        return cls(
            name=athlete_data["name"],
            gender=athlete_data["gender"],
            city=athlete_data["city"],
            state=athlete_data["state"],
            country=athlete_data["country"],
        )

    def __str__(self) -> str:
        return f"Athlete(name={self.name}, gender={self.gender}, city={self.city}, state={self.state}, country={self.country})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Athlete):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
