# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from player.models import UserProgress, Playlist


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:book_list')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect('catalog:book_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:book_list')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"С возвращением, {user.username}!")
            next_url = request.GET.get('next', 'catalog:book_list')
            return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта")
    return redirect('catalog:book_list')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    # Получаем историю прослушиваний (последние 10)
    recent_progress = UserProgress.objects.filter(
        user=request.user
    ).select_related('chapter__audiobook').order_by('-last_listened_at')[:10]

    # Получаем плейлисты
    playlists = Playlist.objects.filter(user=request.user).prefetch_related('items')

    return render(request, 'accounts/profile.html', {
        'form': form,
        'recent_progress': recent_progress,
        'playlists': playlists
    })