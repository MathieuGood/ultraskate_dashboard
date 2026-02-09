from models.scraped_site_params import ScrapedSiteParams


class JmsSiteParams(ScrapedSiteParams):
    """
    Parameters for scraping the JMS site.
    """

    def __init__(
        self,
        ranking_home_url: str,
        categories_indexes: list[int],
        position_col_index: int,
        name_col_index: int,
        athlete_link_col_index: int = 1,
    ):
        self.base_url = "https://jms.racetecresults.com"
        self.categories_indexes = categories_indexes
        self.ranking_home_url = ranking_home_url
        self.position_col_index = position_col_index
        self.name_col_index = name_col_index
        self.athlete_link_col_index = athlete_link_col_index
