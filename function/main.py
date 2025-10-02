import pygame
import sys

from function.JsonManager import JsonManager
from function.AssetManager import AssetManager
from function.AudioManager import AudioManager
from function.SplashManager import SplashManager
from display.main import Display
from function.PlayerInput import PlayerInput
from function.Menu import Menu
from function.Settings import Settings
from function.Multiplayer import Multiplayer
from function.PlayerProfile import PlayerProfile
from function.ErrorHandler import ErrorHandler
from display.ErrorDisplay import ErrorDisplay

class Main:

    def __init__(self):
        
        pygame.init()

        self.JsonManager = JsonManager(self)
        self.AssetManager = AssetManager(self)
        self.AudioManager = AudioManager(self)
        self.SplashManager = SplashManager(self)
        
        self.Disp = Display(self)
        self.PI = PlayerInput(self)
        self.Menu = Menu(self)
        self.Settings = Settings(self)
        self.Multiplayer = Multiplayer(self)
        self.PlayerProfile = PlayerProfile()
        self.ErrorHandler = ErrorHandler()
        self.ErrorDisplay = ErrorDisplay()

        self.scene = 'menu'
        self.prev_scene = None
        
        # Ограничение FPS
        self.clock = pygame.time.Clock()
        self.target_fps = 60

    def start(self):

        while True:
            try:
                # Если есть активное окно ошибки, показываем его
                if self.ErrorHandler.is_error_visible():
                    self._handle_error_display()
                    continue

                if self.scene == 'menu':
                    # В меню тоже нужно обрабатывать события
                    self.PI.MI.mouse_pos = pygame.mouse.get_pos()
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.stop()
                        self.PI.MI.main(self, event)
                        self.PI.KI.main(self, event)
                    
                    # Обработка клавиш F11 и F3 в меню
                    self.Disp.fullscreen_press_check(self)
                    self.Disp.debug_mode_press_check(self)
                    
                    self.Menu.main(self)
                    self.Disp.main(self, scene='menu')
                    
                    # Обновляем состояние ввода
                    self.PI.MI.update(self)
                    self.PI.KI.update(self)
                elif self.scene == 'settings':
                    # Обработка событий в настройках
                    self.PI.MI.mouse_pos = pygame.mouse.get_pos()
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.stop()
                        self.PI.MI.main(self, event)
                        self.PI.KI.main(self, event)
                    
                    self.Disp.fullscreen_press_check(self)
                    self.Disp.debug_mode_press_check(self)
                    
                    self.Settings.main(self)
                    self.Disp.main(self, scene='settings')
                    
                    self.PI.MI.update(self)
                    self.PI.KI.update(self)
                elif self.scene == 'multiplayer':
                    # Обработка событий в мультиплеере
                    self.PI.MI.mouse_pos = pygame.mouse.get_pos()
                    
                    events = []
                    for event in pygame.event.get():
                        events.append(event)
                        if event.type == pygame.QUIT:
                            self.stop()
                        self.PI.MI.main(self, event)
                        self.PI.KI.main(self, event)
                    
                    self.Disp.fullscreen_press_check(self)
                    self.Disp.debug_mode_press_check(self)
                    
                    self.Multiplayer.main(self)
                    # Передаем события в мультиплеер для обработки текстового ввода
                    self.Multiplayer.handle_text_input(self, events)
                    # Обрабатываем редактор аватаров
                    self.Multiplayer.handle_avatar_editor(self, events, self.PI.MI.mouse_pos)
                    self.Disp.main(self, scene='multiplayer')
                    
                    self.PI.MI.update(self)
                    self.PI.KI.update(self)
                else:
                    self.PI.main(self)
                    self.Disp.main(self, scene='game')
                
                # Обновляем музыку (проверяем окончание треков)
                self.AudioManager.update()
                
                pygame.display.flip()
                
                # Ограничиваем FPS
                self.clock.tick(self.target_fps)
                
            except Exception as e:
                # Перехватываем все ошибки и показываем окно
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.ErrorHandler.handle_error(exc_type, exc_value, exc_traceback)
    
    def _handle_error_display(self):
        """Обрабатывает отображение окна ошибки"""
        try:
            # Получаем информацию об ошибке
            error_info = self.ErrorHandler.get_error_info()
            if not error_info:
                return
            
            # Рисуем окно и получаем прямоугольники кнопок
            close_rect, log_rect = self.ErrorDisplay.draw_error_window(self, error_info)
            
            # Обрабатываем события (чтобы окно не зависло)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Обрабатываем клики
                    self.ErrorDisplay.handle_error_input(self, pygame.mouse.get_pos(), close_rect, log_rect)
            
            pygame.display.flip()
            self.clock.tick(self.target_fps)
            
        except Exception as e:
            # Если не можем отобразить окно ошибки, выводим в консоль и закрываем
            print(f"❌ Критическая ошибка при отображении окна ошибки: {e}")
            print(f"Исходная ошибка: {error_info}")
            self.ErrorHandler.clear_error()
    
    def stop(self):
        
        # Останавливаем голосовой чат если активен
        if hasattr(self, 'VoiceChat'):
            self.VoiceChat.cleanup()
        
        # Сохраняем настройки звука
        self.config['music_volume'] = self.AudioManager.music_volume
        self.config['sfx_volume'] = self.AudioManager.sfx_volume
        
        self.JsonManager.save("data/config",self.config)
        pygame.quit()
        sys.exit()

    # Смена сцены с триггером анимации входа (без затемнения)
    def set_scene(self, scene: str):
        if scene == self.scene:
            return
        self.prev_scene = self.scene
        self.scene = scene
        # Сообщаем дисплею о смене сцены — он сам запустит intro-анимацию
        if hasattr(self, 'Disp'):
            setattr(self.Disp, 'last_scene', None)  # заставим Display определить смену