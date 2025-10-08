# Главный класс.

import src.GL as GL

class Main:
    
    def __init__(self, args=None):
        
        self.gl = GL
    
    def draw(self):
        # Очищаем экран
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)
        
        # Рисуем треугольник
        self.gl.glBegin(self.gl.GL_TRIANGLES)
        self.gl.glColor3f(1.0, 0.0, 0.0)  # Красный
        self.gl.glVertex2f(0.0, 0.5)
        self.gl.glColor3f(0.0, 1.0, 0.0)  # Зеленый
        self.gl.glVertex2f(-0.5, -0.5)
        self.gl.glColor3f(0.0, 0.0, 1.0)  # Синий
        self.gl.glVertex2f(0.5, -0.5)
        self.gl.glEnd()
        
        # Обновляем экран
        self.gl.glutSwapBuffers()

    def main(self):
        # Инициализация GLUT
        self.gl.glutInit()
        self.gl.glutInitDisplayMode(self.gl.GLUT_DOUBLE | self.gl.GLUT_RGB)
        self.gl.glutInitWindowSize(500, 500)
        self.gl.glutInitWindowPosition(100, 100)
        self.gl.glutCreateWindow(b"Simple OpenGL Program")
        
        # Устанавливаем функцию отрисовки
        self.gl.glutDisplayFunc(self.draw)
        
        # Задаем цвет очистки экрана
        self.gl.glClearColor(0.0, 0.0, 0.0, 1.0)  # Черный фон
        
        # Главный цикл GLUT
        self.gl.glutMainLoop()