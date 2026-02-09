from models.athlete import Athlete


class AthleteRegistry:
    athletes: list[Athlete] = []

    @classmethod
    def add_athlete(cls, athlete: Athlete) -> bool:
        """
        Add an athlete to the registry if not already present.

        Parameters:
            athlete (Athlete): The athlete to add.

        Returns:
            bool: True if the athlete was added, False if already present.
        """
        # if athlete in cls.athletes:
        #     print(
        #         f" !!! Athlete {athlete.name} already in registry, skipping addition."
        #     )
        #     return False
        cls.athletes.append(athlete)
        cls.athletes.sort(key=lambda a: a.name)
        print(f"Added : {athlete}")
        return True
