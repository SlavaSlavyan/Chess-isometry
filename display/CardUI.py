"""
UI для отображения и взаимодействия с картами
"""

import pygame
import math

class CardUI:
    """Отображение карт на экране"""
    
    def __init__(self, m):
        import sys
        import os
        
        def get_resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return relative_path
        
        self.card_font = pygame.font.Font(get_resource_path('data/font/text.ttf'), 16)
        self.small_font = pygame.font.Font(get_resource_path('data/font/text.ttf'), 12)
        self.icon_font = pygame.font.Font(get_resource_path('data/font/text.ttf'), 32)
        
        self.card_width = 120
        self.card_height = 160
        self.card_spacing = 10
        self.hover_index = -1
        self.selected_index = -1
        
        # Анимация
        self.card_animations = {}  # {index: {'offset': y, 'scale': s}}
    
    def draw_player_hand(self, screen, cards_info, player, screen_width, screen_height, selected_card_index=None):
        """
        Рисует карты игрока внизу экрана
        
        Args:
            screen: Pygame surface
            cards_info: Список словарей с информацией о картах
            player: 'white' или 'black'
            screen_width, screen_height: Размеры экрана
            selected_card_index: Индекс выбранной карты (для подсветки)
        """
        if not cards_info:
            self.hover_index = -1  # Сбрасываем если нет карт
            return
        
        num_cards = len(cards_info)
        total_width = num_cards * self.card_width + (num_cards - 1) * self.card_spacing
        start_x = (screen_width - total_width) // 2
        base_y = screen_height - self.card_height - 20
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Сбрасываем hover перед проверкой
        self.hover_index = -1
        
        for i, card_info in enumerate(cards_info):
            x = start_x + i * (self.card_width + self.card_spacing)
            
            # Анимация при наведении
            if i not in self.card_animations:
                self.card_animations[i] = {'offset': 0, 'scale': 1.0}
            
            anim = self.card_animations[i]
            
            # Проверяем наведение
            card_rect = pygame.Rect(x, base_y, self.card_width, self.card_height)
            is_hovered = card_rect.collidepoint(mouse_pos)
            is_selected = (i == selected_card_index)
            
            # Плавная анимация
            target_offset = -15 if (is_hovered or is_selected) else 0
            target_scale = 1.1 if (is_hovered or is_selected) else 1.0
            
            anim['offset'] += (target_offset - anim['offset']) * 0.3
            anim['scale'] += (target_scale - anim['scale']) * 0.3
            
            y = base_y + anim['offset']
            
            # Рисуем карту
            self._draw_card(screen, x, int(y), card_info, is_hovered or is_selected, anim['scale'], is_selected)
            
            # Устанавливаем hover только если мышь действительно над картой
            if is_hovered:
                self.hover_index = i
    
    def _draw_card(self, screen, x, y, card_info, is_hovered, scale, is_selected=False):
        """Рисует одну карту"""
        w = int(self.card_width * scale)
        h = int(self.card_height * scale)
        
        # Корректируем позицию для центрирования масштабированной карты
        x_offset = (self.card_width - w) // 2
        y_offset = (self.card_height - h) // 2
        
        cx = x + x_offset
        cy = y + y_offset
        
        # Создаем поверхность для карты
        card_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        
        # Тень
        shadow_surface = pygame.Surface((w + 6, h + 6), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 100), (0, 0, w + 6, h + 6), border_radius=10)
        screen.blit(shadow_surface, (cx - 3, cy + 3))
        
        # Фон карты с градиентом редкости
        rarity_colors = {
            'common': (200, 200, 200),
            'rare': (100, 150, 255),
            'epic': (200, 100, 255),
            'legendary': (255, 180, 50)
        }
        
        rarity = card_info.get('rarity', 'common')
        border_color = rarity_colors.get(rarity, (200, 200, 200))
        
        # Фон (ярче если выбрана)
        if is_selected:
            bg_color = (60, 70, 80)
        else:
            bg_color = (40, 40, 50) if not is_hovered else (50, 50, 60)
        pygame.draw.rect(card_surface, bg_color, (0, 0, w, h), border_radius=10)
        
        # Рамка с цветом редкости (толще и ярче если выбрана)
        if is_selected:
            border_width = 5
            # Пульсирующая рамка для выбранной карты
            import math
            pulse = abs(math.sin(pygame.time.get_ticks() / 300.0))
            bright_border = tuple(min(255, int(c * (1.0 + pulse * 0.3))) for c in border_color)
            pygame.draw.rect(card_surface, bright_border, (0, 0, w, h), border_width, border_radius=10)
        else:
            border_width = 4 if is_hovered else 3
            pygame.draw.rect(card_surface, border_color, (0, 0, w, h), border_width, border_radius=10)
        
        # Иконка карты
        icon = card_info.get('icon', '🃏')
        try:
            icon_render = self.icon_font.render(icon, True, (255, 255, 255))
            icon_rect = icon_render.get_rect(center=(w//2, 40))
            card_surface.blit(icon_render, icon_rect)
        except:
            pass
        
        # Название карты
        name = card_info.get('name', 'Unknown')
        name_lines = self._wrap_text(name, self.card_font, w - 10)
        y_pos = 75
        for line in name_lines:
            name_render = self.card_font.render(line, True, (255, 255, 255))
            name_rect = name_render.get_rect(center=(w//2, y_pos))
            card_surface.blit(name_render, name_rect)
            y_pos += 18
        
        # Описание
        desc = card_info.get('description', '')
        desc_lines = self._wrap_text(desc, self.small_font, w - 10)
        y_pos = 105
        for line in desc_lines[:3]:  # Максимум 3 строки
            desc_render = self.small_font.render(line, True, (200, 200, 200))
            desc_rect = desc_render.get_rect(center=(w//2, y_pos))
            card_surface.blit(desc_render, desc_rect)
            y_pos += 14
        
        # Кулдаун
        current_cd = card_info.get('current_cooldown', 0)
        if current_cd > 0:
            cd_text = f"CD: {current_cd}"
            cd_render = self.small_font.render(cd_text, True, (255, 100, 100))
            cd_rect = cd_render.get_rect(bottomright=(w - 5, h - 5))
            card_surface.blit(cd_render, cd_rect)
        
        # Редкость
        rarity_text = rarity.upper()
        rarity_render = self.small_font.render(rarity_text, True, border_color)
        rarity_rect = rarity_render.get_rect(bottomleft=(5, h - 5))
        card_surface.blit(rarity_render, rarity_rect)
        
        # Отображаем карту на экране
        screen.blit(card_surface, (cx, cy))
    
    def _wrap_text(self, text, font, max_width):
        """Переносит текст на несколько строк"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def draw_card_notification(self, screen, card_info, screen_width, screen_height, progress):
        """
        Рисует уведомление о получении новой карты
        
        Args:
            progress: 0.0 - 1.0, прогресс анимации
        """
        if progress <= 0:
            return
        
        # Анимация появления
        alpha = int(255 * min(progress * 2, 1.0))
        scale = 0.5 + 0.5 * min(progress * 1.5, 1.0)
        
        w = int(300 * scale)
        h = int(120 * scale)
        x = (screen_width - w) // 2
        y = int(screen_height * 0.3 - h * progress * 0.2)
        
        # Создаем поверхность
        notif_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        
        # Фон
        bg_color = (60, 40, 80, alpha)
        pygame.draw.rect(notif_surface, bg_color, (0, 0, w, h), border_radius=15)
        
        # Рамка
        rarity_colors = {
            'common': (200, 200, 200),
            'rare': (100, 150, 255),
            'epic': (200, 100, 255),
            'legendary': (255, 180, 50)
        }
        rarity = card_info.get('rarity', 'common')
        border_color = (*rarity_colors.get(rarity, (200, 200, 200)), alpha)
        pygame.draw.rect(notif_surface, border_color, (0, 0, w, h), 4, border_radius=15)
        
        # Текст "NEW CARD!"
        title_render = self.card_font.render("NEW CARD!", True, (255, 255, 255))
        title_render.set_alpha(alpha)
        title_rect = title_render.get_rect(center=(w//2, 25))
        notif_surface.blit(title_render, title_rect)
        
        # Иконка
        icon = card_info.get('icon', '🃏')
        try:
            icon_render = self.icon_font.render(icon, True, (255, 255, 255))
            icon_render.set_alpha(alpha)
            icon_rect = icon_render.get_rect(center=(w//2, 65))
            notif_surface.blit(icon_render, icon_rect)
        except:
            pass
        
        # Название
        name = card_info.get('name', 'Unknown')
        name_render = self.small_font.render(name, True, (255, 255, 255))
        name_render.set_alpha(alpha)
        name_rect = name_render.get_rect(center=(w//2, 95))
        notif_surface.blit(name_render, name_rect)
        
        screen.blit(notif_surface, (x, y))
    
    def get_hovered_card(self):
        """Возвращает индекс карты под курсором"""
        return self.hover_index if self.hover_index >= 0 else None
    
    def reset_hover(self):
        """Сбрасывает состояние наведения"""
        self.hover_index = -1

