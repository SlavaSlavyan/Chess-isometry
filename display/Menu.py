import pygame
import math
import sys
import os

class Menu:

	def __init__(self,m):

		self.title_font = pygame.font.Font(self.get_resource_path('data/font/title.ttf'), 72)
		self.text_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 22)
		self.small_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 14)
		self.pulse = 0
		self.intro_t = 0.0  # время с начала показа меню (сек)
		
		# Кеш для фоновой поверхности  
		self.background_surface = None
		self.background_cached = False
		
		# Кешированные шрифты
		self.splash_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 16)
		self.author_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 18)
		self.about_title_font = pygame.font.Font(self.get_resource_path('data/font/title.ttf'), 32)
		self.about_text_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 16)

	def get_resource_path(self, relative_path):
		"""Получить абсолютный путь к ресурсу, работает как в разработке, так и в PyInstaller"""
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, relative_path)
		else:
			return relative_path

	def main(self,m):

		self.draw_background(m)
		self.draw_title(m)
		self.draw_splash(m)
		self.draw_buttons(m)
		self.draw_author(m)
		if m.Menu.show_about:
			self.draw_about(m)
		self.pulse += 0.03

	def draw_background(self,m):

		screen = m.Disp.screen
		colors = m.Disp.colors['Game']
		screen.fill(colors['bg'])

		# Создаём фоновую поверхность с шахматной доской только один раз
		if not self.background_cached:
			self.background_surface = pygame.Surface((m.Disp.width, m.Disp.height), pygame.SRCALPHA)
			
			# Сохраняем оригинальные настройки поворота и зума
			original_rotate = m.Disp.Game.rotate[:]
			original_zoom = m.config['zoom']
			
			# Используем точно те же настройки что и в игре
			m.Disp.Game.rotate = [0, -90]  # Изометрический поворот как в игре
			m.config['zoom'] = original_zoom  # Тот же зум что и в игре
			
			# Создаем временные позиции клеток для фона
			temp_cells = []
			for y in range(8):
				row = []
				for x in range(8):
					offset_x = x * 50*m.config['zoom'] - 175*m.config['zoom']
					offset_y = y * 50*m.config['zoom'] - 175*m.config['zoom']

					rotated_x = offset_x * math.cos(math.pi*m.Disp.Game.rotate[0]/180) - offset_y * math.sin(math.pi*m.Disp.Game.rotate[0]/180)
					rotated_y = (offset_x * math.sin(math.pi*m.Disp.Game.rotate[0]/180) + offset_y * math.cos(math.pi*m.Disp.Game.rotate[0]/180))*math.sin(math.pi*m.Disp.Game.rotate[1]/180)

					draw_x = int(m.Disp.width//2 + rotated_x)
					draw_y = int(m.Disp.height//2 + rotated_y)
					
					points = m.Disp.Game.square(m, (draw_x, draw_y), 50/(math.pi/2.2))
					row.append(points)
				temp_cells.append(row)
			
			# Рисуем основу доски
			board = m.Disp.Game.square(m,(m.Disp.width//2,m.Disp.height//2),400)
			back = m.Disp.Game.square(m,(m.Disp.width//2,m.Disp.height//2),283)
			
			# Основной фон доски
			pygame.draw.polygon(self.background_surface, colors['bg'], board)
			pygame.draw.polygon(self.background_surface, colors['chessboard'], back)
			
			# Рисуем клетки шахматной доски напрямую на поверхность (оптимизированно)
			for y in range(8):
				for x in range(8):
					if (x+y)%2 == 1:  # Светлые клетки
						# Рисуем полупрозрачные светлые клетки
						light_color = (*colors['light_cell'], 120)
						pygame.draw.polygon(self.background_surface, light_color, temp_cells[y][x])
			
			# Восстанавливаем оригинальные настройки
			m.Disp.Game.rotate = original_rotate
			m.config['zoom'] = original_zoom
			
			self.background_cached = True

		# Рисуем кешированную поверхность с анимацией
		intro = min(1.0, self.intro_t)
		offset_y = int((1.0 - intro) * m.Disp.height * 0.10)
		
		screen.blit(self.background_surface, (0, offset_y))

	def draw_title(self,m):

		text = "CHESS ISOMETRY REWORK"
		intro = min(1.0, self.intro_t)
		slide = int((1.0 - intro) * 40)
		title = self.title_font.render(text, True, (255,255,255))
		rect = title.get_rect(center=(m.Disp.width//2, int(m.Disp.height*0.25) + slide))
		m.Disp.screen.blit(title, rect)

		sub = self.text_font.render("1.0", True, (200,200,200))
		srect = sub.get_rect(center=(m.Disp.width//2, rect.bottom + 24))
		m.Disp.screen.blit(sub, srect)
	
	def draw_splash(self, m):
		"""Рисует splash-текст в стиле Minecraft"""
		# Обновляем анимацию splash-менеджера
		m.SplashManager.update_animation(self.pulse)
		
		splash_text = m.SplashManager.get_current_splash()
		if not splash_text:
			return
		
		# Получаем параметры анимации
		anim = m.SplashManager.get_animation_params()
		
		# Анимация входа (как у всех элементов меню)
		intro = min(1.0, self.intro_t)
		slide_offset = int((1.0 - intro) * 60)  # Въезжает сверху
		intro_alpha = int(255 * intro)  # Плавное появление
		
		# Позиция splash-текста (слева от заголовка, под углом как в Minecraft)
		title_center_x = m.Disp.width//2
		title_y = int(m.Disp.height*0.25)
		
		# Смещение splash-текста относительно заголовка
		offset_x = -420  # Слева от заголовка
		offset_y = 40 + slide_offset  # С анимацией въезда
		
		base_x = title_center_x + offset_x
		base_y = title_y + offset_y
		
		# Создаём поверхность для поворота текста
		splash_render = self.splash_font.render(splash_text, True, (255, 255, 0))
		
		# Масштабируем
		scaled_width = int(splash_render.get_width() * anim['scale'])
		scaled_height = int(splash_render.get_height() * anim['scale'])
		if scaled_width > 0 and scaled_height > 0:
			scaled_surface = pygame.transform.scale(splash_render, (scaled_width, scaled_height))
			
			# Поворачиваем
			rotated_surface = pygame.transform.rotate(scaled_surface, anim['angle'])
			
			# Применяем комбинированную альфу (анимация входа + пульсация)
			combined_alpha = int((anim['alpha'] / 255.0) * intro_alpha)
			rotated_surface.set_alpha(combined_alpha)
			
			# Позиционируем по центру
			splash_rect = rotated_surface.get_rect()
			splash_rect.center = (base_x, base_y)
			
			# Отображаем splash-текст (БЕЗ рамки)
			m.Disp.screen.blit(rotated_surface, splash_rect)

	def draw_author(self, m):
		"""Рисует ник автора в нижнем правом углу"""
		from function.Menu import Menu as LogicMenu
		logic: LogicMenu = m.Menu
		
		if not logic.author_rect:
			return
		
		# Анимация входа
		intro = min(1.0, self.intro_t)
		slide_offset = int((1.0 - intro) * 30)
		intro_alpha = int(255 * intro)
		
		# Цвет зависит от наведения (серые тона)
		if logic.hover == "author":
			color = (180, 180, 180, intro_alpha)  # Светлее при наведении
		else:
			color = (140, 140, 140, intro_alpha)  # Серый цвет
		
		author_text = self.author_font.render("rework by Heck43 :3", True, color[:3])
		author_text.set_alpha(intro_alpha)
		
		# Позиция с анимацией въезда снизу
		rect = logic.author_rect.copy()
		rect.y += slide_offset
		
		m.Disp.screen.blit(author_text, rect)

	def draw_about(self, m):
		"""Рисует окно 'О проекте'"""
		from function.Menu import Menu as LogicMenu
		logic: LogicMenu = m.Menu
		
		screen = m.Disp.screen
		colors = m.Disp.colors['Game']
		
		# Размеры и позиция окна (увеличиваем для помещения всего текста)
		window_w, window_h = 500, 400
		window_x = (m.Disp.width - window_w) // 2
		window_y = (m.Disp.height - window_h) // 2
		
		# Полупрозрачный фон
		overlay = pygame.Surface((m.Disp.width, m.Disp.height), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 120))
		screen.blit(overlay, (0, 0))
		
		# Фон окна с изометрическим стилем
		window_rect = pygame.Rect(window_x, window_y, window_w, window_h)
		pygame.draw.rect(screen, colors['bg'], window_rect, border_radius=10)
		pygame.draw.rect(screen, colors['light_cell'], window_rect, 3, border_radius=10)
		
		# Заголовок
		title_text = self.about_title_font.render("О ПРОЕКТЕ", True, (255, 255, 255))
		title_rect = title_text.get_rect(centerx=window_x + window_w//2, y=window_y + 20)
		screen.blit(title_text, title_rect)
		
		# Информация о проекте
		info_lines = [
			"Chess Isometry rework 1.0",
			"",
			"Изометрическая шахматная игра",
			"с красивой анимацией и эффектами",
			"",
			"Создатель: SlavaSlavyan",
			"Продолжил: Heck43",
			"Движок: Python + Pygame",
			"",
			"Особенности:",
			"Изометрическая проекция",
			"Анимированные частицы",
			"Cистема мультиплейлиста",
			"Splash-тексты как в Minecraft",
			"Полная валидация шахматных правил"
		]
		
		y_offset = title_rect.bottom + 25
		
		for line in info_lines:
			if line.startswith("•"):
				color = (200, 255, 200)  # Зеленоватый для особенностей
			elif line == "Автор: Heck43":
				color = (255, 255, 100)  # Жёлтый для автора
			elif line == "Chess Isometry Alpha 0.2.7":
				color = (255, 200, 100)  # Оранжевый для названия
			else:
				color = (220, 220, 220)  # Обычный белый
			
			if line.strip():  # Не рисуем пустые строки
				line_text = self.about_text_font.render(line, True, color)
				line_rect = line_text.get_rect(centerx=window_x + window_w//2, y=y_offset)
				screen.blit(line_text, line_rect)
			
			y_offset += 18
		
		# Обновляем область для проверки клика
		logic.hover = "about_window" if window_rect.collidepoint(m.PI.MI.mouse_pos) else logic.hover

	def draw_buttons(self,m):

		from function.Menu import Menu as LogicMenu
		logic: LogicMenu = m.Menu
		intro = min(1.0, getattr(self, 'intro_t', 0.0))
		colors = m.Disp.colors['Game']

		for idx, (name, rect) in enumerate(logic.buttons.items()):
			is_hover = logic.hover == name
			base_color = colors['light_cell'] if is_hover else colors['dark_cell']
			# Кнопки плавно выезжают вверх с небольшим сдвигом по времени
			delay = min(0.15 * idx, 0.45)
			local = max(0.0, min(1.0, (self.intro_t - delay) / 0.35))
			y_slide = int((1.0 - local) * 60)
			alpha = int(255 * local)
			animated_rect = pygame.Rect(rect.x, rect.y + y_slide, rect.width, rect.height)
			surface = pygame.Surface((animated_rect.width, animated_rect.height), pygame.SRCALPHA)
			pygame.draw.rect(surface, (*base_color, alpha), surface.get_rect(), border_radius=8)
			pygame.draw.rect(surface, (*colors['chessboard'], alpha), surface.get_rect(), 2, border_radius=8)
			m.Disp.screen.blit(surface, animated_rect)

			label = name.upper()
			if name == 'continue': label = 'CONTINUE'
			elif name == 'play': label = 'NEW GAME'
			elif name == 'multiplayer': label = 'MULTIPLAYER'
			elif name == 'settings': label = 'SETTINGS'
			elif name == 'exit': label = 'EXIT'
			render = self.text_font.render(label, True, (255,255,255))
			lrect = render.get_rect(center=animated_rect.center)
			# Накладываем альфу через поверхность
			text_surface = pygame.Surface(render.get_size(), pygame.SRCALPHA)
			text_surface.blit(render, (0,0))
			text_surface.set_alpha(alpha)
			m.Disp.screen.blit(text_surface, lrect)


