from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import OpenGL

def draw():
    # Очищаем экран
    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT)
    
    # Рисуем треугольник
    OpenGL.GL.glBegin(GL_TRIANGLES)
    OpenGL.GL.glColor3f(1.0, 0.0, 0.0)  # Красный
    OpenGL.GL.glVertex2f(0.0, 0.5)
    OpenGL.GL.glColor3f(0.0, 1.0, 0.0)  # Зеленый
    OpenGL.GL.glVertex2f(-0.5, -0.5)
    OpenGL.GL.glColor3f(0.0, 0.0, 1.0)  # Синий
    OpenGL.GL.glVertex2f(0.5, -0.5)
    OpenGL.GL.glEnd()
    
    # Обновляем экран
    OpenGL.GLUT.glutSwapBuffers()

def main():
    # Инициализация GLUT
    OpenGL.GLUT.glutInit()
    OpenGL.GLUT.glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    OpenGL.GLUT.glutInitWindowSize(500, 500)
    OpenGL.GLUT.glutInitWindowPosition(100, 100)
    OpenGL.GLUT.glutCreateWindow(b"Simple OpenGL Program")
    
    # Устанавливаем функцию отрисовки
    OpenGL.GLUT.glutDisplayFunc(draw)
    
    # Задаем цвет очистки экрана
    OpenGL.GL.glClearColor(0.0, 0.0, 0.0, 1.0)  # Черный фон
    
    # Главный цикл GLUT
    OpenGL.GLUT.glutMainLoop()

if __name__ == "__main__":
    main()