import pygame
import math

class Game:

    def __init__(self,m):

        self.rotate = [0,90]

        self.test_img = pygame.image.load('data\\assets\\test-pawn.png')

    def main(self,m):

        self.center_test(m)

        pygame.draw.line(m.Disp.screen,(255,0,0),(m.Disp.width//2,0),(m.Disp.width//2,m.Disp.height))
    
    def center_test(self,m):
        
        for y in range(8):
            for x in range(8):

                offset_x = x * 50 - 175
                offset_y = y * 50 - 175

                rotated_x = offset_x * math.cos(math.pi*self.rotate[0]/180) - offset_y * math.sin(math.pi*self.rotate[0]/180)
                rotated_y = (offset_x * math.sin(math.pi*self.rotate[0]/180) + offset_y * math.cos(math.pi*self.rotate[0]/180))*math.sin(math.pi*self.rotate[1]/180)

                draw_x = int(m.Disp.width//2 + rotated_x)
                draw_y = int(m.Disp.height//2 + rotated_y)
                
                pygame.draw.circle(m.Disp.screen,(255,255,255),(draw_x, draw_y), 5, 1)

                self.test(m,(draw_x, draw_y))
    
    def test(self,m,center):

        points = []

        size = 50/(math.pi/2.2)

        for pos in range(4):
            points.append((center[0] + math.cos(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*size,center[1] + math.sin(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*math.sin(math.pi*self.rotate[1]/180)*size))

        pygame.draw.polygon(m.Disp.screen,(255,255,255),points,1)

        img = self.test_img.get_size()
        m.Disp.screen.blit(self.test_img, (center[0] - img[0]//2,center[1] - img[1]/1.25))