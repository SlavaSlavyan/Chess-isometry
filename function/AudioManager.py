import pygame
import os
import random
import sys

class AudioManager:
    
    def __init__(self, m):
        pygame.mixer.init()
        
        # Загружаем настройки из конфига
        self.music_volume = m.config.get('music_volume', 0.5)
        self.sfx_volume = m.config.get('sfx_volume', 0.7)
        self.music_playing = False
        
        # Список музыкальных файлов
        self.music_files = []
        self.current_track_index = 0
        
        # Звуковые эффекты
        self.sfx_sounds = {}
        
        # Загружаем музыку и звуки
        self.load_music()
        self.load_sfx()
        
    def get_resource_path(self, relative_path):
        """Получить абсолютный путь к ресурсу, работает как в разработке, так и в PyInstaller"""
        if hasattr(sys, '_MEIPASS'):
            # Запущено из PyInstaller
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            # Запущено в обычном режиме
            return relative_path
        
    def load_music(self):
        """Загружает все музыкальные файлы из папки data/audio/"""
        audio_dir = self.get_resource_path("data/audio/")
        if not os.path.exists(audio_dir):
            return
            
        # Поддерживаемые форматы
        supported_formats = ['.ogg', '.mp3', '.wav']
        
        # Ищем все музыкальные файлы
        for file in os.listdir(audio_dir):
            if any(file.lower().endswith(fmt) for fmt in supported_formats):
                full_path = os.path.join(audio_dir, file)
                self.music_files.append(full_path)
        
        if self.music_files:
            # Перемешиваем список для рандомного порядка
            random.shuffle(self.music_files)
            print(f"Найдено {len(self.music_files)} музыкальных файлов")
            self.start_music()
        else:
            print("Музыкальные файлы не найдены")
    
    def start_music(self):
        """Запускает текущий музыкальный трек"""
        if not self.music_files:
            return
            
        try:
            current_track = self.music_files[self.current_track_index]
            pygame.mixer.music.load(current_track)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play()  # Играем один раз, потом переключимся
            self.music_playing = True
            
            # Выводим название текущего трека
            track_name = os.path.basename(current_track)
            print(f"♪ Играет: {track_name}")
            
        except pygame.error as e:
            print(f"Ошибка воспроизведения музыки: {e}")
            self.next_track()  # Пробуем следующий трек
    
    def stop_music(self):
        """Останавливает музыку"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def set_music_volume(self, volume):
        """Устанавливает громкость музыки (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Устанавливает громкость звуковых эффектов"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def next_track(self):
        """Переключается на следующий трек"""
        if not self.music_files:
            return
            
        self.current_track_index = (self.current_track_index + 1) % len(self.music_files)
        if self.music_playing:
            self.start_music()
    
    def previous_track(self):
        """Переключается на предыдущий трек"""
        if not self.music_files:
            return
            
        self.current_track_index = (self.current_track_index - 1) % len(self.music_files)
        if self.music_playing:
            self.start_music()
    
    def shuffle_playlist(self):
        """Перемешивает плейлист"""
        if self.music_files:
            current_track = self.music_files[self.current_track_index]
            random.shuffle(self.music_files)
            # Находим текущий трек в новом порядке
            try:
                self.current_track_index = self.music_files.index(current_track)
            except ValueError:
                self.current_track_index = 0
    
    def update(self):
        """Обновляет состояние музыки (вызывать в главном цикле)"""
        if self.music_playing and not pygame.mixer.music.get_busy():
            # Текущий трек закончился, переключаемся на следующий
            self.next_track()
    
    def get_current_track_name(self):
        """Возвращает название текущего трека"""
        if self.music_files and self.current_track_index < len(self.music_files):
            return os.path.basename(self.music_files[self.current_track_index])
        return "No music"
    
    def load_sfx(self):
        """Загружает звуковые эффекты из папки data/sfx/"""
        sfx_dir = self.get_resource_path("data/sfx/")
        if not os.path.exists(sfx_dir):
            print("Папка звуковых эффектов не найдена")
            return
            
        # Поддерживаемые форматы для SFX
        supported_formats = ['.wav', '.ogg', '.mp3']
        
        # Загружаем все звуковые файлы
        for file in os.listdir(sfx_dir):
            if any(file.lower().endswith(fmt) for fmt in supported_formats):
                file_path = os.path.join(sfx_dir, file)
                try:
                    sound = pygame.mixer.Sound(file_path)
                    # Используем имя файла без расширения как ключ
                    sound_name = os.path.splitext(file)[0].lower()
                    self.sfx_sounds[sound_name] = sound
                    print(f"🔊 Загружен звук: {sound_name}")
                except pygame.error as e:
                    print(f"Ошибка загрузки звука {file}: {e}")
        
        if self.sfx_sounds:
            print(f"Загружено {len(self.sfx_sounds)} звуковых эффектов")
        else:
            print("Звуковые эффекты не найдены")

    def play_sfx(self, sound_name):
        """Воспроизводит звуковой эффект"""
        if sound_name.lower() in self.sfx_sounds:
            try:
                sound = self.sfx_sounds[sound_name.lower()]
                sound.set_volume(self.sfx_volume)
                sound.play()
            except pygame.error as e:
                print(f"Ошибка воспроизведения звука {sound_name}: {e}")
        else:
            print(f"Звук '{sound_name}' не найден")
