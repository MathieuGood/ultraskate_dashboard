import os
from webscraper.event_scraper import EventScraper
from webscraper.browser_manager import BrowserManager
from event_params_data import miami_event_params
from models.event import Event
from event_stats import EventStats


def scrape_events():
    BrowserManager.start()

    try:
        events = [
            # EventScraper.scrape(miami_event_params[2013]),
            # EventScraper.scrape(miami_event_params[2014]),
            # EventScraper.scrape(miami_event_params[2015]),
            # EventScraper.scrape(miami_event_params[2016]),
            # EventScraper.scrape(miami_event_params[2017]),
            # EventScraper.scrape(miami_event_params[2018]),
            # EventScraper.scrape(miami_event_params[2019]),
            # EventScraper.scrape(miami_event_params[2020]),
            # EventScraper.scrape(miami_event_params[2021]),
            # EventScraper.scrape(miami_event_params[2022]),
            # EventScraper.scrape(miami_event_params[2023]),
            # EventScraper.scrape(miami_event_params[2024]),
            # EventScraper.scrape(miami_event_params[2025]),
        ]
    finally:
        BrowserManager.shutdown()

    for event in events:
        if event is None or len(event.performances) == 0:
            continue

        event.to_json_file(
            os.path.join("ultraskate_miami_" + str(event.date.year) + ".json")
        )
