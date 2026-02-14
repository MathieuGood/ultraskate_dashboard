from datetime import datetime
from models.track import Track
from models.scraped_site_params import ScrapedSiteParams


class EventParams:
    def __init__(
        self,
        scraped_site_params: ScrapedSiteParams,
        date: str,
        track: Track,
        name: str = "",
    ):
        """
        Initializes the parameters for an event.

        Args:
            date (str): The date of the event in ``YYYY-MM-DD`` format.
            track (Track): The track where the event takes place.
            name (str): Display name of the event (e.g. "Miami", "Dutch").
        """
        self.scraped_site_params: ScrapedSiteParams = scraped_site_params
        self.date: datetime = datetime.strptime(date, "%Y-%m-%d")
        self.track: Track = track
        self.name: str = name
