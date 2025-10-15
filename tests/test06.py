import sys
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import time

class Clock:
    """Класс для контроля FPS"""
    def __init__(self, target_fps=60):
        self.target_fps = target_fps
        self.frame_time = 1.0 / target_fps
        self.last_time = time.time()
        self.delta_time = 0
        self.current_time = 0
        
    def tick(self):
        """Обновляет время и возвращает delta_time"""
        self.current_time = time.time()
        self.delta_time = self.current_time - self.last_time
        self.last_time = self.current_time
        return self.delta_time
        
    def limit_fps(self):
        """Ограничивает FPS если нужно"""
        elapsed = time.time() - self.last_time
        if elapsed < self.frame_time:
            time.sleep(self.frame_time - elapsed)

class MouseInput:
    """Класс для обработки ввода с мыши"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.clicked = False
        
    def mouse_move(self, x, y):
        """Обработка движения мыши"""
        self.x = x
        self.y = y
        
    def mouse_click(self, button, state, x, y):
        """Обработка кликов мыши"""
        if button == glut.GLUT_LEFT_BUTTON:
            self.clicked = (state == glut.GLUT_DOWN)
            self.x = x
            self.y = y

class KeyInput:
    """Класс для обработки ввода с клавиатуры"""
    def __init__(self):
        self.keys = {}
        
    def key_press(self, key, x, y):
        """Обработка нажатия клавиш"""
        self.keys[key] = True
        
    def key_release(self, key, x, y):
        """Обработка отпускания клавиш"""
        self.keys[key] = False
        
    def is_key_pressed(self, key):
        """Проверка нажата ли клавиша"""
        return self.keys.get(key, False)

class PlayerInput:
    """Главный класс для обработки ввода пользователя"""
    def __init__(self):
        self.mouse = MouseInput()
        self.keyboard = KeyInput()
        self.custom_events = {}
        
    def bind_custom_event(self, event_name, callback):
        """Привязка кастомных событий"""
        self.custom_events[event_name] = callback

class Display:
    """Класс для отображения"""
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.clock = Clock()
        self.rotation_angle = 0
        self.aspect_ratio = width / height
        
    def init_gl(self):
        """Инициализация OpenGL"""
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)  # Черный фон
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.update_projection()
        
    def update_projection(self):
        """Обновление проекционной матрицы при изменении размера окна"""
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        
        # Устанавливаем фиксированную систему координат
        # Координаты от -10 до 10 по обеим осям
        if self.width <= self.height:
            # Окно вертикальное или квадратное
            aspect = self.height / self.width
            gl.glOrtho(-10.0, 10.0, -10.0 * aspect, 10.0 * aspect, -1.0, 1.0)
        else:
            # Окно горизонтальное
            aspect = self.width / self.height
            gl.glOrtho(-10.0 * aspect, 10.0 * aspect, -10.0, 10.0, -1.0, 1.0)
            
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
    def handle_resize(self, width, height):
        """Обработка изменения размера окна"""
        self.width = width
        self.height = height
        self.aspect_ratio = width / height
        
        gl.glViewport(0, 0, width, height)
        self.update_projection()
        
    def draw_square(self):
        """Рисование квадрата с фиксированным размером"""
        size = 3.0  # Фиксированный размер квадрата в координатах мира
        
        gl.glBegin(gl.GL_QUADS)
        gl.glColor3f(1.0, 0.0, 0.0)  # Красный цвет
        gl.glVertex2f(-size/2, -size/2)
        gl.glVertex2f(size/2, -size/2)
        gl.glVertex2f(size/2, size/2)
        gl.glVertex2f(-size/2, size/2)
        gl.glEnd()
        
    def render(self):
        """Основная функция отрисовки"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        
        # Вращение квадрата
        self.rotation_angle += 1.0
        if self.rotation_angle > 360:
            self.rotation_angle = 0
            
        gl.glRotatef(self.rotation_angle, 0, 0, 1)
        self.draw_square()
        
        glut.glutSwapBuffers()

class Main:
    """Главный класс приложения"""
    def __init__(self):
        self.running = False
        self.display = Display()
        self.player_input = PlayerInput()
        
    def initialize(self):
        """Инициализация GLUT и OpenGL"""
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
        glut.glutInitWindowSize(self.display.width, self.display.height)
        glut.glutCreateWindow(b"Rotating Square")
        
        # Настройка callback функций
        glut.glutDisplayFunc(self.display.render)
        glut.glutIdleFunc(self.idle)
        glut.glutReshapeFunc(self.display.handle_resize)  # Добавляем обработчик изменения размера
        
        # Настройка обработчиков ввода
        glut.glutKeyboardFunc(self.player_input.keyboard.key_press)
        glut.glutKeyboardUpFunc(self.player_input.keyboard.key_release)
        glut.glutMouseFunc(self.player_input.mouse.mouse_click)
        glut.glutMotionFunc(self.player_input.mouse.mouse_move)
        glut.glutPassiveMotionFunc(self.player_input.mouse.mouse_move)
        
        # Привязка кастомного события выхода
        self.player_input.bind_custom_event('exit', self.stop)
        
        self.display.init_gl()
        
    def idle(self):
        """Функция вызываемая когда приложение простаивает"""
        self.display.clock.tick()
        self.handle_input()
        glut.glutPostRedisplay()
        self.display.clock.limit_fps()
        
    def handle_input(self):
        """Обработка ввода пользователя"""
        # Выход по ESC
        if self.player_input.keyboard.is_key_pressed(b'\x1b'):  # ESC
            self.stop()
            
    def start(self):
        """Запуск основного цикла"""
        if not self.running:
            self.running = True
            print("Starting application...")
            glut.glutMainLoop()
            
    def stop(self):
        """Остановка приложения с возможностью сохранения данных"""
        if self.running:
            self.running = False
            print("Stopping application...")
            # Здесь можно добавить сохранение данных перед выходом
            self.save_data()
            sys.exit(0)
            
    def save_data(self):
        """Функция для сохранения данных перед выходом"""
        print("Saving data before exit...")
        # Здесь можно реализовать логику сохранения

if __name__ == "__main__":
    app = Main()
    app.initialize()
    app.start()