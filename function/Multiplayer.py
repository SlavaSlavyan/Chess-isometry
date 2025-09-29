import pygame
import threading
import time
import sys
import os
from typing import Optional

class Multiplayer:
    """Логика мультиплеера"""
    
    def __init__(self, m):
        self.m = m
        
        # Состояние мультиплеера
        self.state = "menu"  # "menu", "hosting", "connecting", "profile", "lobby", "waiting"
        self.previous_state = "menu"
        
        # Элементы интерфейса
        self.buttons = {}
        self.text_inputs = {}
        self.hover = None
        self.active_input = None
        
        # Данные подключения
        self.host_ip = ""
        self.host_port = 12345
        self.connection_status = ""
        self.connection_error = ""
        
        # Профиль игрока
        self.nickname_input = ""
        self.temp_nickname = ""
        
        # Состояние игры
        self.is_host = False
        self.connected_player = None
        self.game_ready = False
        
        # Таймеры
        self.connection_timeout = 0
        self.status_message_timer = 0
        
        # Редактор аватаров
        self.avatar_editor = None
        
    def get_resource_path(self, relative_path):
        """Получить абсолютный путь к ресурсу"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            return relative_path
    
    def main(self, m):
        """Основной цикл логики мультиплеера"""
        # Если активен редактор аватаров, обрабатываем только его
        if self.avatar_editor and self.avatar_editor.active:
            return
            
        self.layout(m)
        self.handle_input(m)
        self.update_connection_status(m)
    
    def layout(self, m):
        """Создает layout для текущего состояния"""
        width, height = m.Disp.width, m.Disp.height
        
        if self.state == "menu":
            self.layout_main_menu(width, height)
        elif self.state == "profile":
            self.layout_profile_setup(width, height)
        elif self.state == "hosting":
            self.layout_hosting(width, height)
        elif self.state == "connecting":
            self.layout_connecting(width, height)
        elif self.state == "lobby":
            self.layout_lobby(width, height)
        elif self.state == "waiting":
            self.layout_waiting(width, height)
    
    def layout_main_menu(self, width, height):
        """Layout главного меню мультиплеера"""
        btn_w, btn_h = int(width * 0.25), 50
        cx = width // 2 - btn_w // 2
        start_y = height // 2 - 150
        
        self.buttons = {
            "host_game": pygame.Rect(cx, start_y, btn_w, btn_h),
            "join_game": pygame.Rect(cx, start_y + 70, btn_w, btn_h),
            "profile": pygame.Rect(cx, start_y + 140, btn_w, btn_h),
            "back": pygame.Rect(cx, start_y + 210, btn_w, btn_h)
        }
        
        self.text_inputs = {}
    
    def layout_profile_setup(self, width, height):
        """Layout настройки профиля"""
        btn_w, btn_h = int(width * 0.3), 45
        input_w, input_h = int(width * 0.4), 40
        cx = width // 2 - btn_w // 2
        input_cx = width // 2 - input_w // 2
        start_y = height // 2 - 100
        
        self.text_inputs = {
            "nickname": pygame.Rect(input_cx, start_y, input_w, input_h)
        }
        
        self.buttons = {
            "load_avatar": pygame.Rect(cx, start_y + 60, btn_w, btn_h),
            "save": pygame.Rect(cx, start_y + 120, btn_w, btn_h),
            "back": pygame.Rect(cx, start_y + 180, btn_w, btn_h)
        }
    
    def layout_hosting(self, width, height):
        """Layout создания хоста"""
        btn_w, btn_h = int(width * 0.25), 45
        cx = width // 2 - btn_w // 2
        start_y = height // 2 - 50
        
        self.buttons = {
            "start_host": pygame.Rect(cx, start_y, btn_w, btn_h),
            "back": pygame.Rect(cx, start_y + 70, btn_w, btn_h)
        }
        
        self.text_inputs = {}
    
    def layout_connecting(self, width, height):
        """Layout подключения к хосту"""
        btn_w, btn_h = int(width * 0.25), 45
        input_w, input_h = int(width * 0.4), 40
        cx = width // 2 - btn_w // 2
        input_cx = width // 2 - input_w // 2
        start_y = height // 2 - 80
        
        self.text_inputs = {
            "host_ip": pygame.Rect(input_cx, start_y, input_w, input_h)
        }
        
        self.buttons = {
            "connect": pygame.Rect(cx, start_y + 70, btn_w, btn_h),
            "back": pygame.Rect(cx, start_y + 130, btn_w, btn_h)
        }
    
    def layout_lobby(self, width, height):
        """Layout лобби (ожидание игроков)"""
        btn_w, btn_h = int(width * 0.22), 45
        cx = width // 2 - btn_w // 2
        start_y = height - 120
        
        self.buttons = {
            "start_game": pygame.Rect(cx - 120, start_y, btn_w, btn_h),
            "disconnect": pygame.Rect(cx + 120, start_y, btn_w, btn_h)
        }
        
        self.text_inputs = {}
    
    def layout_waiting(self, width, height):
        """Layout ожидания (для клиента)"""
        btn_w, btn_h = int(width * 0.22), 45
        cx = width // 2 - btn_w // 2
        start_y = height - 80
        
        self.buttons = {
            "disconnect": pygame.Rect(cx, start_y, btn_w, btn_h)
        }
        
        self.text_inputs = {}
    
    def handle_input(self, m):
        """Обрабатывает пользовательский ввод"""
        mouse_pos = m.PI.MI.mouse_pos
        self.hover = None
        
        # Проверяем наведение на кнопки
        for name, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                self.hover = name
        
        # Проверяем наведение на поля ввода
        for name, rect in self.text_inputs.items():
            if rect.collidepoint(mouse_pos):
                self.hover = name
        
        # Обрабатываем клики
        if m.PI.MI.mouse_click['lt']:
            self.handle_click(m)
    
    def handle_click(self, m):
        """Обрабатывает клики мыши"""
        if self.state == "menu":
            if self.hover == "host_game":
                if hasattr(m, 'PlayerProfile') and m.PlayerProfile.nickname:
                    self.state = "hosting"
                else:
                    self.state = "profile"
                    self.temp_nickname = getattr(m.PlayerProfile, 'nickname', 'Player') if hasattr(m, 'PlayerProfile') else 'Player'
            elif self.hover == "join_game":
                if hasattr(m, 'PlayerProfile') and m.PlayerProfile.nickname:
                    self.state = "connecting"
                    self.host_ip = ""
                else:
                    self.state = "profile"
                    self.temp_nickname = getattr(m.PlayerProfile, 'nickname', 'Player') if hasattr(m, 'PlayerProfile') else 'Player'
            elif self.hover == "profile":
                self.state = "profile"
                self.temp_nickname = getattr(m.PlayerProfile, 'nickname', 'Player') if hasattr(m, 'PlayerProfile') else 'Player'
            elif self.hover == "back":
                m.set_scene('menu')
        
        elif self.state == "profile":
            if self.hover == "load_avatar":
                self.load_avatar_file(m)
            elif self.hover == "save":
                if len(self.temp_nickname.strip()) > 0:
                    if not hasattr(m, 'PlayerProfile'):
                        from function.PlayerProfile import PlayerProfile
                        m.PlayerProfile = PlayerProfile()
                    m.PlayerProfile.set_nickname(self.temp_nickname.strip())
                    self.state = "menu"
            elif self.hover == "back":
                self.state = "menu"
            elif self.hover == "nickname":
                self.active_input = "nickname"
        
        elif self.state == "hosting":
            if self.hover == "start_host":
                self.start_hosting(m)
            elif self.hover == "back":
                self.state = "menu"
        
        elif self.state == "connecting":
            if self.hover == "connect":
                self.start_connecting(m)
            elif self.hover == "back":
                self.state = "menu"
            elif self.hover == "host_ip":
                self.active_input = "host_ip"
        
        elif self.state == "lobby":
            if self.hover == "start_game" and self.is_host and self.game_ready:
                self.start_multiplayer_game(m)
            elif self.hover == "disconnect":
                self.disconnect(m)
        
        elif self.state == "waiting":
            if self.hover == "disconnect":
                self.disconnect(m)
    
    def handle_text_input(self, m, events=None):
        """Обрабатывает ввод текста"""
        if self.active_input is None:
            return
        
        # Если события не переданы, пропускаем
        if events is None:
            return
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active_input = None
                elif event.key == pygame.K_ESCAPE:
                    self.active_input = None
                elif event.key == pygame.K_BACKSPACE:
                    if self.active_input == "nickname":
                        self.temp_nickname = self.temp_nickname[:-1]
                    elif self.active_input == "host_ip":
                        self.host_ip = self.host_ip[:-1]
                else:
                    if event.unicode.isprintable():
                        if self.active_input == "nickname" and len(self.temp_nickname) < 20:
                            self.temp_nickname += event.unicode
                        elif self.active_input == "host_ip" and len(self.host_ip) < 15:
                            self.host_ip += event.unicode
    
    def start_hosting(self, m):
        """Запускает хост-сервер"""
        if not hasattr(m, 'NetworkManager'):
            from function.NetworkManager import NetworkManager
            m.NetworkManager = NetworkManager()
        
        # Настраиваем callbacks
        m.NetworkManager.on_client_connected = lambda addr: self.on_client_connected(m, addr)
        m.NetworkManager.on_client_disconnected = lambda: self.on_client_disconnected(m)
        m.NetworkManager.on_message_received = lambda msg: self.on_message_received(m, msg)
        
        # Запускаем хост
        if m.NetworkManager.start_host():
            self.is_host = True
            self.state = "lobby"
            self.connection_status = f"Ожидание игроков... IP: {m.NetworkManager.get_local_ip()}"
            
            # Инициализируем чат
            if not hasattr(m, 'ChatSystem'):
                from function.ChatSystem import ChatSystem
                m.ChatSystem = ChatSystem()
                m.ChatSystem.on_message_send = lambda text: self.send_chat_message(m, text)
            
            m.ChatSystem.add_system_message("Хост создан! Ожидание игроков...")
        else:
            self.connection_error = "Ошибка создания хоста"
            self.status_message_timer = time.time()
    
    def start_connecting(self, m):
        """Подключается к хосту"""
        if not self.host_ip.strip():
            self.connection_error = "Введите IP адрес хоста"
            self.status_message_timer = time.time()
            return
        
        if not hasattr(m, 'NetworkManager'):
            from function.NetworkManager import NetworkManager
            m.NetworkManager = NetworkManager()
        
        # Настраиваем callbacks
        m.NetworkManager.on_message_received = lambda msg: self.on_message_received(m, msg)
        m.NetworkManager.on_connection_lost = lambda: self.on_connection_lost(m)
        
        # Подключаемся
        if m.NetworkManager.connect_to_host(self.host_ip.strip()):
            self.is_host = False
            self.state = "waiting"
            self.connection_status = f"Подключение к {self.host_ip}..."
            
            # Инициализируем чат
            if not hasattr(m, 'ChatSystem'):
                from function.ChatSystem import ChatSystem
                m.ChatSystem = ChatSystem()
                m.ChatSystem.on_message_send = lambda text: self.send_chat_message(m, text)
            
            # Отправляем данные профиля
            if hasattr(m, 'PlayerProfile'):
                m.NetworkManager.send_message('player_profile', m.PlayerProfile.get_profile_data())
        else:
            self.connection_error = "Не удалось подключиться к хосту"
            self.status_message_timer = time.time()
    
    def on_client_connected(self, m, address):
        """Обработчик подключения клиента"""
        self.connected_player = address
        self.connection_status = f"Игрок подключился: {address[0]}"
        
        if hasattr(m, 'ChatSystem'):
            m.ChatSystem.add_system_message(f"Игрок подключился: {address[0]}")
    
    def on_client_disconnected(self, m):
        """Обработчик отключения клиента"""
        self.connected_player = None
        self.game_ready = False
        self.connection_status = "Игрок отключился"
        
        if hasattr(m, 'ChatSystem'):
            m.ChatSystem.add_system_message("Игрок отключился")
    
    def on_connection_lost(self, m):
        """Обработчик потери соединения"""
        self.state = "menu"
        self.connection_error = "Соединение потеряно"
        self.status_message_timer = time.time()
        
        if hasattr(m, 'ChatSystem'):
            m.ChatSystem.add_error_message("Соединение потеряно")
    
    def on_message_received(self, m, message):
        """Обработчик получения сообщений"""
        msg_type = message.get('type')
        data = message.get('data', {})
        
        if msg_type == 'player_profile':
            self.connected_player = data
            self.game_ready = True
            
            # Кешируем аватар игрока
            if data.get('avatar_data') and data.get('avatar_hash'):
                from function.PlayerProfile import PlayerAvatarCache
                PlayerAvatarCache.get_avatar(
                    data.get('nickname', 'Unknown'),
                    data.get('avatar_hash'),
                    data.get('avatar_data')
                )
            
            if hasattr(m, 'ChatSystem'):
                nickname = data.get('nickname', 'Unknown')
                m.ChatSystem.add_info_message(f"Игрок {nickname} готов к игре!")
        
        elif msg_type == 'chat_message':
            if hasattr(m, 'ChatSystem'):
                sender = data.get('sender', 'Unknown')
                text = data.get('text', '')
                m.ChatSystem.add_message(sender, text)
        
        elif msg_type == 'game_start':
            # Запускаем игру
            self.start_multiplayer_game(m)
    
    def send_chat_message(self, m, text):
        """Отправляет сообщение в чат"""
        if hasattr(m, 'NetworkManager') and m.NetworkManager.is_connected:
            sender = getattr(m.PlayerProfile, 'nickname', 'Player') if hasattr(m, 'PlayerProfile') else 'Player'
            m.NetworkManager.send_message('chat_message', {
                'sender': sender,
                'text': text
            })
            
            # Добавляем сообщение в локальный чат
            if hasattr(m, 'ChatSystem'):
                m.ChatSystem.add_message(sender, text)
    
    def start_multiplayer_game(self, m):
        """Запускает мультиплеер игру"""
        if self.is_host:
            # Хост отправляет сигнал начала игры
            if hasattr(m, 'NetworkManager'):
                m.NetworkManager.send_message('game_start')
        
        # Настраиваем игру для мультиплеера
        m.PI.Game.restart_game(m)
        m.PI.Game.setup_multiplayer(m, self.is_host)
        
        # Добавляем сообщение в чат
        if hasattr(m, 'ChatSystem'):
            m.ChatSystem.add_system_message("🎮 Игра началась!")
            opponent_team = "черных" if self.is_host else "белых"
            my_team = "белыми" if self.is_host else "черными"
            m.ChatSystem.add_info_message(f"Вы играете {my_team}, противник - {opponent_team}")
        
        # Переходим в игру
        m.set_scene('game')
    
    def disconnect(self, m):
        """Отключается от сети"""
        if hasattr(m, 'NetworkManager'):
            m.NetworkManager.disconnect()
        
        self.state = "menu"
        self.is_host = False
        self.connected_player = None
        self.game_ready = False
        self.connection_status = ""
    
    def update_connection_status(self, m):
        """Обновляет статус соединения"""
        # Очищаем сообщения об ошибках через 3 секунды
        if self.status_message_timer > 0 and time.time() - self.status_message_timer > 3:
            self.connection_error = ""
            self.status_message_timer = 0
        
        # Обрабатываем сообщения из сети
        if hasattr(m, 'NetworkManager'):
            messages = m.NetworkManager.get_messages()
            for message in messages:
                self.on_message_received(m, message)
        
        # Обновляем чат
        if hasattr(m, 'ChatSystem'):
            m.ChatSystem.update(1/60.0)  # Примерно 60 FPS
    
    def load_avatar_file(self, m):
        """Загружает файл аватара через диалог"""
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            # Создаем скрытое окно tkinter
            root = tk.Tk()
            root.withdraw()
            
            # Открываем диалог выбора файла
            file_path = filedialog.askopenfilename(
                title="Выберите изображение для аватара",
                filetypes=[
                    ("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif"),
                    ("PNG файлы", "*.png"),
                    ("JPEG файлы", "*.jpg *.jpeg"),
                    ("Все файлы", "*.*")
                ]
            )
            
            root.destroy()
            
            if file_path:
                # Запускаем редактор аватаров
                if not self.avatar_editor:
                    from function.AvatarEditor import AvatarEditor
                    self.avatar_editor = AvatarEditor()
                
                if self.avatar_editor.start_editing(file_path):
                    print("🎨 Редактор аватара запущен")
                else:
                    self.connection_error = "Ошибка загрузки изображения"
                    self.status_message_timer = time.time()
            
        except ImportError:
            self.connection_error = "Tkinter не доступен для выбора файлов"
            self.status_message_timer = time.time()
        except Exception as e:
            self.connection_error = f"Ошибка: {str(e)}"
            self.status_message_timer = time.time()
    
    def handle_avatar_editor(self, m, events, mouse_pos):
        """Обрабатывает редактор аватаров"""
        if not self.avatar_editor or not self.avatar_editor.active:
            return
        
        result = self.avatar_editor.handle_input(events, mouse_pos, (m.Disp.width, m.Disp.height))
        
        if result == "confirm":
            # Сохраняем отредактированный аватар
            cropped_image = self.avatar_editor.get_cropped_image()
            if cropped_image:
                if not hasattr(m, 'PlayerProfile'):
                    from function.PlayerProfile import PlayerProfile
                    m.PlayerProfile = PlayerProfile()
                
                # Создаем временный файл и сохраняем туда изображение
                import tempfile
                import hashlib
                
                try:
                    # Сохраняем в временный файл
                    temp_path = os.path.join(tempfile.gettempdir(), "avatar_temp.png")
                    pygame.image.save(cropped_image, temp_path)
                    
                    # Загружаем как пользовательский аватар
                    if m.PlayerProfile.load_custom_avatar(temp_path):
                        # Но используем уже обработанное изображение
                        m.PlayerProfile.avatar_surface = cropped_image
                        # Создаем хэш для аватара
                        m.PlayerProfile.avatar_hash = hashlib.md5(pygame.image.tostring(cropped_image, 'RGBA')).hexdigest()
                        # Сохраняем файл аватара под НОВЫМ хэшем и обновляем профиль
                        if hasattr(m.PlayerProfile, '_save_avatar_to_disk'):
                            m.PlayerProfile._save_avatar_to_disk()
                        m.PlayerProfile.save_profile()
                        
                        self.connection_status = "Аватар сохранен!"
                        self.status_message_timer = time.time()
                    else:
                        self.connection_error = "Ошибка сохранения аватара"
                        self.status_message_timer = time.time()
                    
                    # Удаляем временный файл
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                        
                except Exception as e:
                    self.connection_error = f"Ошибка обработки: {str(e)}"
                    self.status_message_timer = time.time()
            
            self.avatar_editor.close()
            
        elif result == "cancel":
            self.avatar_editor.close()
