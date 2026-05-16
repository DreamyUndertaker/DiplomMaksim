# 🎧 AudiobookFlow

> Веб-сервис для каталогизации и прослушивания аудиокниг

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20.svg)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 О проекте

**AudiobookFlow** — кроссплатформенный веб-сервис для прослушивания аудиокниг без установки дополнительных приложений.

### ✨ Ключевые особенности
- 🔐 Безопасная авторизация и защита контента
- 🔄 Синхронизация прогресса между устройствами
- 📱 Адаптивный дизайн (Desktop/Tablet/Mobile)
- 🎛 Кастомный аудиоплеер с управлением скоростью
- 📚 Система плейлистов, избранного и рецензий

### 💰 Экономика
| Показатель | Значение |
|-----------|----------|
| Стоимость подписки | 179 ₽/мес |
| Срок окупаемости | ~5 месяцев |
| Затраты на разработку | 120 500 ₽ |

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.10+
- PostgreSQL 14+
- Docker & Docker Compose (опционально)

### Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/yourusername/AudiobookFlow.git
cd AudiobookFlow

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Настройте переменные окружения
cp .env.example .env
# Отредактируйте .env с вашими параметрами

# Примените миграции
python manage.py migrate

# Запустите сервер разработки
python manage.py runserver
