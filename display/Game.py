import pygame
import math

class Game:

    def __init__(self,m):

        self.rotate = [0,-90]

    def main(self,m):
        
        m.Disp.screen.fill(m.Disp.colors['Game']['bg'])
        
        self.chessboard(m)
        self.cells(m)

        pygame.draw.line(m.Disp.screen,(0,255,0),(m.Disp.width//2,0),(m.Disp.width//2,m.Disp.height))
        pygame.draw.line(m.Disp.screen,(0,0,255),(0,m.Disp.height//2),(m.Disp.width,m.Disp.height//2))
    
    def chessboard(self,m):
        
        z = m.config['zoom']
        
        points = []

        for pos in range(4):
            points.append((m.Disp.width//2 + math.cos(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*400*z,
                          m.Disp.height//2 + math.sin(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*math.sin(math.pi*self.rotate[1]/180)*400*z))

        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['chessboard'],points)
        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['light_cell'],points,1)
    
    def cells(self,m):
        
        z = m.config['zoom']
        
        for y in range(8):
            for x in range(8):
                

                offset_x = x * 50*z - 175*z
                offset_y = y * 50*z - 175*z

                rotated_x = offset_x * math.cos(math.pi*self.rotate[0]/180) - offset_y * math.sin(math.pi*self.rotate[0]/180)
                rotated_y = (offset_x * math.sin(math.pi*self.rotate[0]/180) + offset_y * math.cos(math.pi*self.rotate[0]/180))*math.sin(math.pi*self.rotate[1]/180)

                draw_x = int(m.Disp.width//2 + rotated_x)
                draw_y = int(m.Disp.height//2 + rotated_y)

                self.cell(m,(draw_x,draw_y),(x,y))
    
    def cell(self,m,position,selected_cell):
        
        z = m.config['zoom']
        
        points = []

        size = 50/(math.pi/2.2)*z

        for pos in range(4):
            points.append((position[0] + math.cos(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*size,position[1] + math.sin(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*math.sin(math.pi*self.rotate[1]/180)*size))

        if (selected_cell[0]+selected_cell[1])%2 == 0:
            color = m.Disp.colors['Game']['light_cell']
        else:
            color = m.Disp.colors['Game']['dark_cell']
        
        pygame.draw.polygon(m.Disp.screen,color,points)

        if m.PI.Game.cells[selected_cell[0]][selected_cell[1]] != None:
            m.AssetManager.img[m.PI.Game.cells[selected_cell[0]][selected_cell[1]]] = pygame.transform.scale(m.AssetManager.img[m.PI.Game.cells[selected_cell[0]][selected_cell[1]]], (64*z, 64*z))
            m.Disp.screen.blit(m.AssetManager.img[m.PI.Game.cells[selected_cell[0]][selected_cell[1]]],position)