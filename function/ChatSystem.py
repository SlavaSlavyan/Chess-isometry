import pygame
import time
from typing import List, Dict, Any
from datetime import datetime

class ChatMessage:
    """Класс для представления сообщения в чате"""
    
    def __init__(self, sender: str, text: str, message_type: str = "normal", timestamp: float = None):
        self.sender = sender
        self.text = text
        self.type = message_type  # "normal", "system", "error", "info"
        self.timestamp = timestamp or time.time()
        self.datetime = datetime.fromtimestamp(self.timestamp)
    
    def get_formatted_time(self) -> str:
        """Возвращает отформатированное время"""
        return self.datetime.strftime("%H:%M")

class ChatSystem:
    """Система чата для мультиплеера"""
    
    def __init__(self, max_messages: int = 50):
        self.messages: List[ChatMessage] = []
        self.max_messages = max_messages
        
        # Настройки отображения
        self.visible = False
        self.input_active = False
        self.input_text = ""
        self.scroll_offset = 0
        
        # Размеры и позиция чата
        self.chat_width = 350
        self.chat_height = 200
        self.input_height = 30
        self.message_height = 20
        
        # Шрифты
        try:
            self.message_font = pygame.font.Font("data/font/text.ttf", 14)
            self.input_font = pygame.font.Font("data/font/text.ttf", 16)
            self.time_font = pygame.font.Font("data/font/text.ttf", 10)
        except:
            self.message_font = pygame.font.Font(None, 14)
            self.input_font = pygame.font.Font(None, 16)
            self.time_font = pygame.font.Font(None, 10)
        
        # Цвета
        self.colors = {
            'background': (0, 0, 0, 100),  # Более прозрачный фон
            'border': (100, 100, 100, 150),  # Полупрозрачная рамка
            'input_bg': (20, 20, 20, 120),  # Полупрозрачный фон ввода
            'input_border': (120, 120, 120, 180),
            'input_active': (40, 40, 40, 150),  # Полупрозрачный активный фон
            'text_normal': (255, 255, 255),
            'text_system': (100, 255, 100),
            'text_error': (255, 100, 100),
            'text_info': (100, 200, 255),
            'text_time': (150, 150, 150),
            'sender': (255, 255, 100)
        }
        
        # Callback для отправки сообщений
        self.on_message_send = None
        
        # Автоматическое скрытие
        self.auto_hide_timer = 0
        self.auto_hide_delay = 10.0  # секунд
        
    def add_message(self, sender: str, text: str, message_type: str = "normal"):
        """Добавляет сообщение в чат"""
        message = ChatMessage(sender, text, message_type)
        self.messages.append(message)
        
        # Ограничиваем количество сообщений
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        
        # Автоматически скроллим вниз при новом сообщении
        self.scroll_to_bottom()
        
        # Показываем чат на несколько секунд при новом сообщении
        if not self.visible and message_type != "system":
            self.visible = True
            self.auto_hide_timer = time.time()
    
    def add_system_message(self, text: str):
        """Добавляет системное сообщение"""
        self.add_message("СИСТЕМА", text, "system")
    
    def add_info_message(self, text: str):
        """Добавляет информационное сообщение"""
        self.add_message("ИНФО", text, "info")
    
    def add_error_message(self, text: str):
        """Добавляет сообщение об ошибке"""
        self.add_message("ОШИБКА", text, "error")
    
    def toggle_visibility(self):
        """Переключает видимость чата"""
        self.visible = not self.visible
        if self.visible:
            self.auto_hide_timer = 0  # Отключаем автоскрытие при ручном открытии
    
    def show(self):
        """Показывает чат"""
        self.visible = True
        self.auto_hide_timer = 0
    
    def hide(self):
        """Скрывает чат"""
        self.visible = False
        self.input_active = False
    
    def start_input(self):
        """Начинает ввод сообщения"""
        self.input_active = True
        self.input_text = ""
        self.visible = True
        self.auto_hide_timer = 0
    
    def stop_input(self):
        """Останавливает ввод сообщения"""
        self.input_active = False
        self.input_text = ""
    
    def handle_key_input(self, event):
        """Обрабатывает ввод с клавиатуры"""
        if not self.input_active:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Отправляем сообщение
                self.send_message()
                return True
            elif event.key == pygame.K_ESCAPE:
                # Отменяем ввод
                self.stop_input()
                return True
            elif event.key == pygame.K_BACKSPACE:
                # Удаляем символ
                self.input_text = self.input_text[:-1]
                return True
            else:
                # Добавляем символ
                if len(self.input_text) < 100 and event.unicode.isprintable():
                    self.input_text += event.unicode
                return True
        
        return False
    
    def handle_scroll(self, y_offset: int):
        """Обрабатывает прокрутку чата"""
        if not self.visible:
            return
        
        max_scroll = max(0, len(self.messages) - self.get_visible_messages_count())
        self.scroll_offset = max(0, min(max_scroll, self.scroll_offset + y_offset))
    
    def get_visible_messages_count(self) -> int:
        """Возвращает количество видимых сообщений"""
        return self.chat_height // self.message_height
    
    def scroll_to_bottom(self):
        """Прокручивает к последнему сообщению"""
        visible_count = self.get_visible_messages_count()
        self.scroll_offset = max(0, len(self.messages) - visible_count)
    
    def send_message(self):
        """Отправляет введенное сообщение"""
        if self.input_text.strip() and self.on_message_send:
            self.on_message_send(self.input_text.strip())
        self.stop_input()
    
    def update(self, dt: float):
        """Обновляет состояние чата"""
        # Автоматическое скрытие
        if self.visible and self.auto_hide_timer > 0 and not self.input_active:
            if time.time() - self.auto_hide_timer > self.auto_hide_delay:
                self.visible = False
                self.auto_hide_timer = 0
    
    def draw(self, screen: pygame.Surface, x: int, y: int):
        """Рисует чат на экране"""
        if not self.visible:
            return
        
        # Фон чата
        chat_surface = pygame.Surface((self.chat_width, self.chat_height + self.input_height), pygame.SRCALPHA)
        chat_surface.fill(self.colors['background'])
        
        # Рамка
        pygame.draw.rect(chat_surface, self.colors['border'], 
                        (0, 0, self.chat_width, self.chat_height + self.input_height), 2)
        
        # Рисуем сообщения
        self.draw_messages(chat_surface)
        
        # Рисуем поле ввода
        self.draw_input(chat_surface)
        
        # Отображаем на основном экране
        screen.blit(chat_surface, (x, y))
    
    def draw_messages(self, surface: pygame.Surface):
        """Рисует сообщения в чате"""
        visible_count = self.get_visible_messages_count()
        # Всегда показываем последние сообщения (scroll_offset должен быть 0 для новых сообщений)
        start_index = max(0, len(self.messages) - visible_count)
        end_index = len(self.messages)
        
        y_offset = 5
        
        for i in range(start_index, end_index):
            message = self.messages[i]
            
            # Определяем цвет текста
            if message.type == "system":
                text_color = self.colors['text_system']
            elif message.type == "error":
                text_color = self.colors['text_error']
            elif message.type == "info":
                text_color = self.colors['text_info']
            else:
                text_color = self.colors['text_normal']
            
            # Время
            time_text = self.time_font.render(message.get_formatted_time(), True, self.colors['text_time'])
            surface.blit(time_text, (5, y_offset))
            
            # Отправитель
            sender_text = self.message_font.render(f"{message.sender}:", True, self.colors['sender'])
            sender_width = sender_text.get_width()
            surface.blit(sender_text, (35, y_offset))
            
            # Сообщение (с переносом если нужно)
            message_x = 35 + sender_width + 5
            available_width = self.chat_width - message_x - 10
            wrapped_lines = self.wrap_text(message.text, available_width)
            
            for line in wrapped_lines:
                if y_offset < self.chat_height - self.message_height:
                    line_surface = self.message_font.render(line, True, text_color)
                    surface.blit(line_surface, (message_x, y_offset))
                    y_offset += self.message_height
                else:
                    break
            
            if y_offset >= self.chat_height - self.message_height:
                break
    
    def wrap_text(self, text: str, max_width: int) -> List[str]:
        """Переносит текст по словам"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_width = self.message_font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Слово слишком длинное, разбиваем принудительно
                    lines.append(word)
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def draw_input(self, surface: pygame.Surface):
        """Рисует поле ввода"""
        input_y = self.chat_height
        
        # Создаем поверхность для фона ввода с альфа-каналом
        input_rect = pygame.Rect(2, input_y + 2, self.chat_width - 4, self.input_height - 4)
        input_surface = pygame.Surface((input_rect.width, input_rect.height), pygame.SRCALPHA)
        
        # Фон поля ввода
        input_color = self.colors['input_active'] if self.input_active else self.colors['input_bg']
        input_surface.fill(input_color)
        surface.blit(input_surface, (input_rect.x, input_rect.y))
        
        # Рамка поля ввода
        border_color = self.colors['input_border']
        pygame.draw.rect(surface, border_color, input_rect, 1)
        
        # Текст в поле ввода
        display_text = self.input_text
        if self.input_active:
            # Добавляем курсор
            cursor_visible = int(time.time() * 2) % 2
            if cursor_visible:
                display_text += "|"
        
        if display_text or self.input_active:
            text_surface = self.input_font.render(display_text, True, self.colors['text_normal'])
            surface.blit(text_surface, (8, input_y + 8))
        else:
            # Placeholder
            placeholder = self.input_font.render("Нажмите Enter для ввода...", True, self.colors['text_time'])
            surface.blit(placeholder, (8, input_y + 8))
