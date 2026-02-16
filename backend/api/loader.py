from file_manager import FileManager
from models.event import Event
from models.event_registry import EventRegistry
from models.athlete_registry import AthleteRegistry


def load_events() -> bool:
    """Charge tous les événements depuis les fichiers JSON et les enregistre.

    Returns:
        bool: True si au moins un événement a été chargé.
    """
    json_files = FileManager.get_all_json_in_dir("scraped_events_save")

    if not json_files:
        print("[WARN] No event files found in 'scraped_events_save/'")
        return False

    for file in json_files:
        try:
            event = Event.from_json_file(file)
            EventRegistry.add_event(event)
            EventRegistry.sort_all_performances()
            print(f"[OK] Loaded: {event.name} {event.date.year}")
        except Exception as e:
            print(f"[ERROR] Loading {file}: {e}")

    print(
        f"[OK] {EventRegistry.count()} events loaded, "
        f"{AthleteRegistry.count()} unique athletes registered"
    )

    return len(EventRegistry.events) > 0
