import pygame
import math

class Game:

    def __init__(self,m):

        self.rotate = [0,-90]
        self.pulse = 0

    def main(self,m):
        
        m.Disp.screen.fill(m.Disp.colors['Game']['bg'])
        
        if self.rotate[1] < 0:
            self.chessboard(m)
            self.cells(m)
        else:
            self.cells(m)
            self.chessboard(m)
        
        if m.config['f3']:
            pygame.draw.line(m.Disp.screen,(0,255,0),(m.Disp.width//2,0),(m.Disp.width//2,m.Disp.height))
            pygame.draw.line(m.Disp.screen,(0,0,255),(0,m.Disp.height//2),(m.Disp.width,m.Disp.height//2))
        
        self.pulse += 0.05
    
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
        boardcolor = m.Disp.colors['Game']['bg']
        if self.rotate[1] < 0:
            back = self.square(m,(m.Disp.width//2,m.Disp.height//2),283)
            boardcolor = m.Disp.colors['Game']['chessboard']

        pygame.draw.polygon(m.Disp.screen,boardcolor,board)
        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['light_cell'],board,1)
        if self.rotate[1] < 0:
            pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['dark_cell'],back)

            for y in range(8):
                for x in range(8):

                    if (x+y)%2 == 1:
                    
                        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['light_cell'],m.PI.Game.cells[x][y]['points'])
                    
                    if m.PI.Game.selected_piece == [x,y]:
                        
                        polygon_surface = pygame.Surface((m.Disp.width, m.Disp.height), pygame.SRCALPHA)
                        polygon_surface.fill((0, 0, 0, 0))
                        
                        
                        color = m.Disp.colors['Game']['selected_cell']
                        color = (color[0],color[1],color[2],round(190+63*math.sin(self.pulse)))
                        
                        pygame.draw.polygon(polygon_surface,color,m.PI.Game.cells[x][y]['points'])
                        m.Disp.screen.blit(polygon_surface, (0, 0))
                        
            
            #pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['chessboard'],back,3)
        
    def cells(self,m):
        
        z = m.config['zoom']

        images = m.AssetManager.img
        cells = m.PI.Game.cells

        if self.rotate[0] > 90 or self.rotate[0] < -90:
            Y = range(8)
        else:
            Y = range(7,-1,-1)

        if self.rotate[0] > 0:
            X = range(7,-1,-1)
        else:
            X = range(8)

        for y in Y:
            for x in X:

                if cells[x][y]['value'] in images:

                    image = images[cells[x][y]['value']]
                    image = pygame.transform.scale(image, (50*z, 50*z))
                    if self.rotate[1] < -90 or self.rotate[1] > 90:
                        image = pygame.transform.flip(image, False, True)
                    image_size = image.get_size()
                    pos = [cells[x][y]['pos'][0]-image_size[0]/2,cells[x][y]['pos'][1]-image_size[1] + image_size[1]/2*(self.rotate[1]/-90)]
                    m.Disp.screen.blit(image,pos)
                
                if m.config['f3']:

                    pygame.draw.circle(m.Disp.screen,(255,255,0),cells[x][y]['pos'],5,1)
                    if cells[x][y]['value'] in images:pygame.draw.circle(m.Disp.screen,(255,0,255),(cells[x][y]['pos'][0],cells[x][y]['pos'][1] + image_size[1]/2*(self.rotate[1]/-90)),5,1)
                    pygame.draw.circle(m.Disp.screen,(0,255,255),pos,2,1)