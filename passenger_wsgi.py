"""
Fichier de déploiement pour o2switch (Passenger)
"""
import sys
import os

# Ajouter le répertoire de l'application au path Python
sys.path.insert(0, os.path.dirname(__file__))

# Importer l'application Flask
from app import create_app

application = create_app()

# Pour Passenger
if __name__ == '__main__':
    application.run()
