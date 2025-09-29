import pygame

class Text:
    
    def __init__(self,m):
        
        m.Log.write("Инициализация класса отображения текста.","DEBUG")
        
        self.f3_font = pygame.font.Font("data\\font\\LanaPixel.ttf", 11)
        
    def F3(self,m):
        
        text = f'''F3 MODE CAN FREEZE THE PROGRAM. USE ONLY FOR DEBUGGING!

[CONFIG]
Max FPS: {m.config['max-fps']}
Start screen size: {m.config['start-screen-size']}
Log saving: {m.config['save-logs']}

[MAIN]:
FPS: {round(m.Disp.fps)}
Screen: {m.Disp.width}x{m.Disp.height}
'''
        
        line_num = 0
        
        for line in text.splitlines():

            m.Disp.Screen.blit(self.f3_font.render(line, False, (255,255,255)), (11,11+11*line_num))
            
            line_num += 1
                        
    def paragraf(self,m, text:str|list, pos:tuple, size:int, color:tuple, align:str="center"):

        font = pygame.font.Font("data\\font\\GNF.ttf", round(size*m.Disp.zoom))
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        pos = (m.Disp.width // 2 + pos[0]*m.Disp.zoom, m.Disp.height // 2 - pos[1]*m.Disp.zoom)
        
        if align == "left": text_rect.topleft = pos
        elif align == "center": text_rect.center = pos
        elif align == "right": text_rect.topright = pos
        
        m.Disp.screen.blit(text_surface, text_rect)
    
    def title(self,m, text:str, pos:tuple, size:int, color:tuple):

        font = pygame.font.Font("data\\font\\PIXY.ttf", round(size*m.Disp.zoom))
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        pos = (m.Disp.width // 2 + pos[0]*m.Disp.zoom, m.Disp.height // 2 - pos[1]*m.Disp.zoom)
        
        text_rect.center = pos
        
        m.Disp.screen.blit(text_surface, text_rect)