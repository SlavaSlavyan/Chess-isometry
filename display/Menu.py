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
		
		# Кешированные шрифты
		self.splash_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 16)
		self.author_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 18)
		self.about_title_font = pygame.font.Font(self.get_resource_path('data/font/title.ttf'), 32)
		self.about_text_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 16)
		
		# Атмосферные частицы
		import random
		self.particles = []
		for _ in range(40):
			self.particles.append({
				'x': random.uniform(0, 1280),
				'y': random.uniform(0, 720),
				'vx': random.uniform(-15, 15),
				'vy': random.uniform(-30, -10),
				'size': random.randint(1, 3),
				'alpha': random.randint(50, 150),
				'life': random.uniform(0.3, 1.0)
			})

	def get_resource_path(self, relative_path):
		"""Получить абсолютный путь к ресурсу, работает как в разработке, так и в PyInstaller"""
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, relative_path)
		else:
			return relative_path

	def main(self,m):

		self.draw_background(m)
		self.update_and_draw_particles(m)
		self.draw_title(m)
		self.draw_splash(m)
		self.draw_buttons(m)
		self.draw_author(m)
		if m.Menu.show_about:
			self.draw_about(m)
		self.pulse += 0.03

	def draw_background(self,m):
		"""Рисует фон с медленно вращающейся изометрической доской"""
		screen = m.Disp.screen
		colors = m.Disp.colors['Game']
		
		# Градиентный фон
		bg_base = colors['bg']
		for i in range(m.Disp.height):
			progress = i / m.Disp.height
			r = int(bg_base[0] * (1.0 + progress * 0.3))
			g = int(bg_base[1] * (1.0 + progress * 0.3))
			b = int(bg_base[2] * (1.0 + progress * 0.3))
			pygame.draw.line(screen, (r, g, b), (0, i), (m.Disp.width, i))
		
		# СИНХРОНИЗИРОВАННОЕ вращение (один оборот за ~60 секунд)
		rotation_angle = (m.global_time * 6.0) % 360
		
		# Параметры доски
		center_x, center_y = m.Disp.width // 2, m.Disp.height // 2 - 40
		tile_size = 64
		
		angle_rad = math.radians(rotation_angle)
		cos_a = math.cos(angle_rad)
		sin_a = math.sin(angle_rad)
		
		# Рисуем каждую клетку как деформирующийся квад
		grid = []
		for gy in range(8):
			for gx in range(8):
				# 4 угла клетки в 3D (до вращения)
				corners_3d = []
				for dx, dz in [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]:
					x3d = (gx + dx - 4) * tile_size
					z3d = (gy + dz - 4) * tile_size
					
					# Вращаем вокруг Y оси
					rx = x3d * cos_a - z3d * sin_a
					rz = x3d * sin_a + z3d * cos_a
					
					# Изометрическая проекция
					px = center_x + rx - rz * 0.5
					py = center_y + (rx * 0.5 + rz * 0.5) * 0.5
					corners_3d.append((px, py))
				
				# Центр для сортировки
				center_z = (gx - 3.5) * tile_size * sin_a + (gy - 3.5) * tile_size * cos_a
				grid.append((gx, gy, corners_3d, center_z))
		
		# Подложка доски
		board_corners = []
		for corner_x, corner_z in [(-4, -4), (4, -4), (4, 4), (-4, 4)]:
			x3d = corner_x * tile_size
			z3d = corner_z * tile_size
			rx = x3d * cos_a - z3d * sin_a
			rz = x3d * sin_a + z3d * cos_a
			px = center_x + rx - rz * 0.5
			py = center_y + (rx * 0.5 + rz * 0.5) * 0.5
			board_corners.append((px, py))
		
		# Тень под доской
		shadow_corners = [(x + 8, y + 12) for x, y in board_corners]
		pygame.draw.polygon(screen, (0, 0, 0, 100), shadow_corners)
		pygame.draw.polygon(screen, colors['chessboard'], board_corners)
		
		# Сортируем по глубине
		grid.sort(key=lambda cell: cell[3])
		
		# Рисуем клетки
		for gx, gy, corners, _ in grid:
			# Тень
			shadow = [(px + 2, py + 3) for px, py in corners]
			pygame.draw.polygon(screen, (0, 0, 0, 40), shadow)
			
			# Цвет клетки
			color = colors['light_cell'] if (gx + gy) % 2 == 1 else colors['dark_cell']
			
			pygame.draw.polygon(screen, color, corners)
			pygame.draw.polygon(screen, (0, 0, 0, 30), corners, 1)
	
	def iso_diamond(self, cx, cy, w, h, scale=1.0):
		"""Создает ромб (изометрическая клетка)"""
		hw = (w * scale) / 2
		hh = (h * scale) / 2
		return [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]

	def update_and_draw_particles(self, m):
		"""Обновление и отрисовка атмосферных частиц"""
		import random
		screen = m.Disp.screen
		W, H = m.Disp.width, m.Disp.height
		
		# Обновляем частицы
		for p in self.particles[:]:
			p['x'] += p['vx'] * 0.016  # ~60 FPS
			p['y'] += p['vy'] * 0.016
			p['life'] -= 0.008
			
			# Перезапускаем частицу если она вышла за границы или умерла
			if p['y'] < -10 or p['x'] < -10 or p['x'] > W + 10 or p['life'] <= 0:
				p['x'] = random.uniform(0, W)
				p['y'] = H + 10
				p['vx'] = random.uniform(-15, 15)
				p['vy'] = random.uniform(-30, -10)
				p['life'] = random.uniform(0.5, 1.0)
				p['alpha'] = random.randint(50, 150)
		
		# Рисуем частицы с эффектом intro
		intro = min(1.0, self.intro_t * 1.5)
		for p in self.particles:
			if p['life'] > 0:
				alpha = int(p['alpha'] * p['life'] * intro)
				size = p['size']
				if size > 0 and alpha > 0:
					# Мягкий круг с градиентом
					surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
					for r in range(size, 0, -1):
						a = int(alpha * (r / size))
						pygame.draw.circle(surf, (255, 255, 255, a), (size * 2, size * 2), r)
					screen.blit(surf, (int(p['x'] - size * 2), int(p['y'] - size * 2)))

	def draw_title(self,m):

		text = "CHESS ISOMETRY REWORK"
		intro = min(1.0, self.intro_t)
		slide = int((1.0 - intro) * 40)
		
		# Легкая вибрация заголовка
		vibration = math.sin(self.pulse) * 2 if intro >= 1.0 else 0
		
		# Цветовой пульс для заголовка
		pulse_brightness = int(255 - abs(math.sin(self.pulse * 0.3)) * 30)
		title_color = (pulse_brightness, pulse_brightness, pulse_brightness)
		
		title = self.title_font.render(text, True, title_color)
		
		# Тень под заголовком для глубины
		shadow = self.title_font.render(text, True, (0, 0, 0, 128))
		shadow_rect = shadow.get_rect(center=(m.Disp.width//2 + vibration + 3, int(m.Disp.height*0.25) + slide + 3))
		shadow_surf = pygame.Surface(shadow.get_size(), pygame.SRCALPHA)
		shadow_surf.blit(shadow, (0, 0))
		shadow_surf.set_alpha(int(100 * intro))
		m.Disp.screen.blit(shadow_surf, shadow_rect)
		
		rect = title.get_rect(center=(m.Disp.width//2 + vibration, int(m.Disp.height*0.25) + slide))
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
			"Система мультиплеера",
			"Splash-тексты как в Minecraft",
			"Полная валидация шахматных правил"
		]
		
		y_offset = title_rect.bottom + 25
		
		for line in info_lines:
			color = (220, 220, 220)
			
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
			
			# Эффект свечения при hover с импульсом
			if is_hover:
				glow_pulse = abs(math.sin(self.pulse * 0.5)) * 0.3 + 0.7
				glow_size = 8
				glow_surface = pygame.Surface((animated_rect.width + glow_size * 2, animated_rect.height + glow_size * 2), pygame.SRCALPHA)
				for i in range(glow_size, 0, -1):
					glow_alpha = int((30 * (i / glow_size)) * glow_pulse * local)
					glow_rect = pygame.Rect(glow_size - i, glow_size - i, animated_rect.width + i * 2, animated_rect.height + i * 2)
					pygame.draw.rect(glow_surface, (100, 150, 255, glow_alpha), glow_rect, border_radius=8 + i)
				m.Disp.screen.blit(glow_surface, (animated_rect.x - glow_size, animated_rect.y - glow_size))
			
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


