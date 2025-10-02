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
        self.draw_sliders(m)
        self.draw_buttons(m)
        self.pulse += 0.03
    
    def draw_background(self, m):
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
        
        # СИНХРОНИЗИРОВАННОЕ вращение
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
                corners_3d = []
                for dx, dz in [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]:
                    x3d = (gx + dx - 4) * tile_size
                    z3d = (gy + dz - 4) * tile_size
                    
                    rx = x3d * cos_a - z3d * sin_a
                    rz = x3d * sin_a + z3d * cos_a
                    
                    px = center_x + rx - rz * 0.5
                    py = center_y + (rx * 0.5 + rz * 0.5) * 0.5
                    corners_3d.append((px, py))
                
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
        
        shadow_corners = [(x + 8, y + 12) for x, y in board_corners]
        pygame.draw.polygon(screen, (0, 0, 0, 100), shadow_corners)
        pygame.draw.polygon(screen, colors['chessboard'], board_corners)
        
        # Сортируем по глубине
        grid.sort(key=lambda cell: cell[3])
        
        # Рисуем клетки
        for gx, gy, corners, _ in grid:
            shadow = [(px + 2, py + 3) for px, py in corners]
            pygame.draw.polygon(screen, (0, 0, 0, 40), shadow)
            
            color = colors['light_cell'] if (gx + gy) % 2 == 1 else colors['dark_cell']
            pygame.draw.polygon(screen, color, corners)
            pygame.draw.polygon(screen, (0, 0, 0, 30), corners, 1)
    
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
            elif name == 'back': 
                label = 'BACK TO MENU'
                
            render = self.text_font.render(label, True, (255,255,255))
            lrect = render.get_rect(center=rect.center)
            m.Disp.screen.blit(render, lrect)
