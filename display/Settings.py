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
        
        # Кеш для фоновой поверхности  
        self.background_surface = None
        self.background_cached = False
        self.cached_size = (0, 0)  # Запоминаем размер для которого создан фон
    
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
        screen = m.Disp.screen
        colors = m.Disp.colors['Game']
        screen.fill(colors['bg'])
        
        # Проверяем изменился ли размер экрана
        current_size = (m.Disp.width, m.Disp.height)
        if current_size != self.cached_size:
            self.background_cached = False
            self.cached_size = current_size

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
            
            # Рисуем основу доски (такая же как в игре)
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
                        light_color = (*colors['light_cell'], 120)  # Такая же прозрачность как в меню
                        pygame.draw.polygon(self.background_surface, light_color, temp_cells[y][x])
            
            # Восстанавливаем оригинальные настройки
            m.Disp.Game.rotate = original_rotate
            m.config['zoom'] = original_zoom
            
            self.background_cached = True

        # Рисуем кешированную поверхность с анимацией
        intro = min(1.0, self.intro_t)
        offset_y = int((1.0 - intro) * m.Disp.height * 0.10)
        
        screen.blit(self.background_surface, (0, offset_y))
    
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
