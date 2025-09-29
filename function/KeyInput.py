import pygame

class KeyInput:

    def __init__(self,m):

        self.keys = {
            "up":{"id":pygame.K_UP,"value":False,"press":False,"release":False},
            "down":{"id":pygame.K_DOWN,"value":False,"press":False,"release":False},
            "left":{"id":pygame.K_LEFT,"value":False,"press":False,"release":False},
            "right":{"id":pygame.K_RIGHT,"value":False,"press":False,"release":False},
            "w":{"id":pygame.K_w,"value":False,"press":False,"release":False},
            "s":{"id":pygame.K_s,"value":False,"press":False,"release":False},
            "a":{"id":pygame.K_a,"value":False,"press":False,"release":False},
            "d":{"id":pygame.K_d,"value":False,"press":False,"release":False},
            "f3":{"id":pygame.K_F3,"value":False,"press":False,"release":False},
            "f11":{"id":pygame.K_F11,"value":False,"press":False,"release":False},
            "r":{"id":pygame.K_r,"value":False,"press":False,"release":False},
            "esc":{"id":pygame.K_ESCAPE,"value":False,"press":False,"release":False}
        }

    def main(self,m,event):

        for key in self.keys.values():

            if event.type == pygame.KEYDOWN:

                if event.key == key['id']:
                    key['value'] = True
                    key['press'] = True
            
            if event.type == pygame.KEYUP:

                if event.key == key['id']:
                    key['value'] = False
                    key['release'] = True
    
    def update(self,m):

        for key in self.keys.values():

            key['press'] = False
            key['release'] = False