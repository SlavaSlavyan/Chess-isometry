import pygame
import math

from display.Game import Game
from display.Menu import Menu as MenuDisplay
from display.Settings import Settings as SettingsDisplay

class Display:

    def __init__(self,m):

        self.f3font = pygame.font.Font('data\\font\\text.ttf', 9)
        self.colors = m.JsonManager.load(f"data\\them\\{m.config['them']}")

        self.width,self.height = m.config['start-size']
        self.reload_screen_mode(m)

        self.Game = Game(m)

        self.clock = pygame.time.Clock()
        self.fps = self.clock.get_fps()
        self.last_scene = None
        self.scene_started_at = 0

    def main(self,m, scene='game'):
        
        self.fps = self.clock.get_fps()
        self.width, self.height = self.screen.get_size()
        # Детект смены сцены
        if self.last_scene != scene:
            self.last_scene = scene
            self.scene_started_at = pygame.time.get_ticks()
            # Подготовка меню для intro-анимации
            if scene == 'menu' and hasattr(self, 'Menu'):
                setattr(self.Menu, 'intro_t', 0)
                # Обновляем splash-текст при входе в меню
                m.SplashManager.refresh_splash()
            if scene == 'game':
                # Можно сбросить мелкие эффектные параметры игры, если нужны
                pass
        
        if scene == 'menu':
            # Отрисовка меню. Меню само рисует фон и элементы UI.
            if not hasattr(self, 'Menu'):
                self.Menu = MenuDisplay(m)
            # Передаем время с начала сцены в меню
            self.Menu.intro_t = (pygame.time.get_ticks() - self.scene_started_at) / 1000.0
            self.Menu.main(m)
        elif scene == 'settings':
            # Отрисовка настроек
            if not hasattr(self, 'Settings'):
                self.Settings = SettingsDisplay(m)
            self.Settings.intro_t = (pygame.time.get_ticks() - self.scene_started_at) / 1000.0
            self.Settings.main(m)
        else:
            self.Game.main(m)
        
        if m.config['f3']:
            self.f3(m)

    def reload_screen_mode(self,m):

        if m.config['fullscreen']:
            self.screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN | pygame.DOUBLEBUF)
            
        else:
            self.screen = pygame.display.set_mode((m.config['start-size'][0],m.config['start-size'][1]),pygame.DOUBLEBUF | pygame.RESIZABLE)

        m.JsonManager.save("data\\config",m.config)
    
    def fullscreen_press_check(self,m):
        
        if m.PI.KI.keys['f11']['press']:
            m.config['fullscreen'] = not m.config['fullscreen']
            self.reload_screen_mode(m)
    
    def f3(self,m):
        
        f3context = [
            "F3 mode can reduse much lags, please use this mode only in debug :)","",
            "[GLOBAL]",
            f" screen: {self.width}x{self.height}",
            f" fps: {round(self.fps)}",
            f" rotate: {m.Disp.Game.rotate}"
        ]
        
        config = ["","[CONFIG]"]
        for key,value in m.config.items():
            config.append(f" {key}: {value}")
        
        keys = ["","[KEYS]"]
        for key,value in m.PI.KI.keys.items():        
            keys.append(f" {key}: {value['value']}")
        
        mouse = ["","[MOUSE]",
                f"  pos: {m.PI.MI.mouse_pos}",
                f"  lastpos: {m.PI.MI.last_mouse_pos}",
                f"  status: {m.PI.MI.mouse}"]
            
        f3context.extend(config)
        f3context.extend(keys)
        f3context.extend(mouse)
        
        for line in range(len(f3context)):
            text = self.f3font.render(str(f3context[line]), False, m.Disp.colors['Global']['f3_text'])
            m.Disp.screen.blit(text, (9,9+9*line))
    
    def debug_mode_press_check(self,m):
        
        if m.PI.KI.keys['f3']['press']:
            m.config['f3'] = not m.config['f3']