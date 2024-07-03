import requests
import os
import json
from datetime import datetime

# Paramètres Trello
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_API_SECRET')
BOARD_ID = os.getenv('TRELLO_BOARD_ID')
LIST_NAME = "Releases"  # Nom de la liste où la carte sera ajoutée

# URL pour accéder aux cartes du board Trello
TRELLO_API_URL = f"https://api.trello.com/1/boards/{BOARD_ID}/cards"
TRELLO_LISTS_URL = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"

# Paramètres pour l'appel API
params = {
    'key': TRELLO_API_KEY,
    'token': TRELLO_TOKEN,
    'fields': 'name,desc,labels,dateLastActivity',
}

response = requests.get(TRELLO_API_URL, params=params)
cards = response.json()

release_notes = []

# Processer chaque carte et formater les informations
for card in cards:
    title = card.get('name', 'Sans titre')
    desc = card.get('desc', 'Pas de description')
    labels = ', '.join([label['name'] for label in card.get('labels', [])])
    last_activity = card.get('dateLastActivity', 'Inconnue')

    release_notes.append(f"### {title}\n\n**Labels**: {labels}\n\n**Dernière activité**: {last_activity}\n\n**Description**:\n{desc}\n\n---\n")

# Fusionner toutes les notes en une seule chaîne
release_notes_content = "\n".join(release_notes)

# Formater la date pour le titre de la release note
release_title = f"Release Note - {datetime.now().strftime('%Y-%m-%d')}"

# Récupérer l'ID de la liste "Releases"
lists_response = requests.get(TRELLO_LISTS_URL, params=params)
lists = lists_response.json()
list_id = None
for lst in lists:
    if lst['name'] == LIST_NAME:
        list_id = lst['id']
        break

if not list_id:
    raise ValueError(f"La liste '{LIST_NAME}' n'existe pas sur le board Trello.")

# Créer la carte "Release Note"
create_card_url = "https://api.trello.com/1/cards"
card_params = {
    'key': TRELLO_API_KEY,
    'token': TRELLO_TOKEN,
    'idList': list_id,
    'name': release_title,
    'desc': release_notes_content
}

create_card_response = requests.post(create_card_url, params=card_params)

if create_card_response.status_code == 200:
    print(f"Carte 'Release Note' créée avec succès : {release_title}")
else:
    print(f"Erreur lors de la création de la carte 'Release Note': {create_card_response.status_code}")
    print(create_card_response.text)
