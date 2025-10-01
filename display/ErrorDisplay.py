import pygame

class ErrorDisplay:
    """Визуальное отображение окна ошибок"""
    
    def __init__(self):
        pass
    
    def draw_error_window(self, m, error_info: dict):
        """Рисует окно ошибки поверх всего"""
        screen = m.Disp.screen
        width, height = m.Disp.width, m.Disp.height
        
        # Получаем цвета из темы
        try:
            colors = m.Disp.colors['Game']
            bg_color = colors['bg']
            dark_cell = colors['dark_cell']
            border_color = colors['chessboard']
        except:
            # Fallback цвета если тема не загружена
            bg_color = (40, 44, 52)
            dark_cell = (33, 37, 43)
            border_color = (51, 56, 66)
        
        # Полупрозрачный фон в стиле игры
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((*bg_color, 220))
        screen.blit(overlay, (0, 0))
        
        # Размеры окна ошибки
        error_width = min(900, width - 100)
        error_height = min(550, height - 100)
        error_x = (width - error_width) // 2
        error_y = (height - error_height) // 2
        
        # Основной фон окна с тёмной темой
        error_rect = pygame.Rect(error_x, error_y, error_width, error_height)
        pygame.draw.rect(screen, dark_cell, error_rect, border_radius=12)
        
        # Граница в стиле шахматной доски
        pygame.draw.rect(screen, border_color, error_rect, 3, border_radius=12)
        
        # Красная полоса сверху для акцента ошибки
        header_rect = pygame.Rect(error_x, error_y, error_width, 70)
        pygame.draw.rect(screen, (60, 20, 20), header_rect, border_top_left_radius=12, border_top_right_radius=12)
        pygame.draw.rect(screen, (180, 60, 60), header_rect, 2, border_top_left_radius=12, border_top_right_radius=12)
        
        # Заголовок - используем шрифты игры или fallback
        try:
            title_font = pygame.font.Font(m.AssetManager.font['title'], 36)
            text_font = pygame.font.Font(m.AssetManager.font['text'], 18)
            small_font = pygame.font.Font(m.AssetManager.font['text'], 15)
        except:
            # Fallback на системный шрифт
            title_font = pygame.font.Font(None, 36)
            text_font = pygame.font.Font(None, 18)
            small_font = pygame.font.Font(None, 15)
        
        # Заголовок с иконкой
        title_text = title_font.render("⚠ CRITICAL ERROR", True, (255, 120, 120))
        title_rect = title_text.get_rect(center=(width // 2, error_y + 35))
        screen.blit(title_text, title_rect)
        
        # Тонкая линия разделителя
        pygame.draw.line(screen, border_color, 
                        (error_x + 30, error_y + 75), 
                        (error_x + error_width - 30, error_y + 75), 2)
        
        # Информация об ошибке в компактных блоках
        y_offset = error_y + 95
        
        # Блок с типом ошибки
        info_bg = pygame.Rect(error_x + 30, y_offset, error_width - 60, 40)
        pygame.draw.rect(screen, (50, 50, 60), info_bg, border_radius=6)
        type_text = text_font.render(f"Type: {error_info['type']}", True, (255, 180, 180))
        screen.blit(type_text, (error_x + 45, y_offset + 10))
        y_offset += 50
        
        # Блок с сообщением
        message = error_info['message']
        if len(message) > 90:
            # Разбиваем длинное сообщение
            words = message.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if len(test_line) > 90:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
            
            msg_height = 30 + len(lines[:3]) * 22
            msg_bg = pygame.Rect(error_x + 30, y_offset, error_width - 60, msg_height)
            pygame.draw.rect(screen, (50, 50, 60), msg_bg, border_radius=6)
            
            msg_label = text_font.render("Message:", True, (255, 200, 150))
            screen.blit(msg_label, (error_x + 45, y_offset + 8))
            y_offset += 28
            
            for line in lines[:3]:
                msg_text = small_font.render(line, True, (230, 230, 230))
                screen.blit(msg_text, (error_x + 50, y_offset))
                y_offset += 22
            y_offset += 10
        else:
            msg_bg = pygame.Rect(error_x + 30, y_offset, error_width - 60, 40)
            pygame.draw.rect(screen, (50, 50, 60), msg_bg, border_radius=6)
            msg_text = text_font.render(f"Message: {message}", True, (255, 200, 150))
            screen.blit(msg_text, (error_x + 45, y_offset + 10))
            y_offset += 50
        
        # Блок локации ошибки (самое важное!)
        location_bg = pygame.Rect(error_x + 30, y_offset, error_width - 60, 100)
        pygame.draw.rect(screen, (70, 30, 30), location_bg, border_radius=6)
        pygame.draw.rect(screen, (180, 60, 60), location_bg, 2, border_radius=6)
        
        file_text = text_font.render(f"📁 {error_info['file']}", True, (255, 220, 120))
        screen.blit(file_text, (error_x + 45, y_offset + 12))
        
        line_text = text_font.render(f"Line {error_info['line']}", True, (255, 180, 100))
        line_rect = line_text.get_rect(right=error_x + error_width - 45, centery=y_offset + 22)
        screen.blit(line_text, line_rect)
        
        func_text = small_font.render(f"in {error_info['function']}()", True, (200, 200, 200))
        screen.blit(func_text, (error_x + 45, y_offset + 42))
        
        # Код в этом же блоке
        if error_info['code']:
            code = error_info['code'].strip()
            if len(code) > 95:
                code = code[:92] + "..."
            code_text = small_font.render(f"> {code}", True, (150, 255, 150))
            screen.blit(code_text, (error_x + 45, y_offset + 68))
        
        y_offset += 110
        
        # Timestamp внизу слева
        time_text = small_font.render(f"⏰ {error_info['timestamp']}", True, (130, 130, 140))
        screen.blit(time_text, (error_x + 35, error_y + error_height - 25))
        
        # Кнопки в стиле игры
        button_y = error_y + error_height - 65
        button_width = 160
        button_height = 45
        button_spacing = 20
        
        # Позиции кнопок
        total_width = button_width * 2 + button_spacing
        start_x = error_x + (error_width - total_width) // 2
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Кнопка "CONTINUE"
        close_btn_rect = pygame.Rect(start_x, button_y, button_width, button_height)
        close_hover = close_btn_rect.collidepoint(mouse_pos)
        
        # Используем цвета из темы для кнопок
        try:
            light_cell = colors['light_cell']
            btn_border = border_color
        except:
            light_cell = (204, 204, 204)
            btn_border = (51, 56, 66)
        
        close_color = light_cell if close_hover else dark_cell
        pygame.draw.rect(screen, close_color, close_btn_rect, border_radius=8)
        pygame.draw.rect(screen, btn_border, close_btn_rect, 3, border_radius=8)
        
        close_text = text_font.render("CONTINUE", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=close_btn_rect.center)
        screen.blit(close_text, close_text_rect)
        
        # Кнопка "OPEN LOG"
        log_btn_rect = pygame.Rect(start_x + button_width + button_spacing, button_y, button_width, button_height)
        log_hover = log_btn_rect.collidepoint(mouse_pos)
        
        log_color = light_cell if log_hover else dark_cell
        pygame.draw.rect(screen, log_color, log_btn_rect, border_radius=8)
        pygame.draw.rect(screen, btn_border, log_btn_rect, 3, border_radius=8)
        
        log_text = text_font.render("OPEN LOG", True, (255, 255, 255))
        log_text_rect = log_text.get_rect(center=log_btn_rect.center)
        screen.blit(log_text, log_text_rect)
        
        # Подсказка справа от timestamp
        hint_text = small_font.render("Saved: data/error_log.txt", True, (130, 130, 140))
        hint_rect = hint_text.get_rect(right=error_x + error_width - 35, centery=error_y + error_height - 25)
        screen.blit(hint_text, hint_rect)
        
        return close_btn_rect, log_btn_rect
    
    def handle_error_input(self, m, mouse_pos, close_rect, log_rect):
        """Обрабатывает клики по кнопкам окна ошибки"""
        import os
        import subprocess
        import sys
        
        if close_rect.collidepoint(mouse_pos):
            # Закрыть окно ошибки
            m.ErrorHandler.clear_error()
            return True
        
        elif log_rect.collidepoint(mouse_pos):
            # Открыть файл лога
            log_path = os.path.abspath(m.ErrorHandler.error_log_file)
            try:
                if sys.platform == 'win32':
                    os.startfile(log_path)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', log_path])
                else:
                    subprocess.run(['xdg-open', log_path])
            except:
                print(f"📁 Лог находится в: {log_path}")
            return True
        
        return False
