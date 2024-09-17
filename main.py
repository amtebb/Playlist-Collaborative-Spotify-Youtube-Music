from ytmusicapi import YTMusic
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import json 
import time
import requests
from datetime import datetime, timedelta 


client_id='ID CLIENT SPOT'
secret_client='SECRET CLIENT SPOT'
url_ytb="URL PLAYLIST YOUTUBE"
url_spot="URL PLAYLIST SPOT"

# création des app
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               secret_client,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-public"))


ytmusic = YTMusic("oauth.json")
id_playlist='test api'

def get_playlist_id_ytb(url):
    index = url.find('browse/')
    if index != -1:
        return url[index + len('browse/'):]
    else:
        return False
def get_playlist_id_spot(url):
    index=url.find('playlist/')
    if index !=-1:
        return url[index+len('playlist/'):]
    else:
        return False
id_spot=get_playlist_id_spot(url_spot)
id_ytb=get_playlist_id_ytb(url_ytb)
def get_spotify_tracks(spotify_playlist_id):
    results = sp.playlist_tracks(spotify_playlist_id)
    tracks = set()
    for item in results['items']:
        track_name = item['track']['name']  # Nom de la piste
        artists = tuple(artist['name'] for artist in item['track']['artists'])  # Liste des artistes sous forme de tuple
        tracks.add((track_name, artists))  # Ajouter un tuple (nom de la piste, artistes) au set
    return tracks

def get_youtube_tracks(youtube_playlist_id):
    # Récupère les informations de la playlist via l'instance existante de YTMusic
    playlist = ytmusic.get_playlist(youtube_playlist_id)
    
    tracks = set()
    
    # Parcourir chaque élément de la playlist
    for item in playlist['tracks']:
        track_name = item['title']  # Nom de la piste
        artists = tuple(artist['name'] for artist in item['artists'])  # Liste des artistes sous forme de tuple
        tracks.add((track_name, artists))  # Ajoute un tuple (nom de la piste, artistes) au set
        
    return tracks
def search_track_spot(info):
    query = f"track:{info[0]} artist:{' '.join(info[1])}"
    result = sp.search(q=query, type='track', limit=1)
    
    if result['tracks']['items']:
        return result['tracks']['items'][0]['uri']  # Récupère l'URI de la première piste trouvée
    return None

def add_track_spot(track_uri):
    sp.playlist_add_items(id_spot, [track_uri])


def search_track_youtube(info):
    query = f"{info[0]} {' '.join(info[1])}"
    search_results = ytmusic.search(query, filter="songs", limit=1)
    
    if search_results:
        return search_results[0]['videoId']  # Récupère l'ID de la première vidéo trouvée
    return None


def add_track_to_youtube_playlist(video_id):
    ytmusic.add_playlist_items(id_ytb, [video_id])




# execution du programme 


new_spot_playlist=get_spotify_tracks(id_spot)
new_youtube_playlst=get_youtube_tracks(id_ytb)


def save_playlists_to_file(spotify_set, youtube_set, filename="playlists.json"):
    data = {
        "spotify": list(spotify_set),  # Convertir le set en liste pour JSON
        "youtube": list(youtube_set)
    }
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_playlists_from_file(filename="playlists.json"):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            # Convertir les sous-listes (artistes) en tuples pour pouvoir créer des sets
            spotify_set = set((track[0], tuple(track[1])) for track in data["spotify"])
            youtube_set = set((track[0], tuple(track[1])) for track in data["youtube"])
            return spotify_set, youtube_set
    except FileNotFoundError:
        # Si le fichier n'existe pas, on retourne des sets vides
        return set(), set()

old_spot_playlist, old_ytb_playlist = load_playlists_from_file()

def synchro_playlist():
    add_spotify = new_youtube_playlst-old_ytb_playlist
    add_youtube= new_spot_playlist-old_spot_playlist

    supp_spotify = old_ytb_playlist-new_youtube_playlst
    supp_ytb=old_spot_playlist-new_spot_playlist

    for info in add_spotify:
        track_uri = search_track_spot(info)  # Rechercher la piste sur Spotify
        if track_uri:
            add_track_spot(track_uri)  # Ajouter la piste à Spotify
            print(f"Ajouté à Spotify : {info[0]} par {', '.join(info[1])}")
        else:
            print(f"Piste introuvable sur Spotify : {info[0]} par {', '.join(info[1])}")

    # Ajouter des titres à YouTube
    for info in add_youtube:
        video_id = search_track_youtube(info)  # Rechercher la piste sur YouTube
        if video_id:
            add_track_to_youtube_playlist(video_id)  # Ajouter la piste à YouTube
            print(f"Ajouté à YouTube : {info[0]} par {', '.join(info[1])}")
        else:
            print(f"Piste introuvable sur YouTube : {info[0]} par {', '.join(info[1])}")

    # Supprimer des titres de Spotify
    for info in supp_spotify:
        track_uri = search_track_spot(info)  # Rechercher la piste sur Spotify pour la supprimer
        if track_uri:
            sp.playlist_remove_all_occurrences_of_items(id_spot, [track_uri])  # Supprimer de Spotify
            print(f"Supprimé de Spotify : {info[0]} par {', '.join(info[1])}")
        else:
            print(f"Piste introuvable sur Spotify pour suppression : {info[0]} par {', '.join(info[1])}")

    # Supprimer des titres de YouTube
    current_youtube_videos = {track['videoId'] for track in ytmusic.get_playlist(id_ytb)['tracks']}

    # Supprimer des titres de YouTube
    for info in supp_ytb:
        video_id = search_track_youtube(info)  # Rechercher la piste sur YouTube pour la suppression
        if video_id and video_id in current_youtube_videos:  # Vérifie que la vidéo est encore dans la playlist
            ytmusic.remove_playlist_items(id_ytb, [video_id])  # Supprimer de YouTube
            print(f"Supprimé de YouTube : {info[0]} par {', '.join(info[1])}")
        else:
            print(f"Piste introuvable ou déjà supprimée de YouTube : {info[0]} par {', '.join(info[1])}")


     # Actualiser les sets après la synchronisation
    old_spot_playlist.update(add_spotify)  # Ajouter les nouveaux titres à l'ancien set
    old_spot_playlist.difference_update(supp_spotify)  # Retirer les titres supprimés

    old_ytb_playlist.update(add_youtube)
    old_ytb_playlist.difference_update(supp_ytb)
    save_playlists_to_file(old_spot_playlist, old_ytb_playlist)




def test_internet():
    try:
        requests.get("https://www.google.com", timeout=20)
        return True
    except requests.ConnectionError:
        return False

def run_check_connexion(break_hour=2):
    start_time=datetime.now()
    max_duration = timedelta(hours=break_hour)
    end_time = start_time + max_duration

    while datetime.now() < end_time:
        if test_internet:
            print("La connexion est disponible")
            synchro_playlist()
            print("Synchronisation effectuée")
            return True
        else:
            print("pas de connexion : réssai dans 5 minutes")
            time.sleep(60*5)
    print("La synchronisation n'a pas été effectué")
    return False





