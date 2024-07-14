from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('search/', views.search_songs, name='search_songs'),
   path('save/', views.save_selected_songs, name='save_selected_songs'),
   path('lists/', views.get_playlists, name='get_playlists'),
   path('lists/<str:playlist_name>/', views.get_track, name='get_track')
]
