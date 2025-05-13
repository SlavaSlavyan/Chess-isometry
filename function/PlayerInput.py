import pygame

from function.MouseInput import MouseInput
from function.KeyInput import KeyInput
from function.Game import Game

class PlayerInput:

    def __init__(self,m):

        self.KI = KeyInput(m)
        self.MI = MouseInput(m)
        self.Game = Game(m)

    def main(self,m):

        self.MI.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                m.stop()
            
            self.KI.main(m,event)
            self.MI.main(m,event)

        self.logic(m) 
        
        self.update_input(m)
    
    def logic(self,m):
        
        m.Disp.debug_mode_press_check(m)
        m.Disp.fullscreen_press_check(m)
        self.Game.main(m)
    
    def update_input(self,m):
        
        self.KI.update(m)
        self.MI.update(m)