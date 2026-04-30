# player/views.py
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from catalog.models import Chapter
from .models import UserProgress, Playlist, PlaylistItem
import os
from django.conf import settings
import json


@login_required
@require_POST
def save_progress(request, chapter_id):
    """Сохраняет позицию прослушивания"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        position = int(data.get('position', 0))
        is_finished = str(data.get('finished', 'false')).lower() == 'true'

        chapter = get_object_or_404(Chapter, id=chapter_id, audiobook__is_published=True)

        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            chapter=chapter,
            defaults={'position_seconds': position}
        )

        if not created:
            progress.position_seconds = position
            progress.is_finished = is_finished
            progress.save(update_fields=['position_seconds', 'is_finished', 'last_listened_at'])

        return JsonResponse({
            'status': 'saved',
            'position': position,
            'percentage': progress.get_percentage() if hasattr(progress, 'get_percentage') else 0
        })
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        return JsonResponse({'error': f'Invalid data: {str(e)}'}, status=400)


@login_required
@require_GET
def get_progress(request, chapter_id):
    """Возвращает сохранённую позицию для главы"""
    chapter = get_object_or_404(Chapter, id=chapter_id)
    progress = UserProgress.objects.filter(
        user=request.user,
        chapter=chapter
    ).first()

    if progress:
        return JsonResponse({
            'position': progress.position_seconds,
            'percentage': progress.get_percentage(),
            'is_finished': progress.is_finished
        })
    return JsonResponse({'position': 0, 'percentage': 0, 'is_finished': False})


@login_required
@require_POST
def toggle_playlist_item(request, playlist_id, chapter_id):
    """Добавляет/удаляет главу из плейлиста"""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    chapter = get_object_or_404(Chapter, id=chapter_id)

    item, created = PlaylistItem.objects.get_or_create(
        playlist=playlist,
        chapter=chapter,
        defaults={'order': playlist.items.count()}
    )

    if not created:
        item.delete()
        return JsonResponse({'action': 'removed', 'playlist_id': playlist_id})

    return JsonResponse({
        'action': 'added',
        'playlist_id': playlist_id,
        'item_id': item.id,
        'order': item.order
    })


@login_required
@require_GET
def stream_chapter(request, chapter_id):
    """Защищённая отдача аудиофайла"""
    chapter = get_object_or_404(Chapter, id=chapter_id, audiobook__is_published=True)

    # Проверка: существует ли файл физически
    if not os.path.exists(chapter.audio_file.path):
        placeholder = os.path.join(settings.MEDIA_ROOT, 'demo', 'chapters', 'placeholder.mp3')
        if os.path.exists(placeholder):
            response = FileResponse(open(placeholder, 'rb'), content_type='audio/mpeg')
            response['Content-Length'] = os.path.getsize(placeholder)
            return response
        else:
            return JsonResponse({
                'error': 'Audio file not found',
                'chapter_id': chapter_id,
                'expected_path': chapter.audio_file.path
            }, status=404)

    # Основной поток: отдаём реальный файл
    response = FileResponse(
        open(chapter.audio_file.path, 'rb'),
        content_type='audio/mpeg'
    )
    response['Content-Length'] = os.path.getsize(chapter.audio_file.path)
    return response