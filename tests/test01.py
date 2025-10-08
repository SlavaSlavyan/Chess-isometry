from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

def draw():
    # Очищаем экран
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Рисуем треугольник
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Красный
    glVertex2f(0.0, 0.5)
    glColor3f(0.0, 1.0, 0.0)  # Зеленый
    glVertex2f(-0.5, -0.5)
    glColor3f(0.0, 0.0, 1.0)  # Синий
    glVertex2f(0.5, -0.5)
    glEnd()
    
    # Обновляем экран
    glutSwapBuffers()

def handle_events():
    # Обработка событий GLUT
    # Эта функция обрабатывает события окна (клавиатура, мышь, перерисовка)
    glutMainLoopEvent()

def main():
    # Инициализация GLUT
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Custom OpenGL Main Loop")
    
    # Устанавливаем функцию отрисовки
    glutDisplayFunc(draw)
    
    # Задаем цвет очистки экрана
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Черный фон
    
    # Переменные для контроля FPS
    FPS = 60
    frame_duration = 1.0 / FPS
    running = True
    
    # Пользовательский главный цикл
    while running:
        frame_start = time.time()
        
        # Обработка событий
        handle_events()
        
        # Запрос на перерисовку
        glutPostRedisplay()
        
        # Вызов функции отрисовки
        draw()
        
        # Контроль FPS
        frame_time = time.time() - frame_start
        sleep_time = frame_duration - frame_time
        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == "__main__":
    main()