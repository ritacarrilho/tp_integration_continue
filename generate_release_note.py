import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Paramètres Trello
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_API_SECRET')
BOARD_ID = os.getenv('TRELLO_BOARD_ID')
LIST_NAME = "Releases"  # Nom de la liste où la carte sera ajoutée

# URL pour accéder aux listes du board Trello
TRELLO_LISTS_URL = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"

# Paramètres pour l'appel API
params = {
    'key': TRELLO_API_KEY,
    'token': TRELLO_TOKEN,
}

try:
    # Récupérer l'ID de la liste "Releases"
    lists_response = requests.get(TRELLO_LISTS_URL, params=params)
    lists_response.raise_for_status()  # Lève une exception en cas d'erreur HTTP

    lists = lists_response.json()

    list_id = None
    for lst in lists:
        if lst['name'] == LIST_NAME:
            list_id = lst['id']
            break

    if not list_id:
        raise ValueError(f"La liste '{LIST_NAME}' n'existe pas sur le board Trello.")

    # Autres opérations à effectuer ici (créer la carte de release note, etc.)

except requests.exceptions.RequestException as e:
    print(f"Une erreur s'est produite lors de la requête HTTP : {e}")

except ValueError as ve:
    print(ve)

except Exception as ex:
    print(f"Une erreur inattendue s'est produite : {ex}")