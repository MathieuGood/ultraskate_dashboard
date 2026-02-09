from utils import Utils


class LapStats:
    def __init__(self, lap_number: int, lap_time_ss: int):
        self.lap_number = lap_number
        self.lap_time_ss = lap_time_ss

    def get_lap_time_hhmmss(self) -> str:
        return Utils.seconds_to_hhmmss(self.lap_time_ss)

    def __str__(self) -> str:
        return f"Lap {self.lap_number} -> {self.get_lap_time_hhmmss()}"
