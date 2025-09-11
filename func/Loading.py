import turtle
import math
from pathlib import Path

if not Path('data\\logs').exists():
    Path('data\\logs').mkdir(parents=True, exist_ok=True)
    
if Path('data\\logs\\_last.log').exists():
    Path('data\\logs\\_last.log').unlink()

turtle.Screen().setup(1200,800)
turtle.Screen().title("Loading")
turtle.bgcolor((0,0,0))
turtle.pencolor((1,1,1))
turtle.hideturtle()
turtle.tracer(0)
turtle.up()

timer = 0

while True:
    
    try:
        with open(f'data\\logs\\_last.log', 'r', encoding='utf-8') as file:
            data = file.read()
    except:
        data = "Waiting for info..."
    
    turtle.clear()
    
    if math.sin(timer) < -(1/3):
        title = "Loading..."
    elif math.sin(timer) > 1/3:
        title = "Loading.  "
    else:
        title = "Loading.. "
        
    turtle.teleport(0,0)
    
    turtle.write(title,False,'center',("Courier",30,"normal"))
    
    turtle.teleport(-turtle.Screen().window_width()//2+10,-turtle.Screen().window_height()//2)
    
    turtle.write(data,True,'left',("Courier",8,"normal"))
    
    turtle.update()
    
    timer += 0.03