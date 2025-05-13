import pygame
import math

from display.Game import Game

class Display:

    def __init__(self,m):

        self.f3font = pygame.font.Font('data\\font\\text.ttf', 9)
        self.colors = m.JsonManager.load(f"data\\them\\{m.config['them']}")

        self.width,self.height = m.config['start-size']
        self.reload_screen_mode(m)

        self.Game = Game(m)

        self.clock = pygame.time.Clock()
        self.fps = self.clock.get_fps()

    def main(self,m):
        
        self.fps = self.clock.get_fps()
        self.width, self.height = self.screen.get_size()
        
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
            
        f3context.extend(config)
        f3context.extend(keys)
        
        for line in range(len(f3context)):
            text = self.f3font.render(str(f3context[line]), False, m.Disp.colors['Global']['f3_text'])
            m.Disp.screen.blit(text, (9,9+9*line))
    
    def debug_mode_press_check(self,m):
        
        if m.PI.KI.keys['f3']['press']:
            m.config['f3'] = not m.config['f3']