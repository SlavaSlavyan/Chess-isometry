import pygame

class MouseInput:

    def __init__(self,m):

        self.mouse_pos = pygame.mouse.get_pos()

        self.mouse = {'lt':False,'rt':False}
        self.mouse_click = {'lt':False,'rt':False}
        self.mouse_release = {'lt':False,'rt':False}

        self.last_mouse_pos = pygame.mouse.get_pos()

    def main(self,m,event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 1:

                self.mouse['lt'] = True
                self.mouse_click['lt'] = True
                self.last_mouse_pos = pygame.mouse.get_pos()
            
            if event.button == 3:

                self.mouse['rt'] = True
                self.mouse_click['rt'] = True
                self.last_mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                self.mouse['lt'] = False
                self.mouse_release['lt'] = True
            
            if event.button == 3:

                self.mouse['rt'] = False
                self.mouse_release['rt'] = True
        
        if event.type == pygame.MOUSEWHEEL:

            m.AssetManager.check_new_zoom(m)
            
            if event.y > 0:
                m.config['zoom'] = round(m.config['zoom'] + 0.1, 1)
            
            if event.y < 0:
                m.config['zoom'] = round(m.config['zoom'] - 0.1, 1)
    
    def update(self,m):

        self.mouse_click = {'lt':False,'rt':False}
        self.mouse_release = {'lt':False,'rt':False}