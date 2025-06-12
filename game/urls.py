from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_game, name='create_game'),
    path('join/<uuid:game_code>/', views.join_game, name='join_game'),
    path('play/<int:player_id>/', views.play_game, name='play_game'),
    path('waiting/<uuid:game_code>/', views.waiting_room, name='waiting_room'),
    path('check_players/<uuid:game_code>/', views.check_players, name='check_players'),
    path('winner/<int:game_id>/', views.winner, name='winner'), 
]
