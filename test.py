import pyglet

# Создаем окно
window = pyglet.window.Window(width=800, height=600, caption='Pyglet Example')

# Создаем текстовую метку
label = pyglet.text.Label('Hello, Pyglet World!',
                          font_name='Arial',
                          font_size=36,
                          x=window.width // 2,  # Центрируем по горизонтали
                          y=window.height // 2, # Центрируем по вертикали
                          anchor_x='center',
                          anchor_y='center')

# Определяем, что отрисовывать в окне
@window.event
def on_draw():
    window.clear()          # Очищаем окно (заливаем черным цветом)
    label.draw()           # Рисуем наш текст

# Запускаем приложение
pyglet.app.run()