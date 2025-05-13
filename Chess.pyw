import turtle

turtle.Screen().setup(1200,800)
turtle.bgcolor((0,0,0))
turtle.pencolor((1,1,1))
turtle.hideturtle()
turtle.tracer(0)
turtle.write("Loading...",False,'center',("Courier",30,"normal"))
turtle.update()

from function.main import Main

Chess = Main()
turtle.bye()
Chess.start()