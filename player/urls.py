# player/urls.py
from django.urls import path
from . import views

app_name = 'player'

urlpatterns = [
    # API для сохранения/получения прогресса
    path('api/progress/<int:chapter_id>/save/', views.save_progress, name='save_progress'),
    path('api/progress/<int:chapter_id>/get/', views.get_progress, name='get_progress'),

    # Управление плейлистами
    path('api/playlist/<int:playlist_id>/toggle/<int:chapter_id>/', views.toggle_playlist_item, name='toggle_playlist'),

    # Защищённая отдача аудио
    path('stream/<int:chapter_id>/', views.stream_chapter, name='stream_chapter'),
]