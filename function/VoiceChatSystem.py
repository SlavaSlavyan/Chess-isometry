"""
Система голосового чата для мультиплеера
Интегрируется с существующей сетевой инфраструктурой
"""

import pyaudio
import threading
import time
import pygame
import base64

# Настройки аудио
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


class VoiceChatSystem:
    """Система голосового чата"""
    
    def __init__(self):
        self.audio = None
        self.is_active = False
        self.is_recording = False
        self.network_manager = None
        
        # Потоки
        self.record_thread = None
        self.play_thread = None
        
        # Буфер для воспроизведения
        self.play_buffer = []
        self.buffer_lock = threading.Lock()
        
        # Потоки аудио
        self.input_stream = None
        self.output_stream = None
        
        # Статус
        self.status = "Отключен"
        self.error = None
        
        # Отслеживание говорящего
        self.speaking_player = None  # Никнейм говорящего игрока
        self.last_receive_time = 0   # Время последнего получения аудио
        self.speaking_timeout = 0.5   # Секунд без аудио = игрок перестал говорить
        
    def initialize(self):
        """Инициализация аудио системы"""
        try:
            self.audio = pyaudio.PyAudio()
            
            # Проверяем устройства
            input_count = 0
            output_count = 0
            for i in range(self.audio.get_device_count()):
                info = self.audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    input_count += 1
                if info['maxOutputChannels'] > 0:
                    output_count += 1
            
            if input_count == 0:
                self.error = "Микрофон не обнаружен"
                return False
            
            if output_count == 0:
                self.error = "Устройство вывода не обнаружено"
                return False
            
            self.status = "Инициализирован"
            return True
            
        except Exception as e:
            self.error = f"Ошибка инициализации: {str(e)}"
            return False
    
    def start(self, network_manager, player_name="Unknown"):
        """Запускает голосовой чат"""
        if not self.audio and not self.initialize():
            return False
        
        if self.is_active:
            return True
        
        self.network_manager = network_manager
        self.player_name = player_name
        self.is_active = True
        self.is_recording = True
        
        # Запускаем потоки
        self.record_thread = threading.Thread(target=self._record_audio, daemon=True)
        self.play_thread = threading.Thread(target=self._play_audio, daemon=True)
        
        self.record_thread.start()
        self.play_thread.start()
        
        self.status = "Активен"
        return True
    
    def stop(self):
        """Останавливает голосовой чат"""
        self.is_active = False
        self.is_recording = False
        self.status = "Остановлен"
        
        # Ждем завершения потоков
        time.sleep(0.3)
        
        # Закрываем потоки
        if self.input_stream:
            try:
                self.input_stream.stop_stream()
                self.input_stream.close()
            except:
                pass
            self.input_stream = None
        
        if self.output_stream:
            try:
                self.output_stream.stop_stream()
                self.output_stream.close()
            except:
                pass
            self.output_stream = None
        
        # Очищаем буфер
        with self.buffer_lock:
            self.play_buffer.clear()
    
    def cleanup(self):
        """Полная очистка ресурсов"""
        self.stop()
        
        if self.audio:
            try:
                self.audio.terminate()
            except:
                pass
            self.audio = None
    
    def _record_audio(self):
        """Поток записи аудио"""
        try:
            self.input_stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            while self.is_recording:
                try:
                    data = self.input_stream.read(CHUNK, exception_on_overflow=False)
                    
                    # Отправляем через сеть (кодируем в base64 для JSON)
                    if self.network_manager and self.network_manager.is_connected:
                        encoded_data = base64.b64encode(data).decode('utf-8')
                        self.network_manager.send_message('voice_data', {
                            'audio': encoded_data,
                            'speaker': getattr(self, 'player_name', 'Unknown')
                        })
                        
                except Exception as e:
                    if self.is_recording:
                        self.error = f"Ошибка записи: {str(e)}"
                    break
                    
        except Exception as e:
            self.error = f"Ошибка микрофона: {str(e)}"
        finally:
            if self.input_stream:
                try:
                    self.input_stream.stop_stream()
                    self.input_stream.close()
                except:
                    pass
    
    def _play_audio(self):
        """Поток воспроизведения аудио"""
        try:
            self.output_stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK
            )
            
            while self.is_active:
                try:
                    # Проверяем буфер
                    with self.buffer_lock:
                        if len(self.play_buffer) > 0:
                            data = self.play_buffer.pop(0)
                        else:
                            data = None
                    
                    if data:
                        self.output_stream.write(data)
                    else:
                        time.sleep(0.01)
                        
                except Exception as e:
                    if self.is_active:
                        self.error = f"Ошибка воспроизведения: {str(e)}"
                    break
                    
        except Exception as e:
            self.error = f"Ошибка динамиков: {str(e)}"
        finally:
            if self.output_stream:
                try:
                    self.output_stream.stop_stream()
                    self.output_stream.close()
                except:
                    pass
    
    def receive_audio(self, audio_data, speaker_name=None):
        """Получает аудио данные для воспроизведения"""
        if not self.is_active:
            return
        
        try:
            # Декодируем из base64
            if isinstance(audio_data, str):
                decoded_data = base64.b64decode(audio_data)
            else:
                decoded_data = audio_data
            
            with self.buffer_lock:
                self.play_buffer.append(decoded_data)
                
                # Ограничиваем размер буфера
                if len(self.play_buffer) > 10:
                    self.play_buffer.pop(0)
            
            # Обновляем информацию о говорящем
            if speaker_name:
                self.speaking_player = speaker_name
                self.last_receive_time = time.time()
                
        except Exception as e:
            self.error = f"Ошибка декодирования аудио: {str(e)}"
    
    def update_speaking_status(self):
        """Обновляет статус говорящего игрока"""
        if self.speaking_player and time.time() - self.last_receive_time > self.speaking_timeout:
            self.speaking_player = None
    
    def draw_speaking_indicator(self, screen, font=None):
        """Рисует индикатор говорящего игрока в правом верхнем углу"""
        # Обновляем статус перед отрисовкой
        self.update_speaking_status()
        
        # Показываем только если кто-то говорит
        if not self.speaking_player:
            return
        
        if not font:
            try:
                font = pygame.font.Font("data/font/text.ttf", 18)
            except:
                font = pygame.font.Font(None, 18)
        
        # Позиция в правом верхнем углу
        screen_width = screen.get_width()
        x = screen_width - 20  # 20px от правого края
        y = 20  # 20px от верха
        
        # Текст с иконкой микрофона
        text = f"🎤 {self.speaking_player}"
        text_surface = font.render(text, True, (255, 255, 255))
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        
        # Фон с небольшим паддингом
        padding = 10
        bg_width = text_width + padding * 2
        bg_height = text_height + padding * 2
        bg_x = x - bg_width
        bg_y = y
        
        bg_rect = pygame.Rect(bg_x, bg_y, bg_width, bg_height)
        
        # Полупрозрачный фон
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))
        screen.blit(bg_surface, (bg_x, bg_y))
        
        # Зеленая рамка (говорит)
        pygame.draw.rect(screen, (100, 255, 100), bg_rect, 2, border_radius=5)
        
        # Текст
        text_x = bg_x + padding
        text_y = bg_y + padding
        screen.blit(text_surface, (text_x, text_y))
    
    def draw_mute_indicator(self, screen):
        """Рисует маленький индикатор мута в левом нижнем углу"""
        if not self.is_active:
            return
        
        try:
            font = pygame.font.Font("data/font/text.ttf", 14)
        except:
            font = pygame.font.Font(None, 14)
        
        # Позиция в левом нижнем углу
        x = 10
        y = screen.get_height() - 30
        
        # Иконка и текст в зависимости от статуса микрофона
        if self.is_recording:
            icon = "🎤"
            text = "ON"
            color = (100, 255, 100)
        else:
            icon = "🔇"
            text = "MUTED"
            color = (255, 100, 100)
        
        display_text = f"{icon} {text}"
        text_surface = font.render(display_text, True, color)
        
        # Полупрозрачный фон
        padding = 5
        bg_width = text_surface.get_width() + padding * 2
        bg_height = text_surface.get_height() + padding * 2
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))
        
        screen.blit(bg_surface, (x, y))
        screen.blit(text_surface, (x + padding, y + padding))
    
    def toggle_mute(self):
        """Переключает запись (мут микрофона)"""
        self.is_recording = not self.is_recording
        
        if self.is_recording:
            self.status = "Активен"
        else:
            self.status = "Микрофон выключен"

