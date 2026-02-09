from file_manager import FileManager
from models.event import Event
from models.event_registry import EventRegistry


def load_events() -> bool:
    """Charge tous les événements depuis les fichiers JSON et les enregistre.

    Returns:
        bool: True si au moins un événement a été chargé.
    """
    json_files = FileManager.get_all_json_in_dir("scraped_events_save")

    if not json_files:
        print("⚠️  Aucun fichier d'événement trouvé dans 'scraped_events_save/'")
        return False

    for file in json_files:
        try:
            event = Event.from_json_file(file)
            EventRegistry.add_event(event)
            print(f"✓ Chargé: {event.track.city} {event.date.year}")
        except Exception as e:
            print(f"✗ Erreur lors du chargement {file}: {e}")

    return len(EventRegistry.events) > 0
