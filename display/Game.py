import pygame
import math

class Game:

    def __init__(self,m):

        self.rotate = [0,-90]

    def main(self,m):
        
        m.Disp.screen.fill(m.Disp.colors['Game']['bg'])
        
        self.chessboard(m)
        self.cells(m)
        
        if m.config['f3']:
            pygame.draw.line(m.Disp.screen,(0,255,0),(m.Disp.width//2,0),(m.Disp.width//2,m.Disp.height))
            pygame.draw.line(m.Disp.screen,(0,0,255),(0,m.Disp.height//2),(m.Disp.width,m.Disp.height//2))
    
    def square(self,m,center:tuple,size:float) -> list:
        
        z = m.config['zoom']

        points = []

        for pos in range(4):
            points.append((center[0] + math.cos(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*size*z,
                          center[1] + math.sin(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*math.sin(math.pi*self.rotate[1]/180)*size*z))
        
        return points
    
    def chessboard(self,m):
        
        z = m.config['zoom']
        
        board = self.square(m,(m.Disp.width//2,m.Disp.height//2),400)
        white = self.square(m,(m.Disp.width//2,m.Disp.height//2),282)

        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['chessboard'],board)
        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['light_cell'],board,1)
        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['light_cell'],white)
        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['chessboard'],white,3)
    
    def cells(self,m):
        
        z = m.config['zoom']
        
        for y in range(8):
            for x in range(8):

                if (x+y)%2 == 1:
                
                    pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['dark_cell'],self.square(m,m.PI.Game.cells[x][y]['pos'],50/(math.pi/2.2)))

                    if m.PI.Game.cells[x][y]['value'] != "empty":
                        m.AssetManager.img[m.PI.Game.cells[x][y]['value']] = pygame.transform.scale(m.AssetManager.img[m.PI.Game.cells[x][y]['value']], (64*z, 64*z))
                        m.Disp.screen.blit(m.AssetManager.img[m.PI.Game.cells[x][y]['value']],m.PI.Game.cells[x][y]['pos'])