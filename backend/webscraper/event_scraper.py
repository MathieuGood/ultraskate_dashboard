import pprint
import re
import requests
from bs4 import BeautifulSoup

from models.lap_stats import LapStats
from models.event import Event
from models.athlete import Athlete
from models.performance import Performance
from models.athlete_registry import AthleteRegistry
from models.event_params import EventParams
from webscraper.webscraper import Webscraper
from webscraper.jms_site_params import JmsSiteParams
from webscraper.myraceresult_params import MyRaceResultParams
from utils import Utils


class EventScraper:
    """
    Class responsible for scraping an entire event
    """

    @classmethod
    def scrape(cls, event_params: EventParams) -> Event | None:
        if isinstance(event_params.scraped_site_params, JmsSiteParams):
            print(f"Scraping JMS site for event on {event_params.date}...")
            return cls.__scrape_jms_event(event_params)
        elif isinstance(event_params.scraped_site_params, MyRaceResultParams):
            print(f"Scraping MyRaceResult site for event on {event_params.date}...")
            return cls.__scrape_myraceresult_event(event_params)
        else:
            print(
                f"Scraping site for event on {event_params.date} not implemented yet."
            )
            return None

    @classmethod
    def __scrape_myraceresult_event(cls, event_params: EventParams) -> Event:
        event = Event(event_params)

        # Fetch participants JSON data
        participants_json = cls.fetch_particpants_json(event_params)
        if not participants_json:
            print(
                f"Could not fetch participants JSON data for event on {event_params.date}."
            )
            return event

        no_laps_performances = 0  # DEBUG

        keys = [1, 2]
        for key in keys:
            try:
                participants_data = participants_json["data"][f"#{key}_Individual"]
                break
            except KeyError:
                continue
        else:
            print("Could not find participants data in JSON.")
            return event

        # participants_data: list[list[str]] = participants_json["data"]["#1_Individual"]
        for participant in participants_data:
            print(
                f"ID : {participant[1]} / Name : {participant[3]} / Discipline : {participant[7]} / Age category : {participant[6]}"
            )
            performance = cls.__fetch_participant_performance(
                participant=participant, event=event, event_params=event_params
            )
            if performance:
                event.add_performance(performance)
            else:
                no_laps_performances += 1
        print(
            f"\nNumber of participants found for {event_params.date.year}: {len(participants_data)}"
        )
        print(f"Number of performances scraped: {len(event.performances)}")
        print(f"Number of performances with no laps: {no_laps_performances}\n")
        return event

    @classmethod
    def __format_myraceresult_name(cls, name: str) -> str:
        """
        Format a MyRaceResult participant name to "Last, First" format to "First Last"
        Args:
            name (str): Name string from MyRaceResult participant data
        Returns:
            str: Formatted name string
        """
        name_parts = name.split(", ")
        if len(name_parts) == 2:
            formatted_name = f"{name_parts[1]} {name_parts[0]}"
            return formatted_name
        return name

    @classmethod
    def __fetch_participant_performance(
        cls, participant: list[str], event: Event, event_params: EventParams
    ) -> Performance | None:
        if not isinstance(event_params.scraped_site_params, MyRaceResultParams):
            print(
                "EventScraper: Unsupported scraped site params for fetching participant performance."
            )
            return None

        participant_id: str = participant[1]
        participant_name: str = cls.__format_myraceresult_name(participant[3])
        participant_age_category: str = participant[
            event_params.scraped_site_params.age_group_col_index
        ]
        participant_discipline: str = participant[
            event_params.scraped_site_params.category_col_index
        ]
        participant_gender: str = participant[
            event_params.scraped_site_params.gender_col_index
        ]
        if participant_gender == "Open":
            participant_gender = "Male"
        participant_url = (
            f"{event_params.scraped_site_params.athlete_url}{participant_id}"
        )

        print(participant_url)

        response = requests.get(participant_url)
        if response.status_code != 200:
            print(
                f"Failed to fetch participant JSON data. Status code: {response.status_code}"
            )
            return None

        # pprint.pp(response.json())

        laps_data = response.json()["data"]
        all_laps_stats: list[LapStats] = []
        for lap_index, lap_data in enumerate(laps_data):
            lap_time = lap_data[4][:-3]
            if len(lap_time) == 5:
                lap_time_formatted = "00:" + str(lap_time)
            elif len(lap_time) == 7:
                lap_time_formatted = "0" + str(lap_time)
            elif len(lap_time) >= 8:
                lap_time_formatted = str(lap_time)

            lap_time_seconds = Utils.convert_time_str_to_seconds(
                lap_time_formatted
            )  # pyright: ignore[reportPossiblyUnboundVariable]
            if lap_time_seconds is None:
                print(
                    f"Could not convert lap time for lap {lap_index + 1}: {lap_time_formatted}"  # pyright: ignore[reportPossiblyUnboundVariable]
                )
                continue
            lap_stats = LapStats(lap_number=lap_index + 1, lap_time_ss=lap_time_seconds)
            all_laps_stats.append(lap_stats)

        athlete = Athlete(
            name=participant_name, gender=participant_gender
        )  # pyright: ignore[reportArgumentType]

        athlete_performance = Performance(
            athlete=athlete,
            age_group=participant_age_category,
            category=participant_discipline,
            laps=all_laps_stats,
            event=event,
        )
        # If there are no lap values, skip this participant
        if athlete_performance.total_laps() == 0:
            print(f"No laps found for participant {participant_name}")
            return None
        # print(athlete_performance)

        AthleteRegistry.add_athlete(athlete)

        return athlete_performance
        # https://my4.raceresult.com/192607/RRPublish/data/list?key=9d484a9a9259ff0ae1a4a8570861bc3b&listname=Online%7CLap%20Details&page=live&contest=0&r=pid&pid=421

    @classmethod
    def __scrape_jms_event(cls, event_params: EventParams) -> Event:
        event = Event(event_params)
        if not isinstance(event_params.scraped_site_params, JmsSiteParams):
            print("EventScraper: Invalid scraped site params for JMS event scraping.")
            return event

        athletes_urls: list[str] = []
        for category_index in event_params.scraped_site_params.categories_indexes:
            print(f"Scraping category index: {category_index}")
            athlete_performance_url = (
                event_params.scraped_site_params.ranking_home_url
                + f"&EId={category_index}&dt=0&adv=1"
            )
            print(f"Fetching athlete performance URLs from: {athlete_performance_url}")
            athletes_urls.extend(
                cls.__fetch_all_athlete_performance_urls(
                    athlete_performance_url, event_params
                )
            )

        # Fetch all athlete performance URLs from the event ranking page
        # athletes_urls = cls.__fetch_all_athlete_performance_urls(event_params)

        print(
            f"\nNumber of athlete URLs found for {event_params.date.year}: {len(athletes_urls)}"
        )

        for athlete_url in athletes_urls:
            performance = cls.__get_performance_from_athlete_url(
                athlete_url=athlete_url, event=event
            )
            if performance:
                event.add_performance(performance)

        print(
            f"Total athletes in registry: {len(AthleteRegistry.athletes)}/ {len(athletes_urls)}\n"
        )

        return event

    @classmethod
    def fetch_particpants_json(cls, event_params: EventParams) -> dict | None:
        """
        Build the URL to request the participants JSON data for a given event.

        Args:
            event_params (EventParams): Parameters of the event.
        Returns:
            dict: JSON data containing participants information.
        """
        if not isinstance(event_params.scraped_site_params, MyRaceResultParams):
            print(
                "EventScraper: Unsupported scraped site params for fetching participants JSON."
            )
            return None
        print(f"Participants URL: {event_params.scraped_site_params.ranking_home_url}")
        response = requests.get(event_params.scraped_site_params.ranking_home_url)

        pprint.pp(response.json())

        # If the request was successful, parse and return the JSON data
        if response.status_code != 200:
            print(
                f"Failed to fetch participants JSON data. Status code: {response.status_code}"
            )
            return None

        return response.json()

        # https://my4.raceresult.com/192607/RRPublish/data/list?key=9d484a9a9259ff0ae1a4a8570861bc3b&listname=Participants%7CParticipants%20List%20123&page=participants&contest=0&r=all&l=0

    @classmethod
    def __get_performance_from_athlete_url(
        cls, athlete_url: str, event: Event
    ) -> Performance | None:
        """
        From an athlete URL, scrape the athlete info and performance data and return a Performance object
        Args:
            athlete_url (str): URL of the athlete's performance page
            event_params (EventParams): Parameters of the event
        Returns:
            Performance | None: Performance object containing athlete info and performance data, or None if scraping fails
        """
        athlete_performance_soup = Webscraper.fetch_html(athlete_url)
        if not athlete_performance_soup:
            print(f"athlete_performance_soup is empty for URL: {athlete_url}")
        athlete_info = athlete_performance_soup.find(
            name="div", id="ctl00_Content_Main_divLeft"
        )
        # print(f"\nScraping athlete page: {athlete_url}")

        if not athlete_info:
            print(f"Could not find athlete info on page: {athlete_url}")
            print(athlete_performance_soup)
            return None

        athlete_name = ""
        athlete_gender = ""
        athlete_city = ""
        athlete_state = ""
        athlete_country = ""
        performance_age_group = ""
        performance_category = ""

        # Get athlete name from the specific span
        athlete_name_span = athlete_info.find(
            name="span", id="ctl00_Content_Main_lblName"
        )
        performance_category_span = athlete_info.find(
            name="span", id="ctl00_Content_Main_lblEvent"
        )
        if not athlete_name_span or not performance_category_span:
            return None
        athlete_name = athlete_name_span.text.strip()
        performance_category = performance_category_span.text.strip()

        # Get other athlete info from the table rows
        athlete_info_rows = athlete_info.find_all("tr")

        for row in athlete_info_rows:
            athlete_row_tds = row.find_all("td")
            if len(athlete_row_tds) < 2:
                continue
            label = athlete_row_tds[0].text.strip().lower()
            value = athlete_row_tds[1].text.strip()

            if "gender" in label:
                # print(f"Found athlete gender: {value}")
                athlete_gender = value
            elif "city" in label:
                # print(f"Found athlete city: {value}")
                athlete_city = value
            elif "state" in label:
                # print(f"Found athlete state: {value}")
                athlete_state = value
            elif "country" in label:
                # print(f"Found athlete country: {value}")
                athlete_country = value
            elif "category" in label and label != "secondary category :":
                performance_category = value

        athlete_laps_table = athlete_performance_soup.find(
            name="div", id="ctl00_Content_Main_divSplitGrid"
        )
        if not athlete_laps_table:
            print(f"No laps table found for athlete: {athlete_name} at {athlete_url}")
            return None

        lap_rows = [
            tr
            for tr in athlete_laps_table.find_all("tr")
            if "lap" in tr.get_text(separator=" ", strip=True).lower()
            and Utils.extract_time(tr.get_text()) is not None
        ]

        laps = cls.__parse_athlete_lap_rows(lap_rows)

        athlete = Athlete(
            name=athlete_name,
            gender=athlete_gender,
            city=athlete_city,
            state=athlete_state,
            country=athlete_country,
        )

        AthleteRegistry.add_athlete(athlete)

        return Performance(
            athlete=athlete,
            laps=laps,
            event=event,
            category=performance_category,
            age_group=performance_age_group,
        )

    @classmethod
    def __parse_athlete_lap_rows(cls, lap_rows) -> list[LapStats]:
        """
        Parse the lap rows of an athlete's performance table and extract lap times.
        """
        laps = []
        for lap_index, lap_row in enumerate(lap_rows):
            lap_row_cols = lap_row.find_all("td")
            lap_time = lap_row_cols[2]
            extracted_time = str(Utils.extract_time(lap_time.text))
            lap_time = Utils.convert_time_str_to_seconds(extracted_time)
            if lap_time is None:
                print(
                    f"Could not convert lap time for lap {lap_index + 1}: {extracted_time}"
                )
                continue
            lap_stats = LapStats(lap_number=lap_index + 1, lap_time_ss=lap_time)
            laps.append(lap_stats)
            # print(f"{lap_stats}")
        return laps

    @classmethod
    def __fetch_all_athlete_performance_urls(
        cls, ranking_url: str, event_params: EventParams
    ) -> list[str]:
        # Fetch home page of ranking as a BeautifulSoup object
        # Adding suffix to url in order to get the "advanced view" with page numbers
        if not isinstance(event_params.scraped_site_params, JmsSiteParams):
            print(
                "EventScraper: Unsupported scraped site params for fetching athlete URLs."
            )
            return []

        ranking_home_soup = Webscraper.fetch_html(ranking_url)

        # Extract the number of pages from the ranking page
        number_of_pages = cls.__get_number_of_pages(ranking_home_soup)

        print(
            f"Number of pages of {event_params.track.name} {event_params.date.year} : {number_of_pages}"
        )

        # HTML content of all the ranking pages
        all_ranking_pages: list[BeautifulSoup] = []

        if number_of_pages == 1:
            # If just one page, no need to scrape other content for now
            all_ranking_pages = [ranking_home_soup]
        else:
            # Build all the pages url
            ranking_pages_urls = cls.__build_all_ranking_pages_urls(
                number_of_pages=number_of_pages,
                base_url=ranking_url,
            )
            for ranking_page_url in ranking_pages_urls:
                all_ranking_pages.append(Webscraper.fetch_html(ranking_page_url))

        # Parse all the athlete individual performances urls across the rows
        return cls.__parse_athlete_urls_from_ranking(
            all_ranking_pages_soup=all_ranking_pages, event_params=event_params
        )

    @classmethod
    def __parse_athlete_urls_from_ranking(
        cls, all_ranking_pages_soup: list[BeautifulSoup], event_params: EventParams
    ) -> list[str]:
        if not isinstance(event_params.scraped_site_params, JmsSiteParams):
            print(
                "EventScraper: Unsupported scraped site params for parsing athlete URLs."
            )
            return []

        athletes_urls: list[str] = []
        for ranking_page in all_ranking_pages_soup:
            ranking_table = ranking_page.find(
                name="div", id="ctl00_Content_Main_divGrid"
            )
            if not ranking_table:
                continue
            athlete_rows = ranking_table.find_all("tr")

            for athlete_row in athlete_rows:
                row_tds = athlete_row.find_all("td")
                row_links = athlete_row.find_all("a")

                position_col_index = event_params.scraped_site_params.position_col_index
                name_col_index = event_params.scraped_site_params.name_col_index
                athlete_link_col_index = (
                    event_params.scraped_site_params.athlete_link_col_index
                )

                # Extract the link and name of the skater
                position = row_tds[position_col_index].text.strip()

                # If position is not a digit, skip the row (it can be a header or other info)
                if not position.isdigit():
                    continue

                name = row_tds[name_col_index].text.strip()  # noqa: F841

                # Build the complete URL for the skater's personal stats page
                base_url = Utils.extract_base_url(
                    event_params.scraped_site_params.ranking_home_url
                )
                athlete_url_end = str(row_links[athlete_link_col_index]["href"])
                if not base_url or not athlete_url_end:
                    # print(f"Skipping {base_url} + {athlete_url_end}")
                    continue
                athlete_full_url = base_url + athlete_url_end
                athletes_urls.append(athlete_full_url)
                # print(
                #     f"Row {row_index} -> POS {position} / NAME {name} / URL {athlete_full_url}"
                # )
        print(f"--> Athletes urls found: {len(athletes_urls)}")

        return athletes_urls

    @classmethod
    def __build_all_ranking_pages_urls(
        cls, number_of_pages: int, base_url: str
    ) -> list[str]:
        """
        Build all the ranking pages urls based on the base url and the number of pages

        Args:
            number_of_pages (int): Total number of pages in the ranking
            base_url (str): Base URL of the ranking page
        Returns:
            list[str]: List of all ranking pages URLs
        """

        pages_urls = []
        for i in range(1, number_of_pages + 1):
            pages_urls.append(base_url + "&PageNo=" + str(i))
        return pages_urls

    @classmethod
    def __get_number_of_pages(cls, ranking_home_soup: BeautifulSoup) -> int:
        """
        From a BeautifulSoup objet containing the ranking home page, find the tag contaning pagination info and extract the total number of pages

        Args:
            ranking_home_soup (BeautifulSoup): BeautifulSoup object of the ranking home page
        Returns:
            int: Total number of pages in the ranking
        """

        # print(ranking_home_soup)

        # Look for the tag containing the number of pages
        page_number_span = ranking_home_soup.find_all(
            "span", id="ctl00_Content_Main_lblTopPager"
        )

        # When no page number tag found, it means there is only one page
        if len(page_number_span) == 0:
            return 1

        # Convert bs4 tag to text
        page_number_span = page_number_span[0].text

        # From the string formatted like "Page 1 of 2 (76 items)" extract all the numbers with a regex
        page_number_span = re.findall(r"\d+", page_number_span)

        # Get second int (number of pages)
        number_of_pages = int(page_number_span[1])

        return number_of_pages
