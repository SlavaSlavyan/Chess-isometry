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
        self.MI.update(m)
    
    def logic(self,m):
        
        self.Game.key_input(m)