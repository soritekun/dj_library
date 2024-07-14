from django.shortcuts import render
from django.http import JsonResponse
from .models import Song
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from rest_framework.decorators import api_view

def get_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID, client_secret=settings.SPOTIFY_CLIENT_SECRET)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_recommendations(track_ids, num_recommendations):
    spotify = get_spotify_client()
    recommendations = spotify.recommendations(seed_tracks=track_ids,limit=num_recommendations)
    recommended_tracks = []
    
    for track in recommendations['tracks']:
        track_id = track['id']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        features = spotify.audio_features(track_id)[0]
        
        recommended_tracks.append({
            'id': track_id,
            'name': track_name,
            'artist': artist_name,
            'danceability': features['danceability'],
            'energy': features['energy'],
            'key': features['key'],
            'loudness': features['loudness'],
            'mode': features['mode'],
            'speechiness': features['speechiness'],
            'acousticness': features['acousticness'],
            'instrumentalness': features['instrumentalness'],
            'liveness': features['liveness'],
            'valence': features['valence'],
            'tempo': features['tempo']
        })
        
    return recommended_tracks
    
@api_view(['POST'])
def search_songs(request):
    if request.method == 'POST':
        query = request.data.get('query', '')
        if query == None:
            return JsonResponse({'error': 'None'}, status=400)
        spotify = get_spotify_client()
        results = spotify.search(q=query, type='track', limit=3)
        tracks = [{
            'id':item['id'],
            'name':item['name'],
            'artist':item['artists'][0]['name']
        }for item in results['tracks']['items']]
        return JsonResponse(tracks, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@api_view(['POST'])
def save_selected_songs(request):
    if request.method == 'POST':
        playlist_name = request.data.get('playlist_name', '')
        selected_songs = request.data.getlist('selected_songs', [])
        
        if not playlist_name or not selected_songs:
            return JsonResponse({'error': "プレイリストの名前、もしくは歌の入力がまだです"}, status = 400)
            
        
        spotify = get_spotify_client()
        track_ids = []
        for song_id in selected_songs:
            track = spotify.track(song_id)
            features = spotify.audio_features(song_id)[0]
            
            track_f = [
                song_id,
                track['name'],
                track['artists'][0]['name'],
                features['danceability'],
                features['energy'],
                features['key'],
                features['loudness'],
                features['mode'],
                features['speechiness'],
                features['acousticness'],
                features['instrumentalness'],
                features['liveness'],
                features['valence'],
                features['tempo']
            ]
            # song, created = Song.objects.get_or_create(
            #     id=track_f[0],
            #     name=track_f[1],
            #     artist=track_f[2],
            #     danceability=track_f[3],
            #     energy=track_f[4],
            #     key=track_f[5],
            #     loudness=track_f[6],
            #     mode=track_f[7],
            #     speechiness=track_f[8],
            #     acousticness=track_f[9],
            #     instrumentalness=track_f[10],
            #     liveness=track_f[11],
            #     valence=track_f[12],
            #     tempo=track_f[13]
            # )
            
            if "playlists" not in request.session:
                request.session['playlists'] = {}
            if playlist_name not in request.session['playlists']:
                request.session['playlists'][playlist_name] = []
            request.session['playlists'][playlist_name].append(track_f)
            track_ids.append(song_id)
        
        recommended_tracks = get_recommendations(track_ids, 10)#第二引数おすすめの数
        
        for track in recommended_tracks:
            # track_id = track.pop('id')
            # song, created=Song.objects.get_or_create(
            #     id=track_id,
            #     defaults=track
            # )
            request.session['playlists'][playlist_name].append(track)
        return JsonResponse(recommended_tracks, status=201, safe = False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@api_view(['GET'])
def get_playlists(request):
    playlists = request.session.get('playlists', {})
    return JsonResponse(playlists, safe = False)
    
@api_view(['GET'])
def get_track(request, playlist_name):
    playlists = request.session.get('playlists', {})
    playlist = playlists.get(playlist_name, [])
    
    if not playlist:
        return JsonResponse({"error":"プレイリストが見つかりませんでした"}, status = 404)
        
    return JsonResponse(playlist, safe = False)