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
            
            # Обрабатываем чат в мультиплеере
            if (hasattr(self.Game, 'multiplayer_mode') and self.Game.multiplayer_mode and 
                hasattr(m, 'ChatSystem')):
                # Если чат обработал событие, не передаем его дальше
                if m.ChatSystem.handle_key_input(event):
                    continue
                # Обрабатываем открытие чата по T
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t and not m.ChatSystem.input_active:
                    m.ChatSystem.start_input()
                    continue  # Не обрабатываем T дальше
            
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