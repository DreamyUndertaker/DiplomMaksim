// static/js/player.js
class Audioplayer {
  constructor(options) {
    this.bookId = options.bookId;
    this.csrfToken = options.csrfToken;

    this.audio = document.getElementById('audioElement');
    this.playerEl = document.getElementById('audioplayer');
    this.playPauseBtn = document.getElementById('playPauseBtn');
    this.prevBtn = document.getElementById('prevBtn');
    this.nextBtn = document.getElementById('nextBtn');
    this.progressBar = document.getElementById('progressBar');
    this.progressFill = document.getElementById('progressFill');
    this.currentTimeEl = document.getElementById('currentTime');
    this.durationEl = document.getElementById('duration');
    this.chapterInfoEl = document.getElementById('currentChapter');
    this.playbackRateEl = document.getElementById('playbackRate');

    this.currentChapterId = null;
    this.currentChapterData = null;
    this.saveInterval = null;
    this.chapters = []; // Заполняется при инициализации

    this.initEventListeners();
  }

  initEventListeners() {
    // Кнопки управления
    this.playPauseBtn.addEventListener('click', () => this.togglePlayPause());
    this.prevBtn.addEventListener('click', () => this.playPrevious());
    this.nextBtn.addEventListener('click', () => this.playNext());

    // Прогресс-бар
    this.progressBar.addEventListener('click', (e) => this.seek(e));

    // События аудио
    this.audio.addEventListener('timeupdate', () => this.updateProgress());
    this.audio.addEventListener('loadedmetadata', () => this.updateDuration());
    this.audio.addEventListener('ended', () => this.onChapterEnd());
    this.audio.addEventListener('error', (e) => this.onError(e));

    // Скорость воспроизведения
    this.playbackRateEl.addEventListener('change', (e) => {
      this.audio.playbackRate = parseFloat(e.target.value);
    });

    // Автосохранение прогресса каждые 30 сек
    this.audio.addEventListener('play', () => this.startAutoSave());
    this.audio.addEventListener('pause', () => this.stopAutoSave());
  }

  async loadChapter(chapterId) {
    try {
      // Показываем плеер
      this.playerEl.classList.add('active');

      // Получаем информацию о главе
      const chapterEl = document.querySelector(`[data-chapter-id="${chapterId}"]`);
      const chapterTitle = chapterEl?.querySelector('strong')?.nextSibling?.textContent?.trim() || `Глава ${chapterId}`;
      const duration = parseInt(chapterEl?.dataset.duration || 0);

      this.currentChapterId = chapterId;
      this.currentChapterData = { title: chapterTitle, duration };
      this.chapterInfoEl.textContent = chapterTitle;

      // Загружаем сохранённую позицию
      const progress = await this.fetchProgress(chapterId);

      // Загружаем аудио
      this.audio.src = `/player/stream/${chapterId}/`;
      this.audio.currentTime = progress.position || 0;

      // Обновляем отображение
      this.updateDuration();
      this.play();

    } catch (error) {
      console.error('Ошибка загрузки главы:', error);
      alert('Не удалось загрузить аудио. Попробуйте позже.');
    }
  }

  async fetchProgress(chapterId) {
    try {
      const response = await fetch(`/player/api/progress/${chapterId}/get/`);
      return await response.json();
    } catch {
      return { position: 0, percentage: 0 };
    }
  }

  async saveProgress(position, isFinished = false) {
    if (!this.currentChapterId) return;

    try {
      await fetch(`/player/api/progress/${this.currentChapterId}/save/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.csrfToken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          position: Math.floor(position),
          finished: isFinished
        })
      });
    } catch (error) {
      console.warn('Не удалось сохранить прогресс:', error);
    }
  }

  play() {
    this.audio.play().then(() => {
      this.playPauseBtn.textContent = '⏸';
    }).catch(err => {
      console.error('Ошибка воспроизведения:', err);
    });
  }

  pause() {
    this.audio.pause();
    this.playPauseBtn.textContent = '▶';
  }

  togglePlayPause() {
    if (this.audio.paused) {
      this.play();
    } else {
      this.pause();
    }
  }

  seek(event) {
    const rect = this.progressBar.getBoundingClientRect();
    const percent = (event.clientX - rect.left) / rect.width;
    this.audio.currentTime = percent * this.audio.duration;
  }

  updateProgress() {
    const percent = (this.audio.currentTime / this.audio.duration) * 100;
    this.progressFill.style.width = `${percent}%`;
    this.currentTimeEl.textContent = this.formatTime(this.audio.currentTime);
  }

  updateDuration() {
    if (this.audio.duration) {
      this.durationEl.textContent = this.formatTime(this.audio.duration);
    } else if (this.currentChapterData?.duration) {
      this.durationEl.textContent = this.formatTime(this.currentChapterData.duration);
    }
  }

  startAutoSave() {
    if (this.saveInterval) clearInterval(this.saveInterval);
    this.saveInterval = setInterval(() => {
      this.saveProgress(this.audio.currentTime);
    }, 30000); // Каждые 30 секунд
  }

  stopAutoSave() {
    if (this.saveInterval) {
      clearInterval(this.saveInterval);
      this.saveInterval = null;
    }
    // Сохраняем текущую позицию при паузе
    if (this.currentChapterId) {
      this.saveProgress(this.audio.currentTime);
    }
  }

  async onChapterEnd() {
    // Отмечаем как прослушанную
    await this.saveProgress(this.audio.duration, true);

    // Автопереход к следующей главе (опционально)
    // this.playNext();
  }

  onError(event) {
    console.error('Ошибка аудио:', event);
    alert('Ошибка загрузки аудиофайла. Проверьте соединение.');
    this.pause();
  }

  playPrevious() {
    // Логика перехода к предыдущей главе
    // Можно расширить: искать предыдущую главу в списке
    console.log('Previous chapter');
  }

  playNext() {
    // Логика перехода к следующей главе
    const nextBtn = document.querySelector(`[data-chapter-id="${this.currentChapterId}"]`)?.nextElementSibling;
    const nextChapterId = nextBtn?.dataset?.chapterId;
    if (nextChapterId) {
      this.loadChapter(nextChapterId);
    }
  }

  formatTime(seconds) {
    if (!seconds || isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  destroy() {
    this.stopAutoSave();
    this.audio.pause();
    this.audio.src = '';
    this.playerEl?.classList.remove('active');
  }
}