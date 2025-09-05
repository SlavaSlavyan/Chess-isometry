# Класс отображения

import pygame

class Main:
    
    def __init__(self,m):
        
        self.Screen = pygame.display.set_mode(m.config['start-screen-size'],pygame.RESIZABLE)
    
    def main(self,m):
        
        self.width, self.height = self.Screen.get_size()