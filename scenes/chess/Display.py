import pygame
import math

class Display:

    def __init__(self,m):
        self.rotate = [0,0]

    def main(self, m):
        
        m.Disp.Screen.fill((0, 0, 0))
        
        poses = self.create_poses(m,self.rotate[0])
        
        for i in range(len(poses)):
            for j in range(len(poses[0])):
                
                pos = [m.Disp.width//2+poses[i][j][0]*50,m.Disp.height//2+poses[i][j][1]*50]
                
                pygame.draw.circle(m.Disp.Screen,(255,255,255),pos,5,1)

        self.rotate[0] += 1.5
        self.rotate[1] += 1
    
    def create_poses(self,m,degrees):
        
        width = 9
        height = 9
        
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
    
    def rotate_points(m,self,dots, center_point, angle_degrees):
        """
        Вращает точки вокруг заданной центральной точки
        
        Args:
            dots: список точек [[x1,y1], [x2,y2], ...]
            center_point: центральная точка [cx, cy]
            angle_degrees: угол вращения в градусах
        
        Returns:
            Список повернутых точек
        """
        # Преобразуем угол из градусов в радианы
        angle_rad = math.radians(angle_degrees)
        
        # Синус и косинус угла
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        # Центральная точка
        cx, cy = center_point
        
        rotated_dots = []
        
        for dot in dots:
            x, y = dot
            
            # Переносим точку в систему координат с центром в center_point
            x_translated = x - cx
            y_translated = y - cy
            
            # Применяем вращение
            x_rotated = x_translated * cos_angle - y_translated * sin_angle
            y_rotated = x_translated * sin_angle + y_translated * cos_angle
            
            # Возвращаем точку в исходную систему координат
            x_final = x_rotated + cx
            y_final = y_rotated + cy
            
            rotated_dots.append([x_final, y_final])
        
        return rotated_dots