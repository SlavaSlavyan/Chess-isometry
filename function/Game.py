import pygame

class Game:

    def __init__(self,m):

        self.new_rotate = [0,0]

    def main(self,m):
        pass

    #def mouse_input(self,m):
    #    if m.PI.MI.mouse['rt']:
    #        self.new_rotate = [
    #            m.PI.MI.last_mouse_pos[0] - m.PI.MI.mouse_pos[0],
    #            m.PI.MI.last_mouse_pos[1] - m.PI.MI.mouse_pos[1]
    #        ]
    #    elif self.new_rotate != [0,0]:
    #       m.Disp.Game.rotate = [m.Disp.Game.rotate[0]-self.new_rotate[0],m.Disp.Game.rotate[1]-self.new_rotate[1]]
    #        self.new_rotate = [0,0]

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