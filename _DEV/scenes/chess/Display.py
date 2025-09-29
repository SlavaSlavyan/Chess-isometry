import pygame
import math

class Display:

    def __init__(self,m):
        
        m.Log.write("       |Инициализация отображения сцены Chess.")
        
        self.rotate = [0,0]

    def main(self, m):
        
        m.Disp.Screen.fill((0, 0, 0))
        
        poses = self.create_poses(m,self.rotate[0])
        
        for i in range(len(poses)):
            for j in range(len(poses[0])):
                
                pos = [m.Disp.width//2+poses[i][j][0]*50,m.Disp.height//2+poses[i][j][1]*50]
                
                pygame.draw.circle(m.Disp.Screen,(255,255,255),pos,5,1)

        self.rotate[0] += 1.33
        self.rotate[1] += 1
    
    def create_poses(self,m,degrees):
        
        width = 8
        height = 8
        
        poses = []
        
        cos_degrees = math.cos(math.radians(degrees))
        sin_degrees = math.sin(math.radians(degrees))
        
        for i in range(width):
            poses.append([])
            
            for j in range(height):
                poses[i].append([i,j])
                
                x_translated = poses[i][j][0] - (width-1)/2
                y_translated = poses[i][j][1] - (height-1)/2
                
                x_final = x_translated*cos_degrees - y_translated*sin_degrees
                y_final = x_translated*sin_degrees + y_translated*cos_degrees
                
                poses[i][j] = [x_final,y_final*math.sin(math.radians(self.rotate[1]))]
        
        return poses