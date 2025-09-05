# Основной класс игры.

import pygame
import sys

from func.inp.Main import Main as inp_Main
from display._Main import Main as disp_Main
from func.manager.LogManager import Log
from func.manager.JsonManager import Json

class Main:
    
    # В аргументах указываются особые аргументы по типу версии игры
    def __init__(self, args=None):
        
        # Логирование
        self.Log = Log(self)
        self.Log.write(["=====[START]=====\n","Инициализация основного модуля..."],"DEBUG")
        
        # Конфигурация программы
        self.Json = Json(self)
        self.reload_config()
        
        self.Log.write("Инициализация PyGame.","DEBUG")
        pygame.init()
        
        self.Disp = disp_Main(self) # Display - отображение.
        self.PI = inp_Main(self) # Player input - ввод от пользователя.
        
        self.Log.write("Создание модуля контролирования потока кадров","DEBUG")
        self.Clock = pygame.time.Clock()
    
    # Основная функция для цикла
    def main(self):
        
        self.PI.main(self)
        
        self.Disp.main(self)
        
        pygame.display.flip()
        
        self.Clock.tick(self.config['max-fps'])
    
    # Перезагрузка конфигурации программы
    def reload_config(self):
        self.config = self.load(self,"data\\config",True)
        
    # Остановка программы
    def stop(self):
        
        self.Log.write("Запущена функция отключения программы...","WARNING")
        
        if self.config["save-logs"]:
            self.Log.save()
        
        pygame.quit()
        sys.exit()