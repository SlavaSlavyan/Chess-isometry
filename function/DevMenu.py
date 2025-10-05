"""
Developer Menu - Меню разработчика в стиле чит-меню
Активация: INSERT или F12
"""

import pygame
import time

class DevMenu:
    def __init__(self):
        self.active = False
        self.alpha = 0
        self.target_alpha = 0
        self.animation_speed = 15
        
        # Категории
        self.categories = ['Game', 'Cards', 'Visual', 'System', 'Menu', 'Misc']
        self.current_category = 0
        
        # Опции для каждой категории
        self.options = {
            'Game': [
                {'type': 'button', 'name': 'Force Win (White)', 'action': 'win_white'},
                {'type': 'button', 'name': 'Force Win (Black)', 'action': 'win_black'},
                {'type': 'button', 'name': 'Switch Player', 'action': 'switch_player'},
                {'type': 'button', 'name': 'Reset Board', 'action': 'reset_board'},
                {'type': 'checkbox', 'name': 'God Mode (King Immortal)', 'var': 'god_mode', 'value': False},
                {'type': 'checkbox', 'name': 'No Turns (Move Anytime)', 'var': 'no_turns', 'value': False},
                {'type': 'checkbox', 'name': 'Fly Mode (Ignore Rules)', 'var': 'fly_mode', 'value': False},
            ],
            'Cards': [
                {'type': 'button', 'name': 'Open Card Gallery', 'action': 'open_card_gallery'},
                {'type': 'button', 'name': 'Give Random Card (White)', 'action': 'give_card_white'},
                {'type': 'button', 'name': 'Give Random Card (Black)', 'action': 'give_card_black'},
                {'type': 'button', 'name': 'Give All Cards (Both)', 'action': 'give_all_cards'},
                {'type': 'button', 'name': 'Clear Cards (White)', 'action': 'clear_cards_white'},
                {'type': 'button', 'name': 'Clear Cards (Black)', 'action': 'clear_cards_black'},
                {'type': 'slider', 'name': 'Card Drop Chance', 'var': 'card_drop_chance', 'min': 0, 'max': 1, 'value': 0.3},
                {'type': 'slider', 'name': 'Max Cards Per Player', 'var': 'max_cards', 'min': 1, 'max': 20, 'value': 5},
                {'type': 'checkbox', 'name': 'Unlimited Card Uses', 'var': 'unlimited_cards', 'value': False},
            ],
            'Visual': [
                {'type': 'slider', 'name': 'Animation Speed', 'var': 'anim_speed', 'min': 0.1, 'max': 5.0, 'value': 1.0},
                {'type': 'slider', 'name': 'Zoom Override', 'var': 'zoom_override', 'min': 0.5, 'max': 5.0, 'value': 1.0},
                {'type': 'checkbox', 'name': 'Show Grid', 'var': 'show_grid', 'value': False},
                {'type': 'checkbox', 'name': 'Show Coordinates', 'var': 'show_coords', 'value': False},
                {'type': 'checkbox', 'name': 'Rainbow Mode', 'var': 'rainbow_mode', 'value': False},
                {'type': 'checkbox', 'name': 'Particle Effects x10', 'var': 'particle_boost', 'value': False},
                {'type': 'button', 'name': 'Screen Shake Test', 'action': 'shake_test'},
            ],
            'System': [
                {'type': 'checkbox', 'name': 'FPS Counter', 'var': 'fps_counter', 'value': False},
                {'type': 'checkbox', 'name': 'Performance Monitor', 'var': 'perf_monitor', 'value': False},
                {'type': 'slider', 'name': 'Target FPS', 'var': 'target_fps', 'min': 30, 'max': 240, 'value': 60},
                {'type': 'dropdown', 'name': 'Engine', 'var': 'engine', 'items': ['pygame', 'panda3d'], 'value': 'pygame'},
                {'type': 'button', 'name': 'Apply Engine (restart)', 'action': 'apply_engine'},
                {'type': 'button', 'name': 'Reload Cards Module', 'action': 'reload_cards'},
                {'type': 'button', 'name': 'Force GC Collect', 'action': 'force_gc'},
                {'type': 'button', 'name': 'Print Game State', 'action': 'print_state'},
            ],
            'Menu': [
                {'type': 'slider', 'name': 'Menu Width', 'var': 'menu_width', 'min': 400, 'max': 1000, 'value': 600},
                {'type': 'slider', 'name': 'Menu Height', 'var': 'menu_height', 'min': 300, 'max': 800, 'value': 500},
                {'type': 'slider', 'name': 'Menu Alpha', 'var': 'menu_alpha', 'min': 100, 'max': 255, 'value': 220},
                {'type': 'slider', 'name': 'Animation Speed', 'var': 'menu_anim_speed', 'min': 5, 'max': 30, 'value': 15},
                {'type': 'checkbox', 'name': 'Show FPS in Menu', 'var': 'menu_show_fps', 'value': False},
                {'type': 'checkbox', 'name': 'Click Through Mode', 'var': 'click_through', 'value': False},
                {'type': 'checkbox', 'name': 'Discord RPC', 'var': 'discord_rpc', 'value': False},
                {'type': 'button', 'name': 'Reconnect Discord', 'action': 'reconnect_discord'},
                {'type': 'button', 'name': 'Reset Menu Settings', 'action': 'reset_menu'},
            ],
            'Misc': [
                {'type': 'button', 'name': 'Spawn Pawn (Random)', 'action': 'spawn_pawn'},
                {'type': 'button', 'name': 'Clear Empty Cells', 'action': 'clear_empty'},
                {'type': 'button', 'name': 'Randomize Board', 'action': 'randomize_board'},
                {'type': 'checkbox', 'name': 'Auto-Win After 10 Moves', 'var': 'auto_win', 'value': False},
                {'type': 'checkbox', 'name': 'Log All Actions', 'var': 'verbose_log', 'value': False},
                {'type': 'slider', 'name': 'Time Scale', 'var': 'time_scale', 'min': 0.1, 'max': 3.0, 'value': 1.0},
            ]
        }
        
        # Состояния опций
        self.option_states = {}
        self._init_option_states()
        
        # UI параметры
        self.menu_width = 600
        self.menu_height = 500
        self.scroll_offset = 0
        self.hover_option = None
        self.dragging_slider = None  # {'category': str, 'option_idx': int}
        
        # Card Gallery
        self.card_gallery_open = False
        self.gallery_scroll = 0
        self.hovered_gallery_card = None
        
        # Анимации
        self.pulse = 0
        self.glow_pulse = 0
        
        # Статистика
        self.start_time = time.time()
        self.frame_times = []
    
    def _init_option_states(self):
        """Инициализация состояний опций"""
        for category in self.options.values():
            for option in category:
                if 'var' in option:
                    self.option_states[option['var']] = option['value']
    
    def toggle(self):
        """Переключение меню"""
        self.active = not self.active
        self.target_alpha = 255 if self.active else 0
        try:
            print(f"🔧 [DEV MENU] {'Activated' if self.active else 'Deactivated'}")
        except:
            print(f"[CFG] [DEV MENU] {'Activated' if self.active else 'Deactivated'}")
    
    def update(self, m, dt):
        """Обновление меню"""
        # Анимация появления/исчезновения
        if self.alpha < self.target_alpha:
            self.alpha = min(self.alpha + self.animation_speed, self.target_alpha)
        elif self.alpha > self.target_alpha:
            self.alpha = max(self.alpha - self.animation_speed, self.target_alpha)
        
        self.pulse += 0.05
        self.glow_pulse += 0.1
        
        # Обновляем FPS счетчик
        if self.option_states.get('fps_counter'):
            self.frame_times.append(dt)
            if len(self.frame_times) > 60:
                self.frame_times.pop(0)
    
    def handle_input(self, m, event):
        """Обработка ввода"""
        if not self.active:
            return
        
        # Если открыта галерея карт, обрабатываем её отдельно
        if self.card_gallery_open:
            self._handle_gallery_input(m, event)
            return
        
        if event.type == pygame.KEYDOWN:
            # Переключение категорий стрелками (оставляем для удобства)
            if event.key == pygame.K_LEFT:
                self.current_category = (self.current_category - 1) % len(self.categories)
            elif event.key == pygame.K_RIGHT:
                self.current_category = (self.current_category + 1) % len(self.categories)
            elif event.key == pygame.K_ESCAPE:
                self.toggle()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ
                self._handle_click(m, pygame.mouse.get_pos())
            elif event.button == 4:  # Колесико вверх
                self.scroll_offset = max(0, self.scroll_offset - 30)
            elif event.button == 5:  # Колесико вниз
                self.scroll_offset += 30
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Отпустили ЛКМ
                self.dragging_slider = None
        
        elif event.type == pygame.MOUSEMOTION:
            # Обработка перетаскивания слайдера
            if self.dragging_slider:
                self._handle_slider_drag(m, pygame.mouse.get_pos())
    
    def _handle_click(self, m, mouse_pos):
        """Обработка кликов"""
        menu_x = (m.Disp.width - self.menu_width) // 2
        menu_y = (m.Disp.height - self.menu_height) // 2
        tab_y = menu_y + 80
        
        # Проверка клика по табам
        tab_width = self.menu_width // len(self.categories)
        for i in range(len(self.categories)):
            tab_x = menu_x + i * tab_width
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, 35)
            if tab_rect.collidepoint(mouse_pos):
                self.current_category = i
                return
        
        # Проверка клика по опциям
        if self.hover_option is not None:
            category = self.categories[self.current_category]
            option = self.options[category][self.hover_option]
            
            if option['type'] == 'button':
                self._execute_action(m, option['action'])
            elif option['type'] == 'checkbox':
                self.option_states[option['var']] = not self.option_states[option['var']]
                try:
                    print(f"🔧 {option['name']}: {self.option_states[option['var']]}")
                except:
                    print(f"[CFG] {option['name']}: {self.option_states[option['var']]}")
                self._apply_option(m, option)
            elif option['type'] == 'slider':
                # Начинаем перетаскивание слайдера
                self.dragging_slider = {
                    'category': category,
                    'option_idx': self.hover_option,
                    'option': option
                }
                self._handle_slider_drag(m, mouse_pos)
    
    def _execute_action(self, m, action):
        """Выполнение действия"""
        try:
            print(f"🔧 [DEV MENU] Action: {action}")
        except:
            print(f"[CFG] [DEV MENU] Action: {action}")
        
        if action == 'apply_engine':
            selected = self.option_states.get('engine', 'pygame')
            m.config['engine'] = selected
            m.JsonManager.save('data\\config', m.config)
            print(f"🔁 Switching engine to: {selected}. Restarting...")
            setattr(m, 'request_restart', True)
            return

        if action == 'win_white':
            m.PI.Game.game_over = True
            m.PI.Game.winner = 'white'
        elif action == 'win_black':
            m.PI.Game.game_over = True
            m.PI.Game.winner = 'black'
        elif action == 'switch_player':
            m.PI.Game.current_player = 'black' if m.PI.Game.current_player == 'white' else 'white'
        elif action == 'reset_board':
            m.PI.Game.restart(m)
        elif action == 'give_card_white':
            if hasattr(m, 'CardSystem'):
                card = m.CardSystem.give_random_card('white')
                if card:
                    print(f"🎴 Выдана карта белым: {card.name}")
        elif action == 'give_card_black':
            if hasattr(m, 'CardSystem'):
                card = m.CardSystem.give_random_card('black')
                if card:
                    print(f"🎴 Выдана карта черным: {card.name}")
        elif action == 'give_all_cards':
            if hasattr(m, 'CardSystem'):
                for _ in range(5):
                    m.CardSystem.give_random_card('white')
                    m.CardSystem.give_random_card('black')
                print(f"🎴 Выданы все карты обеим сторонам")
        elif action == 'clear_cards_white':
            if hasattr(m, 'CardSystem'):
                m.CardSystem.player_decks['white'] = []
        elif action == 'clear_cards_black':
            if hasattr(m, 'CardSystem'):
                m.CardSystem.player_decks['black'] = []
        
        # Открытие галереи карт
        elif action == 'open_card_gallery':
            self.card_gallery_open = not self.card_gallery_open
        
        elif action == 'shake_test':
            if hasattr(m.Disp, 'Game'):
                m.Disp.Game.start_shake(200, 15)
        elif action == 'reload_cards':
            if hasattr(m, 'CardSystem'):
                m.CardSystem.reload_cards()
        elif action == 'force_gc':
            import gc
            gc.collect()
            print("🗑️ Garbage collection выполнен")
        elif action == 'print_state':
            print(f"=== GAME STATE ===")
            print(f"Current Player: {m.PI.Game.current_player}")
            print(f"Game Over: {m.PI.Game.game_over}")
            print(f"Multiplayer: {m.PI.Game.multiplayer_mode}")
            print(f"Cards (white): {len(m.CardSystem.player_decks['white']) if hasattr(m, 'CardSystem') else 0}")
            print(f"Cards (black): {len(m.CardSystem.player_decks['black']) if hasattr(m, 'CardSystem') else 0}")
        elif action == 'spawn_pawn':
            import random
            x, y = random.randint(0, 7), random.randint(0, 7)
            team = random.choice(['white', 'black'])
            m.PI.Game.cells[x][y]['value'] = f'{team}_pawn'
            print(f"♟️ Пешка {team} создана на ({x}, {y})")
        elif action == 'randomize_board':
            import random
            pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
            for x in range(8):
                for y in range(8):
                    if random.random() < 0.3:
                        team = random.choice(['white', 'black'])
                        piece = random.choice(pieces)
                        m.PI.Game.cells[x][y]['value'] = f'{team}_{piece}'
        elif action == 'reset_menu':
            self.menu_width = 600
            self.menu_height = 500
            self.animation_speed = 15
            self.option_states['menu_width'] = 600
            self.option_states['menu_height'] = 500
            self.option_states['menu_alpha'] = 220
            self.option_states['menu_anim_speed'] = 15
            try:
                print("🔧 [DEV MENU] Настройки меню сброшены")
            except:
                print("[CFG] [DEV MENU] Настройки меню сброшены")
        elif action == 'reconnect_discord':
            if hasattr(m, 'DiscordRPC'):
                m.DiscordRPC.disconnect()
                if m.DiscordRPC.connect():
                    try:
                        print("🔄 [Discord RPC] Переподключено")
                    except:
                        print("[>>] [Discord RPC] Переподключено")
    
    def _give_specific_card(self, m, card_class_name):
        """Выдаёт конкретную карту текущему игроку"""
        if not hasattr(m, 'CardSystem'):
            return
        
        # Определяем текущего игрока
        if hasattr(m.PI, 'Game') and hasattr(m.PI.Game, 'current_player'):
            player = m.PI.Game.current_player
        else:
            player = 'white'  # По умолчанию
        
        # Ищем карту по имени класса в словаре available_cards
        # available_cards это словарь {имя_класса: класс_карты}
        card_class = None
        for class_name, cls in m.CardSystem.available_cards.items():
            if class_name == card_class_name:
                card_class = cls
                break
        
        if card_class:
            # Создаём экземпляр карты
            card_instance = card_class()
            
            # Добавляем карту в колоду игрока
            if player not in m.CardSystem.player_decks:
                m.CardSystem.player_decks[player] = []
            
            m.CardSystem.player_decks[player].append(card_instance)
            try:
                print(f"🎴 {player} получил карту: {card_instance.name}")
            except:
                print(f"[CARD] {player} получил карту: {card_instance.name}")
        else:
            try:
                print(f"❌ Карта {card_class_name} не найдена")
            except:
                print(f"[X] Карта {card_class_name} не найдена")
    
    def _handle_gallery_input(self, m, event):
        """Обработка ввода в галерее карт"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.card_gallery_open = False
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверяем клик по картам
            if self.hovered_gallery_card is not None:
                # Выдаём карту текущему игроку
                self._give_specific_card(m, self.hovered_gallery_card)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Колесико вверх
                self.gallery_scroll = max(0, self.gallery_scroll - 30)
            elif event.button == 5:  # Колесико вниз
                self.gallery_scroll += 30
    
    def _draw_card_gallery(self, m):
        """Рисует галерею карт"""
        screen = m.Disp.screen
        W, H = m.Disp.width, m.Disp.height
        
        # Затемнённый фон
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(150 * (self.alpha / 255))))
        screen.blit(overlay, (0, 0))
        
        # Главное окно галереи (больше чем обычное меню)
        gallery_width = min(1000, W - 100)
        gallery_height = min(700, H - 100)
        gallery_x = (W - gallery_width) // 2
        gallery_y = (H - gallery_height) // 2
        
        # Градиентный фон с эффектом глубины
        gallery_surface = pygame.Surface((gallery_width, gallery_height), pygame.SRCALPHA)
        
        menu_alpha = self.option_states.get('menu_alpha', 220)
        
        for i in range(gallery_height):
            progress = i / gallery_height
            alpha = int(menu_alpha * (self.alpha / 255))
            # Тёмно-синий градиент как в игре
            color = (
                int(10 + progress * 15),
                int(15 + progress * 20),
                int(30 + progress * 30),
                alpha
            )
            pygame.draw.line(gallery_surface, color, (0, i), (gallery_width, i))
        
        # Пульсирующая рамка
        import math
        pulse_color = int(abs(math.sin(self.glow_pulse)) * 80 + 120)
        for thickness in range(3):
            pygame.draw.rect(gallery_surface, 
                           (pulse_color, pulse_color + 30, 255, self.alpha), 
                           (thickness, thickness, gallery_width - thickness*2, gallery_height - thickness*2), 
                           1, border_radius=15)
        
        screen.blit(gallery_surface, (gallery_x, gallery_y))
        
        # Заголовок
        import sys, os
        def get_font(size):
            path = 'data/font/title.ttf' if os.path.exists('data/font/title.ttf') else None
            return pygame.font.Font(path, size) if path else pygame.font.Font(None, size)
        
        title_font = get_font(48)
        small_font = get_font(18)
        
        # Заголовок с эффектом свечения
        title_text = "CARD GALLERY"
        title_color = (100 + int(abs(math.sin(self.glow_pulse)) * 50), 200, 255)
        
        # Тень заголовка
        title_shadow = title_font.render(title_text, True, (0, 0, 50))
        screen.blit(title_shadow, (gallery_x + gallery_width//2 - title_shadow.get_width()//2 + 3, gallery_y + 23))
        
        title_surf = title_font.render(title_text, True, title_color)
        screen.blit(title_surf, (gallery_x + gallery_width//2 - title_surf.get_width()//2, gallery_y + 20))
        
        # Подзаголовок
        subtitle = small_font.render("Click on a card to add it to your inventory", True, (150, 150, 200))
        screen.blit(subtitle, (gallery_x + gallery_width//2 - subtitle.get_width()//2, gallery_y + 75))
        
        # Инструкция по закрытию
        close_text = small_font.render("Press ESC to close", True, (100, 100, 150))
        screen.blit(close_text, (gallery_x + gallery_width - close_text.get_width() - 20, gallery_y + 20))
        
        # Рисуем карты
        if hasattr(m, 'CardSystem') and m.CardSystem.available_cards:
            cards_area_y = gallery_y + 110
            cards_area_height = gallery_height - 130
            
            card_width = 140
            card_height = 180
            card_spacing = 20
            cards_per_row = (gallery_width - 40) // (card_width + card_spacing)
            
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_gallery_card = None
            
            card_list = list(m.CardSystem.available_cards.items())
            row = 0
            col = 0
            
            for card_name, card_class in card_list:
                # Создаём временный экземпляр для получения информации
                try:
                    temp_card = card_class()
                    card_info = temp_card.get_info()
                    
                    # Позиция карты
                    x = gallery_x + 20 + col * (card_width + card_spacing)
                    y = cards_area_y + row * (card_height + card_spacing) - self.gallery_scroll
                    
                    # Пропускаем если вне видимой области
                    if y + card_height < cards_area_y or y > cards_area_y + cards_area_height:
                        col += 1
                        if col >= cards_per_row:
                            col = 0
                            row += 1
                        continue
                    
                    # Проверяем hover
                    card_rect = pygame.Rect(x, y, card_width, card_height)
                    is_hovered = card_rect.collidepoint(mouse_pos) and cards_area_y < mouse_pos[1] < cards_area_y + cards_area_height
                    
                    if is_hovered:
                        self.hovered_gallery_card = card_name
                    
                    # Рисуем карту (используем стиль из CardUI)
                    self._draw_gallery_card(screen, x, y, card_width, card_height, card_info, is_hovered)
                    
                    col += 1
                    if col >= cards_per_row:
                        col = 0
                        row += 1
                        
                except Exception as e:
                    print(f"Ошибка отрисовки карты {card_name}: {e}")
                    col += 1
                    if col >= cards_per_row:
                        col = 0
                        row += 1
    
    def _draw_gallery_card(self, screen, x, y, w, h, card_info, is_hovered):
        """Рисует одну карту в галерее (в стиле CardUI)"""
        # Эффект при наведении
        if is_hovered:
            w = int(w * 1.05)
            h = int(h * 1.05)
            x -= int(w * 0.025)
            y -= int(h * 0.025)
        
        # Создаём поверхность карты
        card_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        
        # Фон карты с градиентом
        for i in range(h):
            progress = i / h
            alpha = 220 if not is_hovered else 255
            color = (
                int(20 + progress * 10),
                int(25 + progress * 15),
                int(40 + progress * 20),
                alpha
            )
            pygame.draw.line(card_surface, color, (0, i), (w, i))
        
        # Рамка карты (цвет зависит от редкости)
        rarity_colors = {
            'common': (120, 120, 120),
            'rare': (100, 150, 255),
            'epic': (200, 100, 255),
            'legendary': (255, 200, 50)
        }
        
        border_color = rarity_colors.get(card_info.get('rarity', 'common'), (120, 120, 120))
        
        if is_hovered:
            # Пульсирующая рамка при наведении
            import math
            pulse = int(abs(math.sin(self.glow_pulse)) * 50)
            border_color = tuple(min(255, c + pulse) for c in border_color)
        
        for thickness in range(3):
            pygame.draw.rect(card_surface, border_color,
                           (thickness, thickness, w - thickness*2, h - thickness*2),
                           1, border_radius=8)
        
        # Иконка карты
        icon = card_info.get('icon', '?')
        icon_font = pygame.font.Font(None, 48)
        icon_surf = icon_font.render(icon, True, card_info.get('color', (255, 255, 255)))
        icon_rect = icon_surf.get_rect(center=(w//2, h//3))
        card_surface.blit(icon_surf, icon_rect)
        
        # Название карты
        name_font = pygame.font.Font(None, 20)
        name_surf = name_font.render(card_info.get('name', 'Card'), True, (255, 255, 255))
        name_rect = name_surf.get_rect(center=(w//2, h//2 + 10))
        card_surface.blit(name_surf, name_rect)
        
        # Редкость
        rarity_font = pygame.font.Font(None, 16)
        rarity_text = card_info.get('rarity', 'common').upper()
        rarity_surf = rarity_font.render(rarity_text, True, border_color)
        rarity_rect = rarity_surf.get_rect(center=(w//2, h - 20))
        card_surface.blit(rarity_surf, rarity_rect)
        
        # Эффект свечения при наведении
        if is_hovered:
            glow_surface = pygame.Surface((w + 10, h + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*border_color, 50), (0, 0, w + 10, h + 10), border_radius=10)
            screen.blit(glow_surface, (x - 5, y - 5))
        
        screen.blit(card_surface, (x, y))
    
    def _handle_slider_drag(self, m, mouse_pos):
        """Обработка перетаскивания слайдера"""
        if not self.dragging_slider:
            return
        
        option = self.dragging_slider['option']
        
        # Вычисляем позицию слайдера
        menu_x = (m.Disp.width - self.menu_width) // 2
        menu_y = (m.Disp.height - self.menu_height) // 2
        options_y = menu_y + 80 + 50
        
        idx = self.dragging_slider['option_idx']
        opt_y = options_y + idx * 40 - self.scroll_offset
        
        slider_x = menu_x + 20 + self.menu_width - 40 - 200
        slider_width = 180
        
        # Вычисляем новое значение
        relative_x = mouse_pos[0] - slider_x
        relative_x = max(0, min(relative_x, slider_width))
        
        norm = relative_x / slider_width
        new_value = option['min'] + norm * (option['max'] - option['min'])
        
        # Округляем для целых чисел
        if isinstance(option['value'], int):
            new_value = int(new_value)
        
        self.option_states[option['var']] = new_value
        self._apply_option(m, option)
    
    def _apply_option(self, m, option):
        """Применение опции"""
        if option['var'] == 'card_drop_chance' and hasattr(m, 'CardSystem'):
            m.CardSystem.card_drop_chance = self.option_states[option['var']]
        elif option['var'] == 'max_cards' and hasattr(m, 'CardSystem'):
            m.CardSystem.max_cards_per_player = int(self.option_states[option['var']])
        elif option['var'] == 'target_fps':
            m.target_fps = int(self.option_states[option['var']])
        elif option['var'] == 'menu_width':
            self.menu_width = int(self.option_states[option['var']])
        elif option['var'] == 'menu_height':
            self.menu_height = int(self.option_states[option['var']])
        elif option['var'] == 'menu_anim_speed':
            self.animation_speed = int(self.option_states[option['var']])
        elif option['var'] == 'discord_rpc' and hasattr(m, 'DiscordRPC'):
            # Включение/выключение Discord RPC
            if self.option_states[option['var']]:
                m.DiscordRPC.enable()
            else:
                m.DiscordRPC.disable()
    
    def draw(self, m):
        """Отрисовка меню"""
        if self.alpha <= 0:
            return
        
        # Если открыта галерея карт, рисуем её вместо главного меню
        if self.card_gallery_open:
            self._draw_card_gallery(m)
            return
        
        screen = m.Disp.screen
        W, H = m.Disp.width, m.Disp.height
        
        # Полупрозрачный фон
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(120 * (self.alpha / 255))))
        screen.blit(overlay, (0, 0))
        
        # Главное окно
        menu_x = (W - self.menu_width) // 2
        menu_y = (H - self.menu_height) // 2
        
        # Фон окна (градиент)
        menu_surface = pygame.Surface((self.menu_width, self.menu_height), pygame.SRCALPHA)
        
        menu_alpha = self.option_states.get('menu_alpha', 220)
        
        for i in range(self.menu_height):
            progress = i / self.menu_height
            alpha = int(menu_alpha * (self.alpha / 255))
            color = (
                int(15 + progress * 5),
                int(15 + progress * 5),
                int(25 + progress * 10),
                alpha
            )
            pygame.draw.line(menu_surface, color, (0, i), (self.menu_width, i))
        
        # Рамка окна
        import math
        pulse_color = int(abs(math.sin(self.pulse)) * 50 + 100)
        pygame.draw.rect(menu_surface, (pulse_color, pulse_color + 50, 255, self.alpha), 
                        (0, 0, self.menu_width, self.menu_height), 2, border_radius=10)
        
        screen.blit(menu_surface, (menu_x, menu_y))
        
        # FPS в меню если включено
        if self.option_states.get('menu_show_fps', False):
            fps = m.clock.get_fps()
            fps_text = f"FPS: {fps:.1f}"
            try:
                fps_surf = font_small.render(fps_text, True, (100, 255, 100))
            except:
                fps_surf = font_small.render(fps_text, True, (100, 255, 100))
            screen.blit(fps_surf, (menu_x + self.menu_width - 80, menu_y - 25))
        
        # Заголовок
        import sys, os
        def get_font(size):
            path = 'data/font/title.ttf' if os.path.exists('data/font/title.ttf') else None
            return pygame.font.Font(path, size) if path else pygame.font.Font(None, size)
        
        title_font = get_font(32)
        title = title_font.render("DEV MENU", True, (255, 255, 255, self.alpha))
        screen.blit(title, (menu_x + 20, menu_y + 15))
        
        # Версия
        small_font = get_font(14)
        version = small_font.render("v1.0 | Chess Isometry Rework", True, (150, 150, 150, self.alpha))
        screen.blit(version, (menu_x + 20, menu_y + 50))
        
        # Категории (табы)
        tab_y = menu_y + 80
        tab_width = self.menu_width // len(self.categories)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, cat in enumerate(self.categories):
            tab_x = menu_x + i * tab_width
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, 35)
            
            is_active = (i == self.current_category)
            is_hover = tab_rect.collidepoint(mouse_pos) and self.active
            
            # Фон таба
            if is_active:
                color = (50, 80, 150, int(200 * (self.alpha / 255)))
            elif is_hover:
                color = (40, 40, 60, int(180 * (self.alpha / 255)))
            else:
                color = (25, 25, 35, int(160 * (self.alpha / 255)))
            
            tab_surf = pygame.Surface((tab_width, 35), pygame.SRCALPHA)
            pygame.draw.rect(tab_surf, color, (0, 0, tab_width, 35), border_radius=5)
            screen.blit(tab_surf, (tab_x, tab_y))
            
            # Текст таба
            text_color = (255, 255, 255, self.alpha) if is_active else (180, 180, 180, self.alpha)
            tab_text = small_font.render(cat, True, text_color[:3])
            tab_text.set_alpha(self.alpha)
            text_rect = tab_text.get_rect(center=(tab_x + tab_width // 2, tab_y + 17))
            screen.blit(tab_text, text_rect)
        
        # Опции текущей категории
        options_y = tab_y + 50
        current_options = self.options[self.categories[self.current_category]]
        
        self.hover_option = None
        
        for idx, option in enumerate(current_options):
            opt_y = options_y + idx * 40 - self.scroll_offset
            
            if opt_y < options_y - 20 or opt_y > menu_y + self.menu_height - 20:
                continue
            
            opt_rect = pygame.Rect(menu_x + 20, opt_y, self.menu_width - 40, 35)
            
            is_hover = opt_rect.collidepoint(mouse_pos) and self.active
            if is_hover:
                self.hover_option = idx
            
            self._draw_option(screen, option, menu_x + 20, opt_y, self.menu_width - 40, is_hover)
        
        # FPS Counter
        if self.option_states.get('fps_counter'):
            self._draw_fps_counter(screen, W, H)
        
        # Performance Monitor
        if self.option_states.get('perf_monitor'):
            self._draw_perf_monitor(screen, m, W, H)
    
    def _draw_option(self, screen, option, x, y, width, is_hover):
        """Отрисовка опции"""
        small_font = pygame.font.Font(None, 20)
        
        # Фон опции
        if is_hover:
            bg = pygame.Surface((width, 35), pygame.SRCALPHA)
            pygame.draw.rect(bg, (60, 60, 80, int(150 * (self.alpha / 255))), (0, 0, width, 35), border_radius=5)
            screen.blit(bg, (x, y))
        
        # Название
        name_text = small_font.render(option['name'], True, (255, 255, 255))
        name_text.set_alpha(self.alpha)
        screen.blit(name_text, (x + 10, y + 10))
        
        # Элемент управления
        if option['type'] == 'checkbox':
            self._draw_checkbox(screen, x + width - 40, y + 8, option)
        elif option['type'] == 'slider':
            self._draw_slider(screen, x + width - 200, y + 8, 180, option)
        elif option['type'] == 'button':
            self._draw_button(screen, x + width - 100, y + 5, 90, option, is_hover)
        elif option['type'] == 'dropdown':
            self._draw_dropdown(screen, x + width - 200, y + 5, 180, option)
    
    def _draw_checkbox(self, screen, x, y, option):
        """Отрисовка чекбокса"""
        checked = self.option_states.get(option['var'], False)
        
        # Фон чекбокса
        bg_color = (80, 180, 80) if checked else (60, 60, 70)
        pygame.draw.rect(screen, bg_color, (x, y, 25, 20), border_radius=3)
        pygame.draw.rect(screen, (200, 200, 200), (x, y, 25, 20), 2, border_radius=3)
        
        # Галочка
        if checked:
            pygame.draw.line(screen, (255, 255, 255), (x + 5, y + 10), (x + 10, y + 15), 2)
            pygame.draw.line(screen, (255, 255, 255), (x + 10, y + 15), (x + 20, y + 5), 2)
    
    def _draw_slider(self, screen, x, y, width, option):
        """Отрисовка слайдера"""
        value = self.option_states.get(option['var'], option['value'])
        min_val = option['min']
        max_val = option['max']
        
        # Нормализация
        norm = (value - min_val) / (max_val - min_val) if max_val != min_val else 0
        
        # Фон слайдера
        pygame.draw.rect(screen, (40, 40, 50), (x, y + 5, width, 10), border_radius=5)
        
        # Заполнение
        fill_width = int(width * norm)
        pygame.draw.rect(screen, (80, 150, 255), (x, y + 5, fill_width, 10), border_radius=5)
        
        # Ручка
        handle_x = x + fill_width
        pygame.draw.circle(screen, (255, 255, 255), (handle_x, y + 10), 8)
        pygame.draw.circle(screen, (100, 150, 255), (handle_x, y + 10), 6)
        
        # Значение
        small_font = pygame.font.Font(None, 16)
        val_text = small_font.render(f"{value:.2f}" if isinstance(value, float) else str(int(value)), True, (200, 200, 200))
        screen.blit(val_text, (x + width + 10, y + 3))
    
    def _draw_button(self, screen, x, y, width, option, is_hover):
        """Отрисовка кнопки"""
        # Фон кнопки
        color = (70, 120, 200) if is_hover else (50, 80, 150)
        pygame.draw.rect(screen, color, (x, y, width, 25), border_radius=5)
        pygame.draw.rect(screen, (150, 150, 150), (x, y, width, 25), 2, border_radius=5)
        
        # Текст
        small_font = pygame.font.Font(None, 16)
        btn_text = small_font.render("Execute", True, (255, 255, 255))
        text_rect = btn_text.get_rect(center=(x + width // 2, y + 12))
        screen.blit(btn_text, text_rect)

    def _draw_dropdown(self, screen, x, y, width, option):
        """Отрисовка простого дропдауна (без выпадающего списка, клик по области циклично переключает)"""
        value = self.option_states.get(option['var'], option.get('value'))
        items = option.get('items', [])
        rect = pygame.Rect(x, y, width, 25)
        pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=5)
        pygame.draw.rect(screen, (150, 150, 150), rect, 2, border_radius=5)
        small_font = pygame.font.Font(None, 16)
        text = small_font.render(str(value), True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + width // 2, y + 12))
        screen.blit(text, text_rect)
        # Обработка клика по дропдауну
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and rect.collidepoint(mouse_pos):
            if items:
                try:
                    idx = items.index(value)
                except ValueError:
                    idx = -1
                idx = (idx + 1) % len(items)
                self.option_states[option['var']] = items[idx]
    
    def _draw_fps_counter(self, screen, W, H):
        """FPS счетчик"""
        if not self.frame_times:
            return
        
        avg_dt = sum(self.frame_times) / len(self.frame_times)
        fps = 1.0 / avg_dt if avg_dt > 0 else 0
        
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {int(fps)}", True, (0, 255, 0))
        screen.blit(fps_text, (W - 100, 10))
    
    def _draw_perf_monitor(self, screen, m, W, H):
        """Монитор производительности"""
        font = pygame.font.Font(None, 18)
        y_offset = 40
        
        stats = [
            f"Uptime: {int(time.time() - self.start_time)}s",
            f"Scene: {m.scene}",
            f"Zoom: {m.config.get('zoom', 1.0):.2f}",
        ]
        
        for stat in stats:
            text = font.render(stat, True, (255, 255, 0))
            screen.blit(text, (W - 200, y_offset))
            y_offset += 20

