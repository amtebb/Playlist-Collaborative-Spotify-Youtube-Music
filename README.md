# Playlist Collab YouTube Music & Spotify

## Description
Ce projet est un script Python permettant de créer et gérer des playlists collaboratives entre YouTube Music et Spotify. Il offre la possibilité de faire une playlist collaborative entre un.e utilisateur.rice de spotify et de youtube music.

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
2. Modifiez le fichier `oauth.json` pour inclure vos identifiants d'API Youtube Music.
3. Au début du fichier `main.py` vous pouvez inserer vos identifiants d'API Spotify ainsi que les urls de la playlist spotify et Youtube Music. 
4. Exécutez le script principal :
   ```bash
   python exe.py
   ```
5. Lancez le fichier `exe.py` pour faire la synchronisation. Vous pouvez définir une tache sur votre PC pour lancer la synchronisation aux heures qui vous arrangent (attention à la limite de requetes API)
6. Si il n'y a pas de connexion, le programme tentera la synchronisation périodiquement pendant 2 heures. 

## Prérequis
- Python 3.7+
- Clés API pour YouTube Music et Spotify


