#!/usr/bin/env python3
"""
Script pour démarrer l'API FastAPI avec les événements pré-chargés.
"""

import sys
from api.loader import load_events
from models.event_registry import EventRegistry

if __name__ == "__main__":
    print("🚀 Démarrage de l'API UltraskateDashboard...\n")

    # Charger les événements
    print("📂 Chargement des événements...")
    if load_events():
        print(f"\n✓ {len(EventRegistry.events)} événement(s) chargé(s)\n")
    else:
        print("\n⚠️  Aucun événement chargé - l'API fonctionnera en mode vide\n")

    # Démarrer le serveur
    import uvicorn
    from api.app import app

    print("🌐 Serveur en cours de démarrage...")
    print("📖 Documentation: http://localhost:8000/docs")
    print("🛑 Appuyez sur CTRL+C pour arrêter\n")

    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n\n✓ API arrêtée")
        sys.exit(0)
