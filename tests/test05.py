from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

# Переменные для вращения
rotation_x = 0.0
rotation_y = 0.0

def init():
    """Инициализация OpenGL"""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Черный фон
    glEnable(GL_DEPTH_TEST)  # Включение теста глубины
    
    # Настройка освещения
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Параметры света
    light_position = [2.0, 2.0, 2.0, 1.0]
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    
    # Материал куба
    material_ambient = [0.1, 0.2, 0.5, 1.0]
    material_diffuse = [0.3, 0.5, 0.9, 1.0]
    material_specular = [1.0, 1.0, 1.0, 1.0]
    material_shininess = [100.0]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

def draw_cube():
    """Рисование куба"""
    vertices = [
        # Передняя грань
        [-0.5, -0.5,  0.5], [0.5, -0.5,  0.5], [0.5,  0.5,  0.5], [-0.5,  0.5,  0.5],
        # Задняя грань
        [-0.5, -0.5, -0.5], [-0.5,  0.5, -0.5], [0.5,  0.5, -0.5], [0.5, -0.5, -0.5],
        # Верхняя грань
        [-0.5,  0.5, -0.5], [-0.5,  0.5,  0.5], [0.5,  0.5,  0.5], [0.5,  0.5, -0.5],
        # Нижняя грань
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, -0.5,  0.5], [-0.5, -0.5,  0.5],
        # Правая грань
        [0.5, -0.5, -0.5], [0.5,  0.5, -0.5], [0.5,  0.5,  0.5], [0.5, -0.5,  0.5],
        # Левая грань
        [-0.5, -0.5, -0.5], [-0.5, -0.5,  0.5], [-0.5,  0.5,  0.5], [-0.5,  0.5, -0.5]
    ]
    
    normals = [
        [0, 0, 1],   # Передняя
        [0, 0, -1],  # Задняя
        [0, 1, 0],   # Верхняя
        [0, -1, 0],  # Нижняя
        [1, 0, 0],   # Правая
        [-1, 0, 0]   # Левая
    ]
    
    indices = [
        [0, 1, 2, 3],    # Передняя
        [4, 5, 6, 7],    # Задняя
        [8, 9, 10, 11],  # Верхняя
        [12, 13, 14, 15],# Нижняя
        [16, 17, 18, 19],# Правая
        [20, 21, 22, 23] # Левая
    ]
    
    glBegin(GL_QUADS)
    for i, face in enumerate(indices):
        glNormal3fv(normals[i])
        for vertex_index in face:
            glVertex3fv(vertices[vertex_index])
    glEnd()

def display():
    """Функция отрисовки"""
    global rotation_x, rotation_y
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(3, 3, 3,  # Позиция камеры
              0, 0, 0,  # Точка, на которую смотрим
              0, 1, 0)  # Вектор "вверх"
    
    # Вращение куба
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)
    
    draw_cube()
    
    glutSwapBuffers()

def reshape(width, height):
    """Функция изменения размера окна"""
    if height == 0:
        height = 1
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def idle():
    """Функция для анимации"""
    global rotation_x, rotation_y
    rotation_x += 0.5
    rotation_y += 0.3
    glutPostRedisplay()

def keyboard(key, x, y):
    """Обработка клавиатуры"""
    if key == b'\x1b':  # ESC
        sys.exit()

def main():
    """Основная функция"""
    # Инициализация GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"PyOpenGL Cube with GLUT")
    
    # Инициализация OpenGL
    init()
    
    # Регистрация callback-функций
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)  # Для анимации
    
    # Главный цикл GLUT
    glutMainLoop()

if __name__ == "__main__":
    main()