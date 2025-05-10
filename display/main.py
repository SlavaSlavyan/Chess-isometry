import pygame
import math

from display.Game import Game

class Display:

    def __init__(self,m):

        self.colors = m.JsonManager.load(f"data\\them\\{m.config['them']}")

        self.width,self.height = m.config['start-size']
        self.reload_screen_mode(m)

        self.Game = Game(m)

        self.clock = pygame.time.Clock()
        self.fps = self.clock.get_fps()

    def main(self,m):
        
        self.fps = self.clock.get_fps()
        self.width, self.height = self.screen.get_size()

        self.screen.fill((0,0,0))
        self.Game.main(m)

    def reload_screen_mode(self,m):

        if m.config['fullscreen']:
            self.screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode((m.config['start-size'][0],m.config['start-size'][1]),pygame.DOUBLEBUF | pygame.RESIZABLE)

        m.JsonManager.save("data\\config",m.config)