from __future__ import annotations

from typing import TYPE_CHECKING

from models.athlete import Athlete

if TYPE_CHECKING:
    from models.event import Event


class AthleteRegistry:
    athletes: list[Athlete] = []
    _by_canonical: dict[str, Athlete] = {}
    total_count: int = 0

    @classmethod
    def get_or_register(cls, athlete: Athlete, event: Event | None = None) -> Athlete:
        """Return the canonical Athlete object for the given athlete.

        If an athlete with the same canonical name already exists in the
        registry, the existing instance is returned so that every performance
        across all events shares the same Athlete object.

        When the athlete is new, it is registered and returned.

        Note: same-name-in-same-event disambiguation (e.g. Jorge Rodriguez
        in Miami 2015/2016) is handled upstream in Performance.from_dict()
        by appending the category to the name before calling this method.
        """
        cls.total_count += 1
        key = athlete.canonical_name

        if key in cls._by_canonical:
            print(
                f"Duplicate athlete name detected: '{athlete.name}' (canonical: '{key}'). "
            )
            return cls._by_canonical[key]

        cls._by_canonical[key] = athlete
        cls.athletes.append(athlete)
        cls.athletes.sort(key=lambda a: a.name.lower())
        return athlete

    @classmethod
    def get_by_name(cls, name: str) -> Athlete | None:
        """Look up an athlete by any known name variant."""
        tmp = Athlete(name=name)
        return cls._by_canonical.get(tmp.canonical_name)

    @classmethod
    def clear(cls) -> None:
        """Reset the registry (useful for testing)."""
        cls.athletes.clear()
        cls._by_canonical.clear()

    @classmethod
    def count(cls) -> int:
        return len(cls.athletes)
