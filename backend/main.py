import os
from file_manager import FileManager
from webscraper.event_scraper import EventScraper
from webscraper.browser_manager import BrowserManager
from event_params_data import miami_event_params
from models.event import Event
from models.event_registry import EventRegistry
from event_stats import EventStats
from scraper import scrape_events


def main():
    # scrape_events()

    for file in FileManager.get_all_json_in_dir("scraped_events_save"):
        event = Event.from_json_file(file)
        EventRegistry.add_event(event)

    unique_sports = set()
    unique_categories = set()
    unique_age_groups = set()

    for event in EventRegistry.events:
        if event.date.year:
            print("\n", event.track.city, event.date.year)

            for performance in event.performances:
                unique_sports.add(performance.sport)
                unique_categories.add(performance.category)
                unique_age_groups.add(performance.age_group)

            event_stats = EventStats(event)
            # event_stats.print_all(event_stats.top(100))

            # Output to CSV
            with open("event_stats_" + str(event.date.year) + ".csv", "w") as f:
                f.write(
                    "Name,Sport,Discipline,Age Category,Total Miles,Total Laps,Average Speed (kph),Total Time (HH:MM:SS)\n"
                )
                for performance in event_stats.get_all():
                    f.write(
                        f"{performance.athlete.name},{performance.sport},{performance.category},{performance.age_group}, {performance.athlete.team}\n"
                    )

    print("\nUnique sports in all events:")
    for sport in sorted(unique_sports):
        print("-", sport)

    print("\nUnique categories in all events:")
    for category in sorted(unique_categories):
        print("-", category)
    print("\nUnique age groups in all events:")
    for age_group in sorted(unique_age_groups):
        print("-", age_group)


if __name__ == "__main__":
    main()
