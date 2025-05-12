import pygame

class Game:

    def __init__(self,m):

        self.cells = {
            "a":[20,10,0,0,0,0,11,21],
            "b":[30,10,0,0,0,0,11,31],
            "c":[40,10,0,0,0,0,11,41],
            "d":[50,10,0,0,0,0,11,51],
            "e":[60,10,0,0,0,0,11,61],
            "f":[40,10,0,0,0,0,11,41],
            "g":[30,10,0,0,0,0,11,31],
            "h":[20,10,0,0,0,0,11,21]
        }

    def key_input(self,m):

        if m.PI.KI.keys['up']['value']:
            m.Disp.Game.rotate[1] += 1
        if m.PI.KI.keys['down']['value']:
            m.Disp.Game.rotate[1] -= 1
        if m.PI.KI.keys['left']['value']:
            m.Disp.Game.rotate[0] -= 1
        if m.PI.KI.keys['right']['value']:
            m.Disp.Game.rotate[0] += 1
        
        for i in range(2):
            
            if m.Disp.Game.rotate[i] > 180:
                m.Disp.Game.rotate[i] -= 360
            
            if m.Disp.Game.rotate[i] < -180:
                m.Disp.Game.rotate[i] += 360
        
        print(m.Disp.Game.rotate)
    
    def is_point_in_polygon(point, polygon):
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside