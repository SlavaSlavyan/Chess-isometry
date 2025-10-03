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
        
        # Анимации
        self.pulse = 0
        
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
        
        # Обновляем FPS счетчик
        if self.option_states.get('fps_counter'):
            self.frame_times.append(dt)
            if len(self.frame_times) > 60:
                self.frame_times.pop(0)
    
    def handle_input(self, m, event):
        """Обработка ввода"""
        if not self.active:
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

