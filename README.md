# Playlist Collab YouTube Music & Spotify

## Description
Ce projet est un script Python permettant de créer et gérer des playlists collaboratives entre YouTube Music et Spotify. Il offre la possibilité de récupérer des titres depuis l'une des plateformes et de les synchroniser avec l'autre, facilitant ainsi le partage et la découverte musicale entre utilisateurs de services différents.

## Fonctionnalités
- Connexion aux API de YouTube Music et Spotify.
- Extraction des playlists et des titres de chaque service.
- Synchronisation bidirectionnelle entre les plateformes.
- Gestion des doublons et des titres déjà présents.
- Options de personnalisation pour choisir les playlists à synchroniser.

## Technologies utilisées
- Python
- API YouTube Data v3
- API Spotify Web
- Bibliothèques : `requests`, `spotipy`, `pytube`

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/amtebb/playlist-collab-ytb-music-spor.git
   ```
2. Accédez au dossier du projet :
   ```bash
   cd playlist-collab-ytb-music-spor
   ```
3. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
1. Assurez-vous d'avoir configuré vos clés API pour YouTube et Spotify.
2. Modifiez le fichier `oauth.json` pour inclure vos identifiants d'API.
3. Exécutez le script principal :
   ```bash
   python main.py
   ```
4. Suivez les instructions affichées pour choisir les playlists et les options de synchronisation.

## Prérequis
- Python 3.7+
- Clés API pour YouTube Music et Spotify

## Configuration
Créez un fichier `config.py` et ajoutez les lignes suivantes :
```python
YOUTUBE_API_KEY = 'votre_clé_youtube'
SPOTIFY_CLIENT_ID = 'votre_client_id_spotify'
SPOTIFY_CLIENT_SECRET = 'votre_secret_spotify'
```
