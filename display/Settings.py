import pygame
import math
import sys
import os

class Settings:
    
    def __init__(self, m):
        
        self.title_font = pygame.font.Font(self.get_resource_path('data/font/title.ttf'), 48)
        self.text_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 24)
        self.small_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 18)
        self.pulse = 0
        self.intro_t = 0.0
        
    def get_resource_path(self, relative_path):
        """Получить абсолютный путь к ресурсу, работает как в разработке, так и в PyInstaller"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            return relative_path
    
    def main(self, m):
        self.draw_background(m)
        self.draw_title(m)
        self.draw_tabs(m)
        self.draw_sliders(m)
        self.draw_buttons(m)
        self.pulse += 0.03
    
    def draw_background(self, m):
        """Рисует фон. Поддерживает режимы 2D (статичная доска) и 3D (вращающаяся доска)."""
        screen = m.Disp.screen
        colors = m.Disp.colors['Game']
        
        # Градиентный фон всегда
        bg_base = colors['bg']
        for i in range(m.Disp.height):
            progress = i / m.Disp.height
            r = int(bg_base[0] * (1.0 + progress * 0.3))
            g = int(bg_base[1] * (1.0 + progress * 0.3))
            b = int(bg_base[2] * (1.0 + progress * 0.3))
            pygame.draw.line(screen, (r, g, b), (0, i), (m.Disp.width, i))
        
        # Режим 2D — статичная плоская шахматная доска
        if m.config.get('bg_mode', '3d') == '2d':
            center_x, center_y = m.Disp.width // 2, m.Disp.height // 2 - 40
            cell_size = 48
            board_size = 8
            total_size = cell_size * board_size
            start_x = center_x - total_size // 2
            start_y = center_y - total_size // 2
            
            # Тень под доской
            shadow_offset = 8
            shadow_rect = pygame.Rect(start_x + shadow_offset, start_y + shadow_offset, total_size, total_size)
            shadow_surf = pygame.Surface((total_size, total_size), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (0, 0, 0, 80), (0, 0, total_size, total_size), border_radius=8)
            screen.blit(shadow_surf, shadow_rect)
            
            # Подложка доски
            board_bg = pygame.Rect(start_x, start_y, total_size, total_size)
            pygame.draw.rect(screen, colors['chessboard'], board_bg, border_radius=8)
            
            # Рисуем клетки
            for row in range(board_size):
                for col in range(board_size):
                    x = start_x + col * cell_size
                    y = start_y + row * cell_size
                    color = colors['light_cell'] if (row + col) % 2 == 1 else colors['dark_cell']
                    cell_rect = pygame.Rect(x, y, cell_size, cell_size)
                    pygame.draw.rect(screen, color, cell_rect)
                    # Тонкие линии между клетками
                    pygame.draw.rect(screen, (0, 0, 0, 30), cell_rect, 1)
            
            # Рамка вокруг доски
            pygame.draw.rect(screen, colors['light_cell'], board_bg, 3, border_radius=8)
            return
        
        # 3D — изометрическая доска с вращением (в стиле 2D доски)
        rotation_angle = (m.global_time * 6.0) % 360
        center_x, center_y = m.Disp.width // 2, m.Disp.height // 2 - 40
        
        # Изометрические параметры
        cell_size = 48
        board_size = 8
        angle_rad = math.radians(rotation_angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # Проецируем доску в изометрию
        def to_iso(x, z):
            # Вращаем вокруг Y
            rx = x * cos_a - z * sin_a
            rz = x * sin_a + z * cos_a
            # Изометрическая проекция
            screen_x = center_x + (rx - rz) * 0.866  # sqrt(3)/2
            screen_y = center_y + (rx + rz) * 0.5
            return screen_x, screen_y
        
        # Собираем все клетки для сортировки по глубине
        cells = []
        for row in range(board_size):
            for col in range(board_size):
                world_x = (col - 3.5) * cell_size
                world_z = (row - 3.5) * cell_size
                depth = world_x * sin_a + world_z * cos_a
                cells.append((row, col, world_x, world_z, depth))
        
        # Сортируем от дальних к ближним
        cells.sort(key=lambda c: c[4])
        
        # Рисуем тень под доской
        board_corners = []
        for corner_col, corner_row in [(0, 0), (8, 0), (8, 8), (0, 8)]:
            wx = (corner_col - 4) * cell_size
            wz = (corner_row - 4) * cell_size
            board_corners.append(to_iso(wx, wz))
        
        shadow_corners = [(x + 10, y + 10) for x, y in board_corners]
        shadow_surf = pygame.Surface((m.Disp.width, m.Disp.height), pygame.SRCALPHA)
        pygame.draw.polygon(shadow_surf, (0, 0, 0, 60), shadow_corners)
        screen.blit(shadow_surf, (0, 0))
        
        # Рисуем подложку доски
        pygame.draw.polygon(screen, colors['chessboard'], board_corners)
        
        # Рисуем клетки
        for row, col, world_x, world_z, _ in cells:
            # 4 угла клетки
            corners = []
            for dx, dz in [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]:
                wx = world_x + dx * cell_size
                wz = world_z + dz * cell_size
                corners.append(to_iso(wx, wz))
            
            # Цвет клетки
            color = colors['light_cell'] if (row + col) % 2 == 1 else colors['dark_cell']
            
            # Рисуем клетку
            pygame.draw.polygon(screen, color, corners)
            pygame.draw.polygon(screen, (0, 0, 0, 60), corners, 1)
        
        # Рамка вокруг доски
        pygame.draw.polygon(screen, colors['light_cell'], board_corners, 4)
    
    def iso_diamond(self, cx, cy, w, h, scale=1.0):
        """Создает ромб"""
        hw = (w * scale) / 2
        hh = (h * scale) / 2
        return [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
    
    def draw_title(self, m):
        text = "SETTINGS"
        intro = min(1.0, self.intro_t)
        slide = int((1.0 - intro) * 40)
        
        title = self.title_font.render(text, True, (255,255,255))
        rect = title.get_rect(center=(m.Disp.width//2, int(m.Disp.height*0.2) + slide))
        m.Disp.screen.blit(title, rect)
        
        # Показываем текущий трек
        current_track = m.AudioManager.get_current_track_name()
        if current_track != "No music":
            track_text = f"♪ {current_track}"
            track_render = self.small_font.render(track_text, True, (180, 180, 180))
            track_rect = track_render.get_rect(center=(m.Disp.width//2, rect.bottom + 25))
            m.Disp.screen.blit(track_render, track_rect)

    def draw_tabs(self, m):
        from function.Settings import Settings as LogicSettings
        logic: LogicSettings = m.Settings
        colors = m.Disp.colors['Game']
        
        for name, rect in logic.tabs.items():
            is_active = (logic.active_tab == name)
            is_hover = (logic.hover == f"tab_{name}")
            base_color = colors['light_cell'] if (is_active or is_hover) else colors['dark_cell']
            pygame.draw.rect(m.Disp.screen, base_color, rect, border_radius=10)
            pygame.draw.rect(m.Disp.screen, colors['chessboard'], rect, 2, border_radius=10)
            label = self.text_font.render(name.upper(), True, (255,255,255))
            lrect = label.get_rect(center=rect.center)
            m.Disp.screen.blit(label, lrect)
    
    def draw_sliders(self, m):
        from function.Settings import Settings as LogicSettings
        logic: LogicSettings = m.Settings
        colors = m.Disp.colors['Game']
        
        for name, slider in logic.sliders.items():
            rect = slider["rect"]
            value = slider["value"]
            label = slider["label"]
            
            # Заголовок слайдера
            label_text = self.text_font.render(label, True, (255,255,255))
            label_rect = label_text.get_rect(center=(rect.centerx, rect.y - 30))
            m.Disp.screen.blit(label_text, label_rect)
            
            # Фон слайдера
            pygame.draw.rect(m.Disp.screen, colors['dark_cell'], rect, border_radius=10)
            pygame.draw.rect(m.Disp.screen, colors['chessboard'], rect, 2, border_radius=10)
            
            # Заполнение слайдера
            fill_width = int(rect.width * value)
            fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
            pygame.draw.rect(m.Disp.screen, colors['selected_cell'], fill_rect, border_radius=10)
            
            # Ручка слайдера
            handle_x = rect.x + fill_width
            handle_y = rect.centery
            pygame.draw.circle(m.Disp.screen, (255,255,255), (handle_x, handle_y), 12)
            pygame.draw.circle(m.Disp.screen, colors['chessboard'], (handle_x, handle_y), 12, 2)
            
            # Значение в процентах
            percent_text = f"{int(value * 100)}%"
            percent_render = self.small_font.render(percent_text, True, (200,200,200))
            percent_rect = percent_render.get_rect(center=(rect.centerx, rect.y + rect.height + 20))
            m.Disp.screen.blit(percent_render, percent_rect)
    
    def draw_buttons(self, m):
        from function.Settings import Settings as LogicSettings
        logic: LogicSettings = m.Settings
        colors = m.Disp.colors['Game']
        
        for name, rect in logic.buttons.items():
            is_hover = logic.hover == name
            base_color = colors['light_cell'] if is_hover else colors['dark_cell']
            pygame.draw.rect(m.Disp.screen, base_color, rect, border_radius=8)
            pygame.draw.rect(m.Disp.screen, colors['chessboard'], rect, 2, border_radius=8)
            
            label = name.upper()
            if name == 'fullscreen': 
                label = 'FULLSCREEN ON' if m.config['fullscreen'] else 'FULLSCREEN OFF'
            elif name == 'bg_mode':
                mode = m.config.get('bg_mode', '3d').upper()
                label = f'BG MODE: {mode}'
            elif name == 'f3_toggle':
                label = 'F3 DEBUG: ON' if m.config.get('f3', False) else 'F3 DEBUG: OFF'
            elif name == 'back': 
                label = 'BACK TO MENU'
                
            render = self.text_font.render(label, True, (255,255,255))
            lrect = render.get_rect(center=rect.center)
            m.Disp.screen.blit(render, lrect)
