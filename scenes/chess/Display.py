import pygame
import math

class Display:

    def __init__(self,m):
        pass

    def main(self,m):

        m.Disp.Screen.fill((0,0,0))

        dots = []

        for i in range(4):
            dots.append((math.cos(math.pi/2*i)*50+m.Disp.width//2,math.sin(math.pi/2*i)*50+m.Disp.height//2))
            pygame.draw.circle(m.Disp.Screen,(255,255,255),dots[-1],5,1)