import sys
import turtle
import math

class SimpleDisplay:

    def __init__(self):

        turtle.Screen().setup(1200,800)
        turtle.Screen().title("Simple display")
        turtle.bgcolor((0,0,0))
        turtle.fillcolor((0,0,0))
        turtle.pencolor((1,1,1))
        turtle.hideturtle()
        turtle.tracer(0)
    
    def read_log(self, path: str) -> str:

        try:
            with open(path,"r",encoding='utf-8') as file:
                return file.read()
            
        except:
            return r"No data found ¯\_(ツ)_/¯"

    def loading_screen(self):

        tick = 0

        while True:
            
            log = self.read_log('data\\logs\\_last.log')

            turtle.clear()

            turtle.teleport(2-turtle.window_width()//2,8-turtle.window_height()//2)
            turtle.write(log,False,'left',("Courier",9,"normal"))
            
            turtle.teleport(turtle.window_width()//2-9,turtle.window_height()//2-14)
            turtle.write(tick,False,'right',("Courier",9,"normal"))
            
            turtle.teleport(math.cos(tick/100-math.pi/2)*100,math.sin(tick/100-math.pi/2)*100)

            for i in range(4):
                turtle.goto(math.cos(tick/100+math.pi/2*i)*100,math.sin(tick/100+math.pi/2*i)*100)

            turtle.teleport(-200,25)
            
            turtle.begin_fill()
            turtle.goto(200,25)
            turtle.goto(200,-25)
            turtle.goto(-200,-25)
            turtle.goto(-200,25)
            turtle.end_fill()
            
            turtle.teleport(0,-25)
            turtle.write(f"LOADING",False,'center',("Courier",30,"normal"))
            
            turtle.update()

            tick += 1

Display = SimpleDisplay()
getattr(Display, sys.argv[1])()