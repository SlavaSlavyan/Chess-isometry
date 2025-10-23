import sys
import turtle
import math

class SimpleDisplay:

    def __init__(self):
        
        self.screen = turtle.Screen()

        self.screen.setup(1200,800)
        self.screen.title("Simple display :)")
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

            turtle.begin_fill()
            for i in range(4):
                turtle.goto(math.cos(tick/100+math.pi/2*i)*100,math.sin(tick/100+math.pi/2*i)*100)
            turtle.end_fill()

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
    
    def text_up(self):
        self.text_scroll += 1
    
    def text_down(self):
        self.text_scroll -= 1
    
    def crash_log_screen(self):
        
        self.text_scroll = 0
        self.rotate = 0
        
        #turtle.up()
        
        original_crash_log = self.read_log('Crash report ALL.log')
        
        self.screen.listen()
        
        while True:
            
            self.screen.onkey(self.text_up,"Up")
            self.screen.onkey(self.text_down,"Down")
            
            crash_log = original_crash_log.split('\n')
            
            repeat = 1
            
            while repeat > 0:
                
                for i in range(len(crash_log)):
                    
                    if len(crash_log[i]) > turtle.window_width()//8:
                        
                        buffer = crash_log[i]
                        
                        crash_log[i] = buffer[:turtle.window_width()//8]
                        crash_log.insert(i+1,buffer[turtle.window_width()//8-len(buffer):])
                        
                        repeat += 1
                
                repeat -= 1
            
            crash_log = "\n".join(crash_log)
            
            turtle.clear()
        
            turtle.teleport(2-turtle.window_width()//2,8-turtle.window_height()//2+self.text_scroll*20)
            turtle.write(crash_log,False,'left',("Courier",9,"normal"))
            
            turtle.teleport(math.cos(self.rotate/100-math.pi/2)*100,math.sin(self.rotate/100-math.pi/2)*100)

            turtle.begin_fill()
            for i in range(4):
                turtle.goto(math.cos(self.rotate/100+math.pi/2*i)*100,math.sin(self.rotate/100+math.pi/2*i)*100)
            turtle.end_fill()
            
            turtle.teleport(-200,25)
            
            turtle.begin_fill()
            turtle.goto(200,25)
            turtle.goto(200,-25)
            turtle.goto(-200,-25)
            turtle.goto(-200,25)
            turtle.end_fill()
            
            turtle.teleport(0,-25)
            turtle.write(f"ERROR ＞︿＜",False,'center',("Courier",30,"normal"))
            
            if self.rotate < self.text_scroll*50:
                self.rotate += abs(self.text_scroll*50 - self.rotate)*0.1
            if self.rotate > self.text_scroll*50:
                self.rotate -= abs(self.text_scroll*50 - self.rotate)*0.1
            
            turtle.update()

Display = SimpleDisplay()
getattr(Display, sys.argv[1])()
#Display.crash_log_screen()