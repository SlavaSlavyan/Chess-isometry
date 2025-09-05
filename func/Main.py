# Основной класс игры.

import pygame
import sys

from func.inp.Main import Main as inp_Main
from display.Main import Main as disp_Main

class Main:
    
    # В аргументах указываются особые аргументы по типу версии игры
    def __init__(self, args=None):
        
        # Конфигурация программы
        self.config = {
            "max-fps":60,
            "start-screen-size":[1200,800]
        }
        
        pygame.init()
        
        self.Disp = disp_Main(self) # Display - отображение.
        self.PI = inp_Main(self) # Player input - ввод от пользователя.
        
        self.Clock = pygame.time.Clock()
    
    # Основная функция для цикла
    def main(self):
        
        self.PI.main(self)
        
        self.Disp.main(self)
        
        pygame.display.flip()
        
        self.Clock.tick(self.config['max-fps'])
        
    # Остановка программы
    def stop(self):
        
        pygame.quit()
        sys.exit()