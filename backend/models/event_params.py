from datetime import datetime
from models.track import Track
from models.scraped_site_params import ScrapedSiteParams


class EventParams:
    def __init__(
        self,
        scraped_site_params: ScrapedSiteParams,
        date: str,
        track: Track,
    ):
        """
        Initializes the parameters for an event.

        Args:
            date (str): The date of the event in ``YYYY-MM-DD`` format.
            track (Track): The track where the event takes place.
            url (str): The URL of the rankings page.
            position_col_index (int): Index of the column in the ranking page containing the athlete's position.
            name_col_index (int): Index of the column in the ranking page containing the athlete's name.
        """
        self.scraped_site_params: ScrapedSiteParams = scraped_site_params
        self.date: datetime = datetime.strptime(date, "%Y-%m-%d")
        self.track: Track = track
