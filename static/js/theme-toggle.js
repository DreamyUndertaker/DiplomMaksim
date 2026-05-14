// static/js/theme-toggle.js
(function() {
  'use strict';

  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const STORAGE_KEY = 'audiobookflow-theme';

  // Проверка сохранённой темы или системных предпочтений
  function getPreferredTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return saved;

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  // Применение темы
  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);

    // Обновляем состояние кнопки
    if (themeToggle) {
      themeToggle.setAttribute('aria-pressed', theme === 'dark');
    }

    // Сообщаем Telegram WebApp (если используется)
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.setHeaderColor(theme === 'dark' ? '#1a1a2e' : '#f8f9fa');
      window.Telegram.WebApp.setBackgroundColor(theme === 'dark' ? '#0f0f1a' : '#f8f9fa');
    }
  }

  // Инициализация при загрузке
  function init() {
    const theme = getPreferredTheme();
    applyTheme(theme);

    // Обработчик переключения
    if (themeToggle) {
      themeToggle.addEventListener('click', function() {
        const current = html.getAttribute('data-theme');
        const newTheme = current === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);

        // Плавный переход для визуального эффекта
        document.body.style.transition = 'background 0.25s ease, color 0.25s ease';
        setTimeout(() => {
          document.body.style.transition = '';
        }, 250);
      });
    }

    // Слушаем изменения системной темы
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!localStorage.getItem(STORAGE_KEY)) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }

  // Запуск после загрузки DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();