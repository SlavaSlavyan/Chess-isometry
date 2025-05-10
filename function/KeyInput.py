import pygame

class KeyInput:

    def __init__(self,m):

        self.keys = {
            "up":{"id":pygame.K_UP,"value":False},
            "down":{"id":pygame.K_DOWN,"value":False},
            "left":{"id":pygame.K_LEFT,"value":False},
            "right":{"id":pygame.K_RIGHT,"value":False}
        }

    def main(self,m,event):

        for key in self.keys.values():

            if event.type == pygame.KEYDOWN:

                if event.key == key['id']:
                    key['value'] = True
            
            if event.type == pygame.KEYUP:

                if event.key == key['id']:
                    key['value'] = False