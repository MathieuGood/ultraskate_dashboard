from models.scraped_site_params import ScrapedSiteParams


class MyRaceResultParams(ScrapedSiteParams):
    """
    Parameters for scraping the MyRaceResult site.
    """

    def __init__(
        self,
        race_id: int,
        ranking_home_url: str,
        athlete_middle_url: str,
        gender_col_index: int,
        discipline_col_index: int,
        age_category_col_index: int,
    ):
        self.base_url = "https://my4.raceresult.com/"
        self.race_id = race_id
        self.url = f"{self.base_url}{self.race_id}"
        self.ranking_home_url = ranking_home_url
        self.athlete_url = self.url + athlete_middle_url
        self.gender_col_index = gender_col_index
        self.category_col_index = discipline_col_index
        self.age_group_col_index = age_category_col_index
