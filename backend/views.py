from django.shortcuts import render
from django.http import JsonResponse
from .models import Song

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


SPOTIFY_CLIENT_ID = 'YOUR_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

def get_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_songs(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        spotify = get_spotify_client()
        results = spotify.search(q=query, type='track', limit=10)
        return JsonResponse(results['tracks']['items'], safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def save_selected_songs(request):
    if request.method == 'POST':
        selected_songs = request.POST.getlist('selected_songs[]')
        spotify = get_spotify_client()

        for song_id in selected_songs:
            track = spotify.track(song_id)
            features = spotify.audio_features(song_id)[0]

            Song.objects.create(
                id=song_id,
                name=track['name'],
                artist=track['artists'][0]['name'],
                danceability=features['danceability'],
                energy=features['energy'],
                key=features['key'],
                loudness=features['loudness'],
                mode=features['mode'],
                speechiness=features['speechiness'],
                acousticness=features['acousticness'],
                instrumentalness=features['instrumentalness'],
                liveness=features['liveness'],
                valence=features['valence'],
                tempo=features['tempo']
            )

        return JsonResponse({'message': 'Selected songs saved successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=400)