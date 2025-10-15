import sys
import turtle

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
        with open(path,"r",encoding='utf-8') as file:
            return file.read()

    def loading_screen(self):

        tick = 0

        while True:
            
            log = self.read_log('data\\logs\\_last.log')

            turtle.clear()
            
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