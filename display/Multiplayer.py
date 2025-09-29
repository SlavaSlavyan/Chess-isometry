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
        
        # Кеш для фоновой поверхности
        self.background_surface = None
        self.background_cached = False
    
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
        """Рисует фон как в главном меню"""
        screen = m.Disp.screen
        colors = m.Disp.colors['Game']
        screen.fill(colors['bg'])
        
        # Используем тот же фон что и в меню
        if not self.background_cached:
            self.background_surface = pygame.Surface((m.Disp.width, m.Disp.height), pygame.SRCALPHA)
            
            # Сохраняем оригинальные настройки
            original_rotate = m.Disp.Game.rotate[:]
            original_zoom = m.config['zoom']
            
            # Используем настройки как в игре
            m.Disp.Game.rotate = [0, -90]
            m.config['zoom'] = original_zoom
            
            # Создаем временные позиции клеток
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
            
            pygame.draw.polygon(self.background_surface, colors['bg'], board)
            pygame.draw.polygon(self.background_surface, colors['chessboard'], back)
            
            # Рисуем клетки
            for y in range(8):
                for x in range(8):
                    if (x+y)%2 == 1:
                        light_color = (*colors['light_cell'], 120)
                        pygame.draw.polygon(self.background_surface, light_color, temp_cells[y][x])
            
            # Восстанавливаем настройки
            m.Disp.Game.rotate = original_rotate
            m.config['zoom'] = original_zoom
            
            self.background_cached = True
        
        # Отображаем фон
        screen.blit(self.background_surface, (0, 0))
    
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
        
        # Чат
        if hasattr(m, 'ChatSystem'):
            m.ChatSystem.draw(m.Disp.screen, 50, m.Disp.height - 280)
        
        # Кнопки
        button_labels = {"disconnect": "ОТКЛЮЧИТЬСЯ"}
        if m.Multiplayer.game_ready:
            button_labels["start_game"] = "НАЧАТЬ ИГРУ"
        
        self.draw_buttons(m, m.Multiplayer.buttons, button_labels)
    
    def draw_waiting(self, m):
        """Рисует экран ожидания для клиента"""
        colors = m.Disp.colors['Game']
        
        # Заголовок
        title = self.subtitle_font.render("ОЖИДАНИЕ ХОСТА", True, (255, 255, 255))
        title_rect = title.get_rect(center=(m.Disp.width//2, 150))
        m.Disp.screen.blit(title, title_rect)
        
        # Анимированный индикатор загрузки
        dots = "." * (int(self.pulse * 3) % 4)
        loading_text = self.text_font.render(f"Ожидание начала игры{dots}", True, (200, 200, 200))
        loading_rect = loading_text.get_rect(center=(m.Disp.width//2, 200))
        m.Disp.screen.blit(loading_text, loading_rect)
        
        # Чат
        if hasattr(m, 'ChatSystem'):
            m.ChatSystem.draw(m.Disp.screen, 50, m.Disp.height - 280)
        
        # Кнопка отключения
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
        
        # Хост (текущий игрок)
        if hasattr(m, 'PlayerProfile'):
            # Аватар хоста
            avatar = m.PlayerProfile.get_avatar_surface()
            avatar_rect = pygame.Rect(x, y_offset, 32, 32)
            scaled_avatar = pygame.transform.scale(avatar, (32, 32))
            m.Disp.screen.blit(scaled_avatar, avatar_rect)
            
            # Текст хоста
            host_text = self.text_font.render(f"👑 {m.PlayerProfile.nickname} (Хост)", True, (255, 255, 100))
            m.Disp.screen.blit(host_text, (x + 40, y_offset + 5))
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
