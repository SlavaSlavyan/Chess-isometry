import pygame
import math

class Game:

    def __init__(self,m):

        self.cells = [
            [{"value":"white_rook" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_rook" }],
            [{"value":"white_knight" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_knight" }],
            [{"value":"white_bishop" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_bishop" }],
            [{"value":"white_queen" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_queen" }],
            [{"value":"white_king" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_king" }],
            [{"value":"white_bishop" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_bishop" }],
            [{"value":"white_knight" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_knight" }],
            [{"value":"white_rook" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_rook" }]
        ]
        
        for line in self.cells:
            for cell in line:
                
                cell['pos'] = []
                cell['offset'] = []
                cell['points'] = []
                cell['status'] = "none"
        
        self.selected_cell = None
        self.move = "white"
    
    def main(self,m):

        self.key_input(m)
        self.createpos(m)
        
        for x in range(8):
            for y in range(8):

                self.cells[x][y]['status'] = None
                
                if self.cells[x][y]['value'] != "empty" and self.cells[x][y]['value'][:5] == self.move:
                    
                    if m.PI.MI.mouse_click['lt']:
                        
                        if self.is_point_in_polygon(m.PI.MI.mouse_pos,self.cells[x][y]['points']):
                            
                            self.selected_cell = [x,y]
                            
        if self.selected_cell:
            
            cell = self.cells[self.selected_cell[0]][self.selected_cell[1]]
            x = self.selected_cell[0]
            y = self.selected_cell[1]
            
            cell['status'] = 'selected'
            
            if cell['value'][6:] == "pawn":
                self.cells[x][y+1] = 'move'

    def createpos(self,m):

        z = m.config['zoom']
        
        for y in range(8):
            for x in range(8):
                
                offset_x = x * 50*z - 175*z
                offset_y = y * 50*z - 175*z

                rotated_x = offset_x * math.cos(math.pi*m.Disp.Game.rotate[0]/180) - offset_y * math.sin(math.pi*m.Disp.Game.rotate[0]/180)
                rotated_y = (offset_x * math.sin(math.pi*m.Disp.Game.rotate[0]/180) + offset_y * math.cos(math.pi*m.Disp.Game.rotate[0]/180))*math.sin(math.pi*m.Disp.Game.rotate[1]/180)

                draw_x = int(m.Disp.width//2 + rotated_x)
                draw_y = int(m.Disp.height//2 + rotated_y)

                self.cells[x][y]['pos'] = [draw_x,draw_y]
                self.cells[x][y]['points'] = m.Disp.Game.square(m,self.cells[x][y]['pos'],50/(math.pi/2.2))

    def key_input(self,m):

        if m.PI.KI.keys['up']['value'] or m.PI.KI.keys['w']['value']:
            m.Disp.Game.rotate[1] += 1
        if m.PI.KI.keys['down']['value'] or m.PI.KI.keys['s']['value']:
            m.Disp.Game.rotate[1] -= 1
        if m.PI.KI.keys['left']['value'] or m.PI.KI.keys['a']['value']:
            m.Disp.Game.rotate[0] -= 1
        if m.PI.KI.keys['right']['value'] or m.PI.KI.keys['d']['value']:
            m.Disp.Game.rotate[0] += 1
        
        for i in range(2):
            
            if m.Disp.Game.rotate[i] > 180:
                m.Disp.Game.rotate[i] -= 360
            
            if m.Disp.Game.rotate[i] < -180:
                m.Disp.Game.rotate[i] += 360
    
    def is_point_in_polygon(self,point:tuple,polygon:list) -> bool:
        
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