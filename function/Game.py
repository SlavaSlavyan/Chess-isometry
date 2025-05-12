import pygame

class Game:

    def __init__(self,m):

        self.cells = [
            ["white_rook","white_pawn",None,None,None,None,"black_pawn","black_rook"],
            ["white_knight","white_pawn",None,None,None,None,"black_pawn","black_knight"],
            ["white_bishop","white_pawn",None,None,None,None,"black_pawn","black_bishop"],
            ["white_queen","white_pawn",None,None,None,None,"black_pawn","black_queen"],
            ["white_king","white_pawn",None,None,None,None,"black_pawn","black_king"],
            ["white_bishop","white_pawn",None,None,None,None,"black_pawn","black_bishop"],
            ["white_knight","white_pawn",None,None,None,None,"black_pawn","black_knight"],
            ["white_rook","white_pawn",None,None,None,None,"black_pawn","black_rook"]
        ]

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