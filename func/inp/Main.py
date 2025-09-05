# Класс ввода

import pygame

class Main:
    
    def __init__(self,m):
        pass
    
    def main(self,m):
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                m.stop()