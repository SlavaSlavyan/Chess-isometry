import pygame
import sys
import os

class Menu:

	def __init__(self,m):

		self.buttons = {}
		self.hover = None
		self.author_rect = None
		self.show_about = False
		
	def get_resource_path(self, relative_path):
		"""Получить абсолютный путь к ресурсу, работает как в разработке, так и в PyInstaller"""
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, relative_path)
		else:
			return relative_path

	def main(self,m):

		self.layout(m)
		self.handle_input(m)

	def layout(self,m):

		width, height = m.Disp.width, m.Disp.height
		btn_w, btn_h = int(width*0.22), 48
		cx = width//2 - btn_w//2
		
		# Проверяем, есть ли активная игра (игра считается активной, если был сделан хотя бы один ход)
		has_active_game = hasattr(m.PI.Game, 'game_started') and getattr(m.PI.Game, 'game_started', False)
		
		button_count = 4 if has_active_game else 3
		start_y = height//2 - int(btn_h * button_count / 2) - 10
		
		self.buttons = {}
		y_offset = 0
		
		if has_active_game:
			self.buttons["continue"] = pygame.Rect(cx, start_y + y_offset, btn_w, btn_h)
			y_offset += btn_h + 12
		
		self.buttons["play"] = pygame.Rect(cx, start_y + y_offset, btn_w, btn_h)
		y_offset += btn_h + 12
		self.buttons["settings"] = pygame.Rect(cx, start_y + y_offset, btn_w, btn_h)
		y_offset += btn_h + 12
		self.buttons["exit"] = pygame.Rect(cx, start_y + y_offset, btn_w, btn_h)
		
		# Область для клика по нику автора (нижний правый угол)
		author_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 18)  # Увеличиваем шрифт
		author_text = author_font.render("revor by Heck43 :3", True, (140, 140, 140))  # Серый цвет
		author_w, author_h = author_text.get_size()
		self.author_rect = pygame.Rect(width - author_w - 20, height - author_h - 15, author_w, author_h)

	def handle_input(self,m):

		mouse_pos = m.PI.MI.mouse_pos
		self.hover = None
		for name, rect in self.buttons.items():
			if rect.collidepoint(mouse_pos):
				self.hover = name
		
		# Проверяем наведение на ник автора
		if self.author_rect and self.author_rect.collidepoint(mouse_pos):
			self.hover = "author"

		if m.PI.MI.mouse_click['lt']:
			if self.hover == "continue":
				# Продолжаем текущую игру с анимацией входа
				m.set_scene('game')
			elif self.hover == "play":
				# Новая игра с анимацией входа
				m.PI.Game.restart_game(m)
				m.set_scene('game')
			elif self.hover == "settings":
				# Переходим в настройки
				m.set_scene('settings')
			elif self.hover == "author":
				# Показываем/скрываем информацию об авторе
				self.show_about = not self.show_about
			elif self.hover == "exit":
				m.stop()
		
		# Закрываем окно "О проекте" при клике вне его
		if m.PI.MI.mouse_click['lt'] and self.show_about and self.hover not in ["author", "about_window"]:
			self.show_about = False


