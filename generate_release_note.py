import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from git import Repo  # Import GitPython's Repo

load_dotenv()

# Chargement des variables d'environnement
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_API_TOKEN')  
BOARD_ID = os.getenv('TRELLO_BOARD_ID')
LIST_NAME = "Releases"  # Nom de la liste où la carte sera ajoutée

TRELLO_LISTS_URL = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"
TRELLO_CARDS_URL = "https://api.trello.com/1/cards"

params = {
    'key': TRELLO_API_KEY,
    'token': TRELLO_TOKEN,
}

headers = {
    'Authorization': f'Bearer {TRELLO_TOKEN}',
}

try:
    # Récupérer l'ID de la liste "Releases"
    lists_response = requests.get(TRELLO_LISTS_URL, params=params, headers=headers)
    lists_response.raise_for_status()

    lists = lists_response.json()

    list_id = None
    for lst in lists:
        if lst['name'] == LIST_NAME:
            list_id = lst['id']
            break

    if not list_id:
        raise ValueError(f"La liste '{LIST_NAME}' n'existe pas sur le board Trello.")

    # Récupérer le nom du dernier commit et sa description
    repo = Repo(search_parent_directories=True)
    last_commit = repo.head.commit
    commit_name = last_commit.message.split('\n')[0]
    commit_description = "\n".join(last_commit.message.split('\n')[1:])
    commit_author = last_commit.author.name
    commit_date = last_commit.authored_datetime.strftime('%Y-%m-%d')
    commit_time = last_commit.authored_datetime.strftime('%H:%M')
    
    # Extraire les 7 premiers caractères du numéro de commit
    short_commit_hash = last_commit.hexsha[:7]

    # Créer une carte dans la liste "Releases" avec la description du commit
    release_title = f"Release Note - {commit_date} {commit_time} - {commit_author}"
    create_card_params = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idList': list_id,
        'name': release_title,
        'desc': (
            f"**Commit N°** {short_commit_hash}\n\n"
            f"**Auteur du commit:** {commit_author}\n\n"
            f"**Date du commit:** {commit_date}\n\n"
            f"**Heure du commit:** {commit_time}\n\n"
            f"**Description commit:** {commit_name}\n\n{commit_description}"
        ) if commit_name else ""
    }

    create_card_response = requests.post(TRELLO_CARDS_URL, params=create_card_params)
    create_card_response.raise_for_status()

    print(f"Carte 'Release Note' créée avec succès : {release_title}")

except requests.exceptions.RequestException as e:
    print(f"Une erreur s'est produite lors de la requête HTTP : {e}")

except ValueError as ve:
    print(ve)

except Exception as ex:
    print(f"Une erreur inattendue s'est produite : {ex}")