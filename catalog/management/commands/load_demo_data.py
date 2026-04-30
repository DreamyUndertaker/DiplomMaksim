# catalog/management/commands/load_demo_data.py
import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from catalog.models import Author, Genre, Audiobook, Chapter
from player.models import Playlist
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Загружает демо-данные для тестирования AudiobookFlow'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Очистить существующие данные перед загрузкой')
        parser.add_argument('--users', type=int, default=3, help='Количество тестовых пользователей')

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('🗑️  Очистка существующих данных...')
            Chapter.objects.all().delete()
            Audiobook.objects.all().delete()
            Genre.objects.all().delete()
            Author.objects.all().delete()
            Playlist.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('✓ Данные очищены'))

        self.stdout.write('🚀 Начинаем загрузку демо-данных...')

        # === Жанры ===
        genres_data = [
            ('Фантастика', 'sci-fi', 'Мир будущего, технологии, космос'),
            ('Детектив', 'detective', 'Загадки, расследования, интриги'),
            ('Фэнтези', 'fantasy', 'Магия, драконы, эпические приключения'),
            ('Роман', 'romance', 'Любовные истории и чувства'),
            ('Бизнес', 'business', 'Финансы, карьера, саморазвитие'),
            ('Психология', 'psychology', 'Понимание себя и отношений'),
            ('История', 'history', 'События прошлого и биографии'),
            ('Приключения', 'adventure', 'Путешествия и экшен'),
        ]

        genres = {}
        for name, slug, desc in genres_data:
            genre, _ = Genre.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': desc}
            )
            genres[name] = genre
            self.stdout.write(f'  ✓ Жанр: {name}')

        # === Авторы ===
        authors_data = [
            ('Айзек Азимов', 'Классик научной фантастики, автор цикла «Основание»'),
            ('Агата Кристи', 'Королева детектива, создательница Эркюля Пуаро'),
            ('Дж. Р. Р. Толкин', 'Отец современного фэнтези, автор «Властелина Колец»'),
            ('Дейл Карнеги', 'Автор бестселлеров по саморазвитию и коммуникации'),
            ('Михаил Лабковский', 'Практикующий психолог, эксперт по отношениям'),
            ('Юваль Ной Харари', 'Историк, автор «Sapiens» и «Homo Deus»'),
        ]

        authors = {}
        for name, bio in authors_data:
            author, _ = Author.objects.get_or_create(
                name=name,
                defaults={'bio': bio}
            )
            authors[name] = author
            self.stdout.write(f'  ✓ Автор: {name}')

        # === Аудиокниги ===
        books_data = [
            {
                'title': 'Основание',
                'author': authors['Айзек Азимов'],
                'genres': [genres['Фантастика']],
                'description': 'Эпическая сага о падении Галактической Империи и попытке сохранить знания цивилизации.',
                'year': 1951,
                'chapters': [
                    ('Психоисторики', 420),
                    ('Энциклопедисты', 380),
                    ('Мэры', 450),
                    ('Торговцы', 410),
                    ('Купцы', 390),
                ]
            },
            {
                'title': 'Убийство в «Восточном экспрессе»',
                'author': authors['Агата Кристи'],
                'genres': [genres['Детектив']],
                'description': 'Знаменитое расследование Эркюля Пуаро в запертом вагоне поезда.',
                'year': 1934,
                'chapters': [
                    ('Важный пассажир', 320),
                    ('Ночь в вагоне', 290),
                    ('Расследование начинается', 410),
                    ('Подозреваемые', 380),
                    ('Разгадка', 450),
                ]
            },
            {
                'title': 'Хоббит, или Туда и обратно',
                'author': authors['Дж. Р. Р. Толкин'],
                'genres': [genres['Фэнтези'], genres['Приключения']],
                'description': 'Невероятное путешествие Бильбо Бэггинса к Одинокой Горе.',
                'year': 1937,
                'chapters': [
                    ('Нежданные гости', 480),
                    ('Баранье жаркое', 420),
                    ('Короткий отдых', 390),
                    ('Через горы и под горами', 510),
                    ('Загадки в темноте', 440),
                    ('Из огня да в полымя', 470),
                ]
            },
            {
                'title': 'Как завоевывать друзей',
                'author': authors['Дейл Карнеги'],
                'genres': [genres['Бизнес'], genres['Психология']],
                'description': 'Классика деловой литературы о эффективном общении и влиянии.',
                'year': 1936,
                'chapters': [
                    ('Введение', 280),
                    ('Фундаментальные техники', 350),
                    ('Шесть способов понравиться', 420),
                    ('Как склонить людей к своей точке зрения', 480),
                    ('Быть лидером', 390),
                ]
            },
            {
                'title': 'Sapiens: Краткая история человечества',
                'author': authors['Юваль Ной Харари'],
                'genres': [genres['История'], genres['Психология']],
                'description': 'Увлекательное путешествие по истории нашего вида от каменного века до наших дней.',
                'year': 2011,
                'chapters': [
                    ('Революция познания', 520),
                    ('Древо познания', 480),
                    ('Один день из жизни Адама и Евы', 410),
                    ('Наводнение', 450),
                    ('История обмана', 490),
                    ('Строители пирамид', 430),
                ]
            },
        ]

        for book_info in books_data:
            audiobook, created = Audiobook.objects.get_or_create(
                title=book_info['title'],
                defaults={
                    'author': book_info['author'],
                    'description': book_info['description'],
                    'publication_year': book_info['year'],
                    'is_published': True,
                }
            )
            audiobook.genres.set(book_info['genres'])

            # Создаём главы
            for i, (chapter_title, duration) in enumerate(book_info['chapters'], 1):
                Chapter.objects.get_or_create(
                    audiobook=audiobook,
                    number=i,
                    defaults={
                        'title': chapter_title,
                        'duration': duration,
                        # В реальном проекте здесь будет путь к аудиофайлу
                        'audio_file': f'demo/chapters/{audiobook.id}_{i}.mp3'
                    }
                )

            # Обновляем общую длительность
            audiobook.update_duration()
            self.stdout.write(f'  ✓ Книга: {book_info["title"]} ({len(book_info["chapters"])} глав)')

        # === Тестовые пользователи ===
        num_users = options['users']
        for i in range(1, num_users + 1):
            username = f'test_user_{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'is_active': True
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
                self.stdout.write(f'  ✓ Пользователь: {username} (пароль: demo123)')

        # === Демо-плейлисты ===
        test_user = User.objects.filter(username='test_user_1').first()
        if test_user:
            playlist, _ = Playlist.objects.get_or_create(
                user=test_user,
                title='Избранное на вечер',
                defaults={'description': 'Книги для спокойного вечера'}
            )
            # Добавляем первые главы всех книг в плейлист
            for audiobook in Audiobook.objects.all()[:3]:
                first_chapter = audiobook.chapters.first()
                if first_chapter:
                    from player.models import PlaylistItem
                    PlaylistItem.objects.get_or_create(
                        playlist=playlist,
                        chapter=first_chapter,
                        defaults={'order': playlist.items.count()}
                    )
            self.stdout.write(f'  ✓ Плейлист для {test_user.username}')

        # === Итог ===
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('✅ Загрузка демо-данных завершена!'))
        self.stdout.write(f'  • Жанров: {Genre.objects.count()}')
        self.stdout.write(f'  • Авторов: {Author.objects.count()}')
        self.stdout.write(f'  • Аудиокниг: {Audiobook.objects.count()}')
        self.stdout.write(f'  • Глав: {Chapter.objects.count()}')
        self.stdout.write(f'  • Пользователей: {User.objects.filter(is_superuser=False).count()}')
        self.stdout.write('=' * 50)
        self.stdout.write('\n🔐 Для входа используйте:')
        self.stdout.write('  Логин: test_user_1 / Пароль: demo123')
        self.stdout.write('  Или создайте своего пользователя через /admin/')