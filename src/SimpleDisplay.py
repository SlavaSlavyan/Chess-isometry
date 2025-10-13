import turtle

class SimpleDisplay:

    def __init__(self):

        turtle.Screen().setup(1200,800)
        turtle.Screen().title("Starting")
        turtle.bgcolor((0,0,0))
        turtle.pencolor((1,1,1))
        turtle.hideturtle()
        turtle.tracer(0)
        turtle.up()

    def loading_screen(self):

        count = 0

        SimpleDisplay.start_settings()

        while True:

            turtle.clear()
            turtle.write(f"Loading... {count}",False,'center',("Courier",30,"normal"))
            turtle.update()

            count += 1