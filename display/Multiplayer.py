import pygame
import math
import time
import sys
import os

class Multiplayer:
    """Отображение интерфейса мультиплеера"""
    
    def __init__(self, m):
        # Шрифты
        try:
            self.title_font = pygame.font.Font(self.get_resource_path('data/font/title.ttf'), 48)
            self.subtitle_font = pygame.font.Font(self.get_resource_path('data/font/title.ttf'), 24)
            self.text_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 18)
            self.small_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 14)
        except:
            self.title_font = pygame.font.Font(None, 48)
            self.subtitle_font = pygame.font.Font(None, 24)
            self.text_font = pygame.font.Font(None, 18)
            self.small_font = pygame.font.Font(None, 14)
        
        # Анимация
        self.pulse = 0
        self.intro_t = 0.0
    
    def get_resource_path(self, relative_path):
        """Получить абсолютный путь к ресурсу"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            return relative_path
    
    def main(self, m):
        """Основной метод отрисовки"""
        self.draw_background(m)
        
        if m.Multiplayer.state == "menu":
            self.draw_main_menu(m)
        elif m.Multiplayer.state == "profile":
            self.draw_profile_setup(m)
        elif m.Multiplayer.state == "hosting":
            self.draw_hosting(m)
        elif m.Multiplayer.state == "connecting":
            self.draw_connecting(m)
        elif m.Multiplayer.state == "lobby":
            self.draw_lobby(m)
        elif m.Multiplayer.state == "waiting":
            self.draw_waiting(m)
        
        # Рисуем редактор аватаров поверх всего
        if hasattr(m.Multiplayer, 'avatar_editor') and m.Multiplayer.avatar_editor and m.Multiplayer.avatar_editor.active:
            colors = m.Disp.colors['Game']
            m.Multiplayer.avatar_editor.draw(m.Disp.screen, m.Disp.width, m.Disp.height, colors)
        
        # Обновляем анимацию
        self.pulse += 0.03
        self.intro_t += 1/60.0
    
    def draw_background(self, m):
        """Рисует фон. Поддерживает 2D/3D режимы в соответствии с config['bg_mode']."""
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
        
        if m.config.get('bg_mode', '3d') == '2d':
            # 2D: статичная плоская доска
            center_x, center_y = m.Disp.width // 2, m.Disp.height // 2 - 40
            cell_size = 48
            board_size = 8
            total_size = cell_size * board_size
            start_x = center_x - total_size // 2
            start_y = center_y - total_size // 2
            
            shadow_offset = 8
            shadow_rect = pygame.Rect(start_x + shadow_offset, start_y + shadow_offset, total_size, total_size)
            shadow_surf = pygame.Surface((total_size, total_size), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (0, 0, 0, 80), (0, 0, total_size, total_size), border_radius=8)
            screen.blit(shadow_surf, shadow_rect)
            
            board_bg = pygame.Rect(start_x, start_y, total_size, total_size)
            pygame.draw.rect(screen, colors['chessboard'], board_bg, border_radius=8)
            
            for row in range(board_size):
                for col in range(board_size):
                    x = start_x + col * cell_size
                    y = start_y + row * cell_size
                    color = colors['light_cell'] if (row + col) % 2 == 1 else colors['dark_cell']
                    cell_rect = pygame.Rect(x, y, cell_size, cell_size)
                    pygame.draw.rect(screen, color, cell_rect)
                    pygame.draw.rect(screen, (0, 0, 0, 30), cell_rect, 1)
            
            pygame.draw.rect(screen, colors['light_cell'], board_bg, 3, border_radius=8)
            return
        
        # 3D: изометрическая доска с вращением (в стиле 2D доски)
        rotation_angle = (m.global_time * 6.0) % 360
        center_x, center_y = m.Disp.width // 2, m.Disp.height // 2 - 40
        
        cell_size = 48
        board_size = 8
        angle_rad = math.radians(rotation_angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        def to_iso(x, z):
            rx = x * cos_a - z * sin_a
            rz = x * sin_a + z * cos_a
            screen_x = center_x + (rx - rz) * 0.866
            screen_y = center_y + (rx + rz) * 0.5
            return screen_x, screen_y
        
        cells = []
        for row in range(board_size):
            for col in range(board_size):
                world_x = (col - 3.5) * cell_size
                world_z = (row - 3.5) * cell_size
                depth = world_x * sin_a + world_z * cos_a
                cells.append((row, col, world_x, world_z, depth))
        
        cells.sort(key=lambda c: c[4])
        
        board_corners = []
        for corner_col, corner_row in [(0, 0), (8, 0), (8, 8), (0, 8)]:
            wx = (corner_col - 4) * cell_size
            wz = (corner_row - 4) * cell_size
            board_corners.append(to_iso(wx, wz))
        
        shadow_corners = [(x + 10, y + 10) for x, y in board_corners]
        shadow_surf = pygame.Surface((m.Disp.width, m.Disp.height), pygame.SRCALPHA)
        pygame.draw.polygon(shadow_surf, (0, 0, 0, 60), shadow_corners)
        screen.blit(shadow_surf, (0, 0))
        
        pygame.draw.polygon(screen, colors['chessboard'], board_corners)
        
        for row, col, world_x, world_z, _ in cells:
            corners = []
            for dx, dz in [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]:
                wx = world_x + dx * cell_size
                wz = world_z + dz * cell_size
                corners.append(to_iso(wx, wz))
            
            color = colors['light_cell'] if (row + col) % 2 == 1 else colors['dark_cell']
            pygame.draw.polygon(screen, color, corners)
            pygame.draw.polygon(screen, (0, 0, 0, 60), corners, 1)
        
        pygame.draw.polygon(screen, colors['light_cell'], board_corners, 4)
    
    def iso_diamond(self, cx, cy, w, h, scale=1.0):
        """Создает ромб"""
        hw = (w * scale) / 2
        hh = (h * scale) / 2
        return [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
    
    def draw_main_menu(self, m):
        """Рисует главное меню мультиплеера"""
        colors = m.Disp.colors['Game']
        
        # Заголовок
        title = self.title_font.render("MULTIPLAYER", True, (255, 255, 255))
        title_rect = title.get_rect(center=(m.Disp.width//2, 150))
        m.Disp.screen.blit(title, title_rect)
        
        # Подзаголовок
        subtitle = self.text_font.render("Локальная сетевая игра", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(m.Disp.width//2, 190))
        m.Disp.screen.blit(subtitle, subtitle_rect)
        
        # Кнопки
        self.draw_buttons(m, m.Multiplayer.buttons, {
            "host_game": "СОЗДАТЬ ИГРУ",
            "join_game": "ПРИСОЕДИНИТЬСЯ",
            "profile": "ПРОФИЛЬ",
            "back": "НАЗАД"
        })
        
        # Информация о профиле
        if hasattr(m, 'PlayerProfile'):
            self.draw_player_info(m, m.Disp.width - 300, 50)
    
    def draw_profile_setup(self, m):
        """Рисует настройку профиля"""
        colors = m.Disp.colors['Game']
        
        # Заголовок
        title = self.subtitle_font.render("НАСТРОЙКА ПРОФИЛЯ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(m.Disp.width//2, 200))
        m.Disp.screen.blit(title, title_rect)
        
        # Поле ввода никнейма
        self.draw_text_inputs(m, {
            "nickname": "Введите ваш никнейм:"
        })
        
        # Кнопки
        self.draw_buttons(m, m.Multiplayer.buttons, {
            "load_avatar": "ЗАГРУЗИТЬ АВАТАР",
            "save": "СОХРАНИТЬ",
            "back": "НАЗАД"
        })
        
        # Показываем статус сообщения
        if m.Multiplayer.connection_status:
            status_text = self.text_font.render(m.Multiplayer.connection_status, True, (100, 255, 100))
            status_rect = status_text.get_rect(center=(m.Disp.width//2, 350))
            m.Disp.screen.blit(status_text, status_rect)
        
        # Показываем текущий аватар
        if hasattr(m, 'PlayerProfile'):
            avatar = m.PlayerProfile.get_avatar_surface()
            avatar_rect = pygame.Rect(m.Disp.width//2 - 32, 300, 64, 64)
            m.Disp.screen.blit(avatar, avatar_rect)
    
    def draw_hosting(self, m):
        """Рисует экран создания хоста"""
        colors = m.Disp.colors['Game']
        
        # Заголовок
        title = self.subtitle_font.render("СОЗДАНИЕ ИГРЫ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(m.Disp.width//2, 200))
        m.Disp.screen.blit(title, title_rect)
        
        # Информация
        info_lines = [
            "Другие игроки смогут подключиться",
            "к вашему компьютеру по IP адресу:",
            "",
            f"IP: {getattr(m.NetworkManager, 'get_local_ip', lambda: '127.0.0.1')() if hasattr(m, 'NetworkManager') else '127.0.0.1'}",
            f"Порт: 12345"
        ]
        
        y_offset = 250
        for line in info_lines:
            color = (255, 255, 100) if line.startswith("IP:") or line.startswith("Порт:") else (200, 200, 200)
            text = self.text_font.render(line, True, color)
            text_rect = text.get_rect(center=(m.Disp.width//2, y_offset))
            m.Disp.screen.blit(text, text_rect)
            y_offset += 25
        
        # Кнопки
        self.draw_buttons(m, m.Multiplayer.buttons, {
            "start_host": "ЗАПУСТИТЬ ХОСТ",
            "back": "НАЗАД"
        })
    
    def draw_connecting(self, m):
        """Рисует экран подключения"""
        colors = m.Disp.colors['Game']
        
        # Заголовок
        title = self.subtitle_font.render("ПОДКЛЮЧЕНИЕ К ИГРЕ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(m.Disp.width//2, 200))
        m.Disp.screen.blit(title, title_rect)
        
        # Поле ввода IP
        self.draw_text_inputs(m, {
            "host_ip": "IP адрес хоста:"
        })
        
        # Кнопки
        self.draw_buttons(m, m.Multiplayer.buttons, {
            "connect": "ПОДКЛЮЧИТЬСЯ",
            "back": "НАЗАД"
        })
    
    def draw_lobby(self, m):
        """Рисует лобби хоста"""
        colors = m.Disp.colors['Game']
        
        # Заголовок
        title = self.subtitle_font.render("ЛОББИ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(m.Disp.width//2, 80))
        m.Disp.screen.blit(title, title_rect)
        
        # Статус
        status = m.Multiplayer.connection_status
        if status:
            status_text = self.text_font.render(status, True, (100, 255, 100))
            status_rect = status_text.get_rect(center=(m.Disp.width//2, 120))
            m.Disp.screen.blit(status_text, status_rect)
        
        # Информация о подключенных игроках
        self.draw_player_list(m, m.Disp.width//2 - 200, 160)
        
        # Индикаторы голосового чата
        if hasattr(m, 'VoiceChat'):
            m.VoiceChat.draw_speaking_indicator(m.Disp.screen)
            m.VoiceChat.draw_mute_indicator(m.Disp.screen)
        
        # Кнопки
        button_labels = {"disconnect": "ОТКЛЮЧИТЬСЯ"}
        if m.Multiplayer.game_ready:
            button_labels["start_game"] = "НАЧАТЬ ИГРУ"
        
        self.draw_buttons(m, m.Multiplayer.buttons, button_labels)
    
    def draw_waiting(self, m):
        """Рисует экран ожидания для клиента (как лобби но без кнопки старта)"""
        colors = m.Disp.colors['Game']
        
        # Заголовок
        title = self.subtitle_font.render("ЛОББИ", True, (255, 255, 255))
        title_rect = title.get_rect(center=(m.Disp.width//2, 80))
        m.Disp.screen.blit(title, title_rect)
        
        # Статус (ожидание хоста)
        dots = "." * (int(self.pulse * 3) % 4)
        status = f"Ожидание начала игры{dots}"
        status_text = self.text_font.render(status, True, (255, 200, 100))
        status_rect = status_text.get_rect(center=(m.Disp.width//2, 120))
        m.Disp.screen.blit(status_text, status_rect)
        
        # Список игроков (показываем хоста и себя)
        self.draw_player_list(m, m.Disp.width//2 - 200, 160)
        
        # Индикаторы голосового чата
        if hasattr(m, 'VoiceChat'):
            m.VoiceChat.draw_speaking_indicator(m.Disp.screen)
            m.VoiceChat.draw_mute_indicator(m.Disp.screen)
        
        # Кнопка отключения (без кнопки старта игры)
        self.draw_buttons(m, m.Multiplayer.buttons, {
            "disconnect": "ОТКЛЮЧИТЬСЯ"
        })
    
    def draw_buttons(self, m, buttons, labels):
        """Рисует кнопки"""
        colors = m.Disp.colors['Game']
        logic = m.Multiplayer
        
        for name, rect in buttons.items():
            if name not in labels:
                continue
                
            is_hover = logic.hover == name
            
            # Проверяем доступность кнопки
            is_enabled = True
            if name == "start_game" and not logic.game_ready:
                is_enabled = False
            
            # Цвет кнопки
            if not is_enabled:
                base_color = (60, 60, 60)
                border_color = (100, 100, 100)
                text_color = (120, 120, 120)
            elif is_hover:
                base_color = colors['light_cell']
                border_color = colors['chessboard']
                text_color = (255, 255, 255)
            else:
                base_color = colors['dark_cell']
                border_color = colors['chessboard']
                text_color = (255, 255, 255)
            
            # Рисуем кнопку
            pygame.draw.rect(m.Disp.screen, base_color, rect, border_radius=8)
            pygame.draw.rect(m.Disp.screen, border_color, rect, 2, border_radius=8)
            
            # Текст кнопки
            label_text = self.text_font.render(labels[name], True, text_color)
            label_rect = label_text.get_rect(center=rect.center)
            m.Disp.screen.blit(label_text, label_rect)
    
    def draw_text_inputs(self, m, inputs):
        """Рисует поля ввода текста"""
        colors = m.Disp.colors['Game']
        logic = m.Multiplayer
        
        for name, rect in logic.text_inputs.items():
            if name not in inputs:
                continue
            
            is_active = logic.active_input == name
            is_hover = logic.hover == name
            
            # Цвет поля
            if is_active:
                bg_color = (60, 60, 80)
                border_color = (150, 150, 200)
            elif is_hover:
                bg_color = (50, 50, 50)
                border_color = (120, 120, 120)
            else:
                bg_color = (40, 40, 40)
                border_color = (100, 100, 100)
            
            # Рисуем поле
            pygame.draw.rect(m.Disp.screen, bg_color, rect, border_radius=5)
            pygame.draw.rect(m.Disp.screen, border_color, rect, 2, border_radius=5)
            
            # Label
            label_text = self.small_font.render(inputs[name], True, (200, 200, 200))
            label_rect = label_text.get_rect(centerx=rect.centerx, bottom=rect.top - 5)
            m.Disp.screen.blit(label_text, label_rect)
            
            # Текст в поле
            if name == "nickname":
                display_text = logic.temp_nickname
            elif name == "host_ip":
                display_text = logic.host_ip
            else:
                display_text = ""
            
            # Курсор
            if is_active:
                cursor_visible = int(time.time() * 2) % 2
                if cursor_visible:
                    display_text += "|"
            
            if display_text:
                text_surface = self.text_font.render(display_text, True, (255, 255, 255))
                text_rect = pygame.Rect(rect.x + 10, rect.y, rect.width - 20, rect.height)
                text_pos = text_surface.get_rect(centery=rect.centery, x=rect.x + 10)
                m.Disp.screen.blit(text_surface, text_pos)
    
    def draw_player_info(self, m, x, y):
        """Рисует информацию о текущем игроке"""
        if not hasattr(m, 'PlayerProfile'):
            return
        
        profile = m.PlayerProfile
        colors = m.Disp.colors['Game']
        
        # Фон панели
        panel_w, panel_h = 250, 120
        panel_rect = pygame.Rect(x, y, panel_w, panel_h)
        pygame.draw.rect(m.Disp.screen, (0, 0, 0, 100), panel_rect, border_radius=10)
        pygame.draw.rect(m.Disp.screen, colors['border'] if 'border' in colors else (100, 100, 100), panel_rect, 2, border_radius=10)
        
        # Аватар
        avatar = profile.get_avatar_surface()
        avatar_rect = pygame.Rect(x + 10, y + 10, 64, 64)
        m.Disp.screen.blit(avatar, avatar_rect)
        
        # Никнейм
        nickname_text = self.text_font.render(profile.nickname, True, (255, 255, 255))
        nickname_rect = nickname_text.get_rect(x=x + 85, y=y + 15)
        m.Disp.screen.blit(nickname_text, nickname_rect)
        
        # Статистика
        stats_lines = [
            f"Игр: {profile.stats['games_played']}",
            f"Побед: {profile.stats['games_won']}",
            f"Винрейт: {profile.get_win_rate():.1f}%"
        ]
        
        y_offset = y + 45
        for line in stats_lines:
            stats_text = self.small_font.render(line, True, (200, 200, 200))
            m.Disp.screen.blit(stats_text, (x + 85, y_offset))
            y_offset += 15
    
    def draw_player_list(self, m, x, y):
        """Рисует список подключенных игроков"""
        colors = m.Disp.colors['Game']
        
        # Заголовок
        title_text = self.text_font.render("ИГРОКИ:", True, (255, 255, 255))
        m.Disp.screen.blit(title_text, (x, y))
        
        y_offset = y + 35
        
        # Текущий игрок (хост или клиент)
        if hasattr(m, 'PlayerProfile'):
            # Аватар текущего игрока
            avatar = m.PlayerProfile.get_avatar_surface()
            if avatar:
                avatar_rect = pygame.Rect(x, y_offset, 32, 32)
                scaled_avatar = pygame.transform.scale(avatar, (32, 32))
                m.Disp.screen.blit(scaled_avatar, avatar_rect)
            
            # Текст с ролью
            role = "(Хост)" if m.Multiplayer.is_host else "(Вы)"
            player_text = self.text_font.render(f"👑 {m.PlayerProfile.nickname} {role}", True, (255, 255, 100))
            m.Disp.screen.blit(player_text, (x + 40, y_offset + 5))
            y_offset += 45
        
        # Подключенный игрок
        if m.Multiplayer.connected_player:
            if isinstance(m.Multiplayer.connected_player, dict):
                nickname = m.Multiplayer.connected_player.get('nickname', 'Unknown')
                avatar_hash = m.Multiplayer.connected_player.get('avatar_hash', '')
                avatar_data = m.Multiplayer.connected_player.get('avatar_data', None)
                
                # Получаем аватар из кеша
                from function.PlayerProfile import PlayerAvatarCache
                player_avatar = PlayerAvatarCache.get_avatar(nickname, avatar_hash, avatar_data)
                
                if player_avatar:
                    avatar_rect = pygame.Rect(x, y_offset, 32, 32)
                    scaled_avatar = pygame.transform.scale(player_avatar, (32, 32))
                    m.Disp.screen.blit(scaled_avatar, avatar_rect)
                
                player_text = self.text_font.render(f"🎮 {nickname}", True, (100, 255, 100))
                m.Disp.screen.blit(player_text, (x + 40, y_offset + 5))
            else:
                player_text = self.text_font.render(f"🎮 Игрок ({m.Multiplayer.connected_player[0]})", True, (100, 255, 100))
                m.Disp.screen.blit(player_text, (x, y_offset))
        else:
            waiting_text = self.text_font.render("⏳ Ожидание игроков...", True, (150, 150, 150))
            m.Disp.screen.blit(waiting_text, (x, y_offset))
    
    def draw_error_message(self, m):
        """Рисует сообщения об ошибках"""
        if not m.Multiplayer.connection_error:
            return
        
        error_text = self.text_font.render(m.Multiplayer.connection_error, True, (255, 100, 100))
        error_rect = error_text.get_rect(center=(m.Disp.width//2, 100))
        
        # Фон для ошибки
        bg_rect = error_rect.inflate(20, 10)
        pygame.draw.rect(m.Disp.screen, (80, 20, 20), bg_rect, border_radius=5)
        pygame.draw.rect(m.Disp.screen, (255, 100, 100), bg_rect, 2, border_radius=5)
        
        m.Disp.screen.blit(error_text, error_rect)
