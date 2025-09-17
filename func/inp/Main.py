# Класс ввода

import pygame

from func.inp.KeyInput import KeyInput

class Main:
    
    def __init__(self,m):
        m.Log.write("Инициализация класса эвентов.","DEBUG")

        self.KI = KeyInput(m)
    
    def main(self,m):
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                m.stop()
            
            self.KI.main(m,event)