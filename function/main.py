import pygame
import sys

from function.JsonManager import JsonManager
from display.main import Display
from function.PlayerInput import PlayerInput

class Main:

    def __init__(self):
        
        pygame.init()

        self.JsonManager = JsonManager(self)
        
        self.Disp = Display(self)
        self.PI = PlayerInput(self)

    def start(self):

        while True:

            self.PI.main(self)
            self.Disp.main(self)

            pygame.display.flip()
            self.Disp.clock.tick(60)
    
    def stop(self):

        pygame.quit()
        sys.exit()