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

        self.scene = 'menu'
        self.prev_scene = None
        
        # Ограничение FPS
        self.clock = pygame.time.Clock()
        self.target_fps = 60

    def start(self):

        while True:

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
            else:
                self.PI.main(self)
                self.Disp.main(self, scene='game')
            
            # Обновляем музыку (проверяем окончание треков)
            self.AudioManager.update()
            
            pygame.display.flip()
            
            # Ограничиваем FPS
            self.clock.tick(self.target_fps)
    
    def stop(self):
        
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