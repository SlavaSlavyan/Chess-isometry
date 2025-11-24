import pygame
import math

class PieseMove:
        
    def __init__(self,m):
        self.game = None  # Будет устанавливаться при вызове
    
    def main(self,m,x:int,y:int):
        
        piece_type = m.PI.Game.cells[x][y]['value'][6:]
        team = m.PI.Game.cells[x][y]['value'][:5]
        
        if piece_type == "pawn":
            self.pawn(m,x,y,team)
        elif piece_type == "rook":
            self.rook(m,x,y,team)
        elif piece_type == "bishop":
            self.bishop(m,x,y,team)
        elif piece_type == "knight":
            self.knight(m,x,y,team)
        elif piece_type == "queen":
            self.queen(m,x,y,team)
        elif piece_type == "king":
            self.king(m,x,y,team)
    
    def is_valid_position(self, x, y):
        """Проверяет, находится ли позиция в пределах доски"""
        return 0 <= x < 8 and 0 <= y < 8
    
    def is_enemy_piece(self, m, x, y, team):
        """Проверяет, является ли фигура на позиции вражеской"""
        if not self.is_valid_position(x, y):
            return False
        cells = m.PI.Game.cells if m else self.game.cells
        cell_value = cells[x][y]['value']
        if cell_value == "empty":
            return False
        return cell_value[:5] != team
    
    def is_empty_cell(self, m, x, y):
        """Проверяет, пуста ли клетка"""
        if not self.is_valid_position(x, y):
            return False
        cells = m.PI.Game.cells if m else self.game.cells
        return cells[x][y]['value'] == "empty"
    
    def add_move_if_valid(self, m, x, y, team):
        """Добавляет ход, если позиция валидна"""
        if not self.is_valid_position(x, y):
            return False
        
        # Используем игровое поле из переданного контекста или из self.game
        cells = m.PI.Game.cells if m else self.game.cells
        
        if self.is_empty_cell(m, x, y):
            cells[x][y]['status'] = 'move'
            return True
        elif self.is_enemy_piece(m, x, y, team):
            cells[x][y]['status'] = 'attack'
            return False  # Блокируется вражеской фигурой
        else:
            return False  # Блокируется своей фигурой
            
    def pawn(self,m,x:int,y:int,team:str):
        
        cells = m.PI.Game.cells if m else self.game.cells
        
        if team == 'white':
            # Движение вперед
            if y+1<8:
                if cells[x][y+1]['value'] == "empty":
                    cells[x][y+1]['status'] = 'move'
                    # Двойной ход с начальной позиции
                    if y == 1 and y+2<8 and cells[x][y+2]['value'] == "empty":
                        cells[x][y+2]['status'] = 'move'
                
                # Атака по диагонали
                if x-1>=0 and cells[x-1][y+1]['value'][:5] == "black":
                    cells[x-1][y+1]['status'] = 'attack'
                if x+1<8 and cells[x+1][y+1]['value'][:5] == "black":
                    cells[x+1][y+1]['status'] = 'attack'
                        
        elif team == 'black':
            # Движение вперед
            if y-1>=0:
                if cells[x][y-1]['value'] == "empty":
                    cells[x][y-1]['status'] = 'move'
                    # Двойной ход с начальной позиции
                    if y == 6 and y-2>=0 and cells[x][y-2]['value'] == "empty":
                        cells[x][y-2]['status'] = 'move'
                
                # Атака по диагонали
                if x-1>=0 and cells[x-1][y-1]['value'][:5] == "white":
                    cells[x-1][y-1]['status'] = 'attack'
                if x+1<8 and cells[x+1][y-1]['value'][:5] == "white":
                    cells[x+1][y-1]['status'] = 'attack'
    
    def rook(self, m, x: int, y: int, team: str):
        """Логика движения ладьи - горизонтально и вертикально"""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # вверх, вниз, вправо, влево
        
        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i
                if not self.add_move_if_valid(m, new_x, new_y, team):
                    break
    
    def bishop(self, m, x: int, y: int, team: str):
        """Логика движения слона - по диагоналям"""
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # все диагонали
        
        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i
                if not self.add_move_if_valid(m, new_x, new_y, team):
                    break
    
    def knight(self, m, x: int, y: int, team: str):
        """Логика движения коня - буквой Г"""
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dx, dy in knight_moves:
            new_x, new_y = x + dx, y + dy
            self.add_move_if_valid(m, new_x, new_y, team)
    
    def queen(self, m, x: int, y: int, team: str):
        """Логика движения ферзя - комбинация ладьи и слона"""
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # как ладья
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # как слон
        ]
        
        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i
                if not self.add_move_if_valid(m, new_x, new_y, team):
                    break
    
    def king(self, m, x: int, y: int, team: str):
        """Логика движения короля - на одну клетку в любом направлении"""
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # горизонтально и вертикально
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # по диагоналям
        ]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            self.add_move_if_valid(m, new_x, new_y, team)

class Game:

    def __init__(self,m):
        
        self.PM = PieseMove(m)

        self.cells = [
            [{"value":"white_rook" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_rook" }],
            [{"value":"white_knight" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_knight" }],
            [{"value":"white_bishop" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_bishop" }],
            [{"value":"white_queen" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_queen" }],
            [{"value":"white_king" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_king" }],
            [{"value":"white_bishop" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_bishop" }],
            [{"value":"white_knight" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_knight" }],
            [{"value":"white_rook" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_rook" }]
        ]
        
        for line in self.cells:
            for cell in line:
                
                cell['pos'] = []
                cell['offset'] = []
                cell['points'] = []
                cell['status'] = "none"
        
        self.selected_cell = None
        self.current_player = "white"  # Белые ходят первыми
        self.game_over = False
        self.winner = None
        self.game_started = False
        
        # Мультиплеер
        self.multiplayer_mode = False
        self.is_host = False
        self.my_team = "white"  # Какой команде принадлежит локальный игрок
        self.waiting_for_opponent = False  # Флаг начала игры

        # Анимации
        self.anim_move = None  # {'from':(x,y),'to':(x,y),'piece':str,'start':ms,'dur':ms,'is_attack':bool}
        
        # Система карт
        self.card_notification = None  # {'card_info': {}, 'timer': int, 'max_timer': int}
        self.selected_card = None  # {'index': int, 'card': Card, 'requires_target': bool}
        self.card_target_mode = None  # 'single_cell', 'two_cells', None
        
        # Эффекты карт
        self.extra_move_active = False
        self.extra_move_player = None
        self.fog_of_war_active = False
        self.fog_of_war_owner = None
        self.fog_of_war_duration = 0
    
    def main(self,m):
        
        # Экспорт состояния для чита
        self.export_game_state(m)

        self.key_input(m)
        # Обновляем эффект тряски экрана
        if hasattr(m.Disp, 'Game') and hasattr(m.Disp.Game, 'update_shake'):
            m.Disp.Game.update_shake(m)
        # Обновляем анимации
        self.update_move_animation(m)
        self.createpos(m)
        self.mouse_input(m)

    def createpos(self,m):

        z = m.config['zoom']
        
        for y in range(8):
            for x in range(8):
                
                offset_x = x * 50*z - 175*z
                offset_y = y * 50*z - 175*z

                rotated_x = offset_x * math.cos(math.pi*m.Disp.Game.rotate[0]/180) - offset_y * math.sin(math.pi*m.Disp.Game.rotate[0]/180)
                rotated_y = (offset_x * math.sin(math.pi*m.Disp.Game.rotate[0]/180) + offset_y * math.cos(math.pi*m.Disp.Game.rotate[0]/180))*math.sin(math.pi*m.Disp.Game.rotate[1]/180)

                draw_x = int(m.Disp.width//2 + rotated_x)
                draw_y = int(m.Disp.height//2 + rotated_y)

                self.cells[x][y]['pos'] = [draw_x,draw_y]
                self.cells[x][y]['points'] = m.Disp.Game.square(m,self.cells[x][y]['pos'],50/(math.pi/2.2))

    def key_input(self,m):

        # Обработка клавиш в конце игры
        if self.game_over:
            if m.PI.KI.keys['r']['press']:
                self.restart_game(m)
            if m.PI.KI.keys['esc']['press']:
                m.set_scene('menu')  # Возвращаемся в меню вместо выхода
            return
        
        # Возврат в меню во время игры
        if m.PI.KI.keys['esc']['press']:
            m.set_scene('menu')
            return
        
        # Обычные клавиши управления камерой (не работают если чат активен)
        if hasattr(m, 'ChatSystem') and m.ChatSystem.input_active:
            return  # Блокируем управление камерой при вводе в чат
        
        if m.PI.KI.keys['up']['value'] or m.PI.KI.keys['w']['value']:
            m.Disp.Game.rotate[1] += 1
        if m.PI.KI.keys['down']['value'] or m.PI.KI.keys['s']['value']:
            m.Disp.Game.rotate[1] -= 1
        if m.PI.KI.keys['left']['value'] or m.PI.KI.keys['a']['value']:
            m.Disp.Game.rotate[0] -= 1
        if m.PI.KI.keys['right']['value'] or m.PI.KI.keys['d']['value']:
            m.Disp.Game.rotate[0] += 1
        
        for i in range(2):
            
            if m.Disp.Game.rotate[i] > 180:
                m.Disp.Game.rotate[i] -= 360
            
            if m.Disp.Game.rotate[i] < -180:
                m.Disp.Game.rotate[i] += 360
    
    def restart_game(self, m):
        """Перезапускает игру"""
        # Сбрасываем доску к начальному состоянию
        self.cells = [
            [{"value":"white_rook" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_rook" }],
            [{"value":"white_knight" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_knight" }],
            [{"value":"white_bishop" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_bishop" }],
            [{"value":"white_queen" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_queen" }],
            [{"value":"white_king" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_king" }],
            [{"value":"white_bishop" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_bishop" }],
            [{"value":"white_knight" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_knight" }],
            [{"value":"white_rook" },{"value":"white_pawn" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"empty" },{"value":"black_pawn" },{"value":"black_rook" }]
        ]
        
        # Инициализируем позиции и статусы клеток
        for line in self.cells:
            for cell in line:
                cell['pos'] = []
                cell['offset'] = []
                cell['points'] = []
                cell['status'] = "none"
        
        # Сбрасываем состояние игры
        self.selected_cell = None
        self.current_player = "white"
        self.game_over = False
        self.winner = None
        self.game_started = False
        
        print("🔄 Игра перезапущена!")
    
    def setup_multiplayer(self, m, is_host: bool):
        """Настраивает игру для мультиплеера"""
        self.multiplayer_mode = True
        self.is_host = is_host
        self.my_team = "white" if is_host else "black"
        
        # Настраиваем обработчик сетевых сообщений
        if hasattr(m, 'NetworkManager'):
            m.NetworkManager.on_message_received = lambda msg: self.handle_network_message(m, msg)
        
        print(f"🌐 Мультиплеер настроен: {'Хост' if is_host else 'Клиент'}, команда: {self.my_team}")
    
    def send_move(self, m, from_pos: tuple, to_pos: tuple):
        """Отправляет ход по сети"""
        if hasattr(m, 'NetworkManager') and m.NetworkManager.is_connected:
            move_data = {
                'from': from_pos,
                'to': to_pos,
                'player': self.current_player,
                'board_state': self.get_board_state()
            }
            m.NetworkManager.send_message('game_move', move_data)
    
    def handle_network_message(self, m, message):
        """Обрабатывает сетевые сообщения"""
        msg_type = message.get('type')
        data = message.get('data', {})
        
        if msg_type == 'game_move':
            self.receive_move(m, data)
        elif msg_type == 'game_state_sync':
            self.sync_game_state(m, data)
    
    def receive_move(self, m, move_data):
        """Получает ход от противника"""
        from_pos = tuple(move_data.get('from', (0, 0)))
        to_pos = tuple(move_data.get('to', (0, 0)))
        player = move_data.get('player', 'white')
        
        # Проверяем что ход от противника
        if player == self.my_team:
            return
        
        # Применяем ход
        self.apply_remote_move(m, from_pos, to_pos)
    
    def apply_remote_move(self, m, from_pos: tuple, to_pos: tuple):
        """Применяет ход противника"""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        # Проверяем валидность хода (базовая проверка)
        if not (0 <= from_x < 8 and 0 <= from_y < 8 and 0 <= to_x < 8 and 0 <= to_y < 8):
            return
        
        # Запускаем анимацию для хода противника
        is_attack = self.cells[to_x][to_y]['value'] != "empty"
        
        # Применяем ход напрямую (без анимации для удаленного хода)
        self.make_move(from_pos, to_pos, m)
        self.switch_player(m)
        
        print(f"📩 Получен ход противника: {from_pos} -> {to_pos}")
    
    def get_board_state(self):
        """Возвращает текущее состояние доски"""
        board_state = []
        for x in range(8):
            row = []
            for y in range(8):
                row.append(self.cells[x][y]['value'])
            board_state.append(row)
        return board_state
    
    def sync_game_state(self, m, state_data):
        """Синхронизирует состояние игры"""
        board_state = state_data.get('board_state', [])
        current_player = state_data.get('current_player', 'white')
        
        if len(board_state) == 8:
            for x in range(8):
                if len(board_state[x]) == 8:
                    for y in range(8):
                        self.cells[x][y]['value'] = board_state[x][y]
            
            self.current_player = current_player
            print("🔄 Состояние игры синхронизировано")
    
    def mouse_input(self,m):
        
        if self.game_over:
            return

        # Блокируем ввод на время анимации перемещения
        if self.anim_move is not None:
            return
        
        # В мультиплеере блокируем ввод если не наша очередь
        if self.multiplayer_mode:
            if self.current_player != self.my_team:
                return

        # Правая кнопка мыши - отменяем выбор карты
        if m.PI.MI.mouse_click['rt']:
            if self.selected_card or self.card_target_mode:
                print("❌ Использование карты отменено")
                self.selected_card = None
                self.card_target_mode = None
                self.card_target_positions = []
                return
        
        if m.PI.MI.mouse_click['lt']:
            # Сначала проверяем клик по картам
            if hasattr(m, 'CardSystem') and hasattr(m, 'CardUI'):
                card_clicked = self.handle_card_click(m)
                if card_clicked:
                    return  # Если кликнули по карте, не обрабатываем клики по доске
            clicked_cell = None

            # Проверяем, на какую клетку кликнули
            for x in range(8):
                for y in range(8):
                    if self.is_point_in_polygon(m.PI.MI.mouse_pos, self.cells[x][y]['points']):
                        clicked_cell = [x, y]
                        break
                if clicked_cell:
                    break

            if clicked_cell:
                x, y = clicked_cell

                # Если есть выбранная фигура и кликнули на возможный ход
                if self.selected_cell and self.cells[x][y]['status'] in ['move', 'attack']:
                    # Запускаем анимацию перемещения
                    is_attack = (self.cells[x][y]['status'] == 'attack' and self.cells[x][y]['value'] != 'empty')
                    self.start_move_animation(m, tuple(self.selected_cell), (x, y), is_attack)
                    return

                # Очищаем старые статусы перед новым выбором
                self.clear_all_statuses()

                # Если кликнули на фигуру текущего игрока
                if (self.cells[x][y]['value'] != "empty" and 
                    self.cells[x][y]['value'][:5] == self.current_player):
                    self.selected_cell = [x, y]

                # Если кликнули на пустую клетку или чужую фигуру без выбранной фигуры
                else:
                    self.selected_cell = None
        
        # Показываем возможные ходы для выбранной фигуры
        if self.selected_cell:
            x, y = self.selected_cell
            self.cells[x][y]['status'] = "selected"
            self.PM.main(m, x, y)
    
    def clear_all_statuses(self):
        """Очищает все статусы клеток"""
        for x in range(8):
            for y in range(8):
                if self.cells[x][y]['status'] in ['move', 'attack', 'selected']:
                    self.cells[x][y]['status'] = None
    
    def make_move(self, from_pos, to_pos, m):
        """Выполняет ход фигуры"""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        # Отмечаем что игра началась
        self.game_started = True
        
        # Проверяем, съедается ли фигура
        captured_piece = self.cells[to_x][to_y]['value']
        if captured_piece != "empty":
            # Воспроизводим звук взятия фигуры
            m.AudioManager.play_sfx("hit")
            # Создаем эффект распада съеденной фигуры
            m.Disp.Game.create_destruction_effect(m, (to_x, to_y), captured_piece)
            
            # === ЭФФЕКТ: Screen Shake при взятии фигуры ===
            if hasattr(m, 'Shaders'):
                # Сила тряски зависит от важности фигуры
                shake_intensity = 5.0
                if 'king' in captured_piece:
                    shake_intensity = 20.0
                elif 'queen' in captured_piece:
                    shake_intensity = 15.0
                elif 'rook' in captured_piece:
                    shake_intensity = 10.0
                
                m.Shaders.trigger_shake(duration=0.3, intensity=shake_intensity)
            
            # Проверяем, съедается ли король
            if captured_piece.endswith('_king'):
                # Игра окончена - король съеден!
                winner = self.current_player
                self.game_over = True
                self.winner = winner
                print(f"🎉 ИГРА ОКОНЧЕНА! {winner.upper()} ПОБЕДИЛ!")
                
                # === ЭФФЕКТ: Bloom + Chromatic Aberration при победе ===
                if hasattr(m, 'Shaders'):
                    m.Shaders.bloom_enabled = True
                    m.Shaders.bloom_intensity = 0.6
                    m.Shaders.chromatic_aberration_enabled = True
                    m.Shaders.aberration_amount = 3.0
        
        # Перемещаем фигуру
        piece = self.cells[from_x][from_y]['value']
        self.cells[to_x][to_y]['value'] = piece
        self.cells[from_x][from_y]['value'] = "empty"
        
        # Очищаем статусы
        self.cells[from_x][from_y]['status'] = None
        self.cells[to_x][to_y]['status'] = None

    def start_move_animation(self, m, from_pos:tuple, to_pos:tuple, is_attack:bool):
        """Запускает анимацию перемещения фигуры"""
        fx, fy = from_pos
        piece = self.cells[fx][fy]['value']
        self.anim_move = {
            'from': from_pos,
            'to': to_pos,
            'piece': piece,
            'start': pygame.time.get_ticks(),
            'dur': 180,  # миллисекунд
            'is_attack': is_attack
        }

    def update_move_animation(self, m):
        """Шаг анимации перемещения. По завершении применяет ход."""
        if not self.anim_move:
            return
        now = pygame.time.get_ticks()
        t0 = self.anim_move['start']
        dur = self.anim_move['dur']
        if now - t0 >= dur:
            # Завершаем анимацию: применяем ход, переключаем игрока, очищаем статусы
            from_pos = self.anim_move['from']
            to_pos = self.anim_move['to']
            is_attack = self.anim_move['is_attack']
            self.anim_move = None
            self.make_move(from_pos, to_pos, m)
            # Небольшая тряска при взятии
            if is_attack and hasattr(m.Disp, 'Game') and hasattr(m.Disp.Game, 'start_shake'):
                amp = 6
                if 'zoom' in m.config:
                    amp = max(4, int(2 * m.config['zoom']))
                m.Disp.Game.start_shake(120, amp)
            self.selected_cell = None
            
            # Отправляем ход по сети в мультиплеере
            if self.multiplayer_mode and hasattr(m, 'NetworkManager') and m.NetworkManager.is_connected:
                self.send_move(m, from_pos, to_pos)
            
            self.switch_player(m)
            self.clear_all_statuses()
    
    def switch_player(self, m=None):
        """Переключает текущего игрока и пытается выдать карту"""
        old_player = self.current_player
        
        # Проверяем эффект двойного хода
        if self.extra_move_active and self.extra_move_player == old_player:
            print(f"⚡ Дополнительный ход для {old_player}!")
            self.extra_move_active = False
            self.extra_move_player = None
            # НЕ переключаем игрока, возвращаем управление
            return
        
        # Обычное переключение игрока
        self.current_player = "black" if self.current_player == "white" else "white"
        
        # Обновляем эффекты
        if self.fog_of_war_active:
            self.fog_of_war_duration -= 1
            if self.fog_of_war_duration <= 0:
                self.fog_of_war_active = False
                print(f"🌫️ Туман войны рассеялся!")
        
        # Попытка выдать карту игроку, который ТОЛЬКО ЧТО сходил
        if m and hasattr(m, 'CardSystem') and self.game_started:
            dropped_card = m.CardSystem.try_drop_card(old_player)
            if dropped_card:
                # Показываем уведомление
                self.card_notification = {
                    'card_info': dropped_card.get_info(),
                    'timer': 120,  # 2 секунды при 60 FPS
                    'max_timer': 120
                }
                print(f"🎴 {old_player} получил карту: {dropped_card.name}")
            
            # Вызываем события начала хода для нового игрока
            m.CardSystem.on_turn_start(self.current_player, self._get_game_state(m))
    
    def _get_game_state(self, m):
        """Возвращает состояние игры для карт с прямым доступом к доске"""
        # Создаем wrapper который позволяет картам напрямую изменять доску
        class BoardWrapper:
            def __init__(self, cells):
                self.cells = cells
            
            def __getitem__(self, y):
                # board[y][x] -> cells[x][y]
                class RowWrapper:
                    def __init__(self, cells, y):
                        self.cells = cells
                        self.y = y
                    
                    def __getitem__(self, x):
                        return self.cells[x][self.y]
                    
                    def __setitem__(self, x, value):
                        self.cells[x][self.y] = value
                
                return RowWrapper(self.cells, y)
        
        return {
            'board': BoardWrapper(self.cells),
            'current_player': self.current_player,
            'move_history': [],
            'captured_pieces': {'white': [], 'black': []},
            'm': m,
            'game': self  # Прямая ссылка на объект игры
        }
    
    def handle_card_click(self, m):
        """Обрабатывает клики по картам. Возвращает True если кликнули по карте или в режиме выбора цели"""
        # Если уже в режиме выбора цели, обрабатываем клики по доске
        if self.selected_card and self.card_target_mode:
            clicked_cell = None
            
            for x in range(8):
                for y in range(8):
                    if self.is_point_in_polygon(m.PI.MI.mouse_pos, self.cells[x][y]['points']):
                        clicked_cell = (x, y)
                        break
                if clicked_cell:
                    break
            
            if clicked_cell:
                if self.card_target_mode == 'single_cell':
                    # Используем карту с одной целью
                    target = {'pos': clicked_cell}
                    success, message = m.CardSystem.use_card(
                        self.current_player,
                        self.selected_card['index'],
                        self._get_game_state(m),
                        target
                    )
                    print(f"{'✅' if success else '❌'} {message}")
                    # Полностью очищаем состояние карты
                    self.selected_card = None
                    self.card_target_mode = None
                    if hasattr(self, 'card_target_positions'):
                        self.card_target_positions = []
                    # Сбрасываем hover карты
                    m.CardUI.reset_hover()
                    return True
                
                elif self.card_target_mode == 'two_cells':
                    # Собираем две позиции
                    if not hasattr(self, 'card_target_positions'):
                        self.card_target_positions = []
                    
                    self.card_target_positions.append(clicked_cell)
                    
                    if len(self.card_target_positions) == 1:
                        print(f"🎯 Первая фигура выбрана: {clicked_cell}. Выберите вторую...")
                    elif len(self.card_target_positions) == 2:
                        # Используем карту с двумя целями
                        target = {
                            'pos1': self.card_target_positions[0],
                            'pos2': self.card_target_positions[1]
                        }
                        success, message = m.CardSystem.use_card(
                            self.current_player,
                            self.selected_card['index'],
                            self._get_game_state(m),
                            target
                        )
                        print(f"{'✅' if success else '❌'} {message}")
                        # Полностью очищаем состояние карты
                        self.selected_card = None
                        self.card_target_mode = None
                        self.card_target_positions = []
                        # Сбрасываем hover карты
                        m.CardUI.reset_hover()
                        # После использования возвращаем False чтобы разрешить обычные клики
                        return False
                    
                    return True
            
            # Если кликнули мимо, все равно блокируем клик (чтобы не ходили фигурами)
            return True
        
        # Проверяем клик по самим картам
        hovered_card = m.CardUI.get_hovered_card()
        
        if hovered_card is not None:
            # Получаем карты текущего игрока
            cards = m.CardSystem.get_player_cards(self.current_player)
            
            if hovered_card < len(cards):
                card = cards[hovered_card]
                
                # Проверяем можно ли использовать карту
                can_use, reason = card.can_use(self._get_game_state(m))
                
                if not can_use:
                    print(f"❌ Нельзя использовать карту: {reason}")
                    # Если карту нельзя использовать - НЕ блокируем клики, возвращаем False
                    return False
                
                # Проверяем требует ли карта цель
                card_name = card.__class__.__name__
                
                # Карты которые не требуют цели - используем сразу
                if card_name in ['DoubleMove', 'FogOfWar', 'TrollCard']:
                    success, message = m.CardSystem.use_card(
                        self.current_player,
                        hovered_card,
                        self._get_game_state(m),
                        None
                    )
                    print(f"{'✅' if success else '❌'} {message}")
                    # Сбрасываем выбор после использования
                    self.selected_card = None
                    self.card_target_mode = None
                    if hasattr(self, 'card_target_positions'):
                        self.card_target_positions = []
                    m.CardUI.reset_hover()
                    # Возвращаем False чтобы разрешить обычные клики после использования
                    return False
                
                # Карты требующие цель - переходим в режим выбора
                elif card_name in ['KnightSwap']:
                    self.selected_card = {
                        'index': hovered_card,
                        'card': card,
                        'name': card_name
                    }
                    self.card_target_mode = 'two_cells'
                    self.card_target_positions = []
                    print(f"🎯 Выберите две фигуры для обмена...")
                    # В режиме выбора цели блокируем обычные клики
                    return True
                
                elif card_name in ['HealPiece']:
                    self.selected_card = {
                        'index': hovered_card,
                        'card': card,
                        'name': card_name
                    }
                    self.card_target_mode = 'single_cell'
                    print(f"🎯 Выберите пустую клетку для воскрешения...")
                    # В режиме выбора цели блокируем обычные клики
                    return True
                
                elif card_name in ['TimeRewind']:
                    # TimeRewind пока используем без цели
                    success, message = m.CardSystem.use_card(
                        self.current_player,
                        hovered_card,
                        self._get_game_state(m),
                        None
                    )
                    print(f"{'✅' if success else '❌'} {message}")
                    # Сбрасываем выбор после использования
                    self.selected_card = None
                    self.card_target_mode = None
                    if hasattr(self, 'card_target_positions'):
                        self.card_target_positions = []
                    m.CardUI.reset_hover()
                    # Возвращаем False чтобы разрешить обычные клики
                    return False
                
                # Если карта неизвестного типа - не блокируем
                else:
                    print(f"⚠️ Неизвестный тип карты: {card_name}")
                    return False
            
            # Если кликнули по карте, но она не была обработана - не блокируем
            return False
        
        # Если не кликнули ни по карте, ни в режиме выбора - разрешаем обычные клики
        return False
    
    def find_king(self, team):
        """Находит позицию короля указанной команды"""
        for x in range(8):
            for y in range(8):
                if self.cells[x][y]['value'] == f"{team}_king":
                    return (x, y)
        return None
    
    def is_in_check(self, team):
        """Проверяет, находится ли король указанной команды под шахом"""
        king_pos = self.find_king(team)
        if not king_pos:
            return False
        
        king_x, king_y = king_pos
        enemy_team = "black" if team == "white" else "white"
        
        # Проверяем, может ли любая вражеская фигура атаковать короля
        for x in range(8):
            for y in range(8):
                piece = self.cells[x][y]['value']
                if piece != "empty" and piece[:5] == enemy_team:
                    if self.can_piece_attack(x, y, king_x, king_y, piece):
                        return True
        return False
    
    def can_piece_attack(self, from_x, from_y, to_x, to_y, piece):
        """Проверяет, может ли фигура атаковать указанную позицию"""
        piece_type = piece[6:]
        team = piece[:5]
        
        # Временно сохраняем состояние клеток
        original_statuses = {}
        for x in range(8):
            for y in range(8):
                original_statuses[(x, y)] = self.cells[x][y]['status']
                self.cells[x][y]['status'] = None
                
        # Устанавливаем контекст игры для проверки ходов
        self.PM.game = self
        
        # Проверяем возможные ходы фигуры
        if piece_type == "pawn":
            self.PM.pawn(None, from_x, from_y, team)
        elif piece_type == "rook":
            self.PM.rook(None, from_x, from_y, team)
        elif piece_type == "bishop":
            self.PM.bishop(None, from_x, from_y, team)
        elif piece_type == "knight":
            self.PM.knight(None, from_x, from_y, team)
        elif piece_type == "queen":
            self.PM.queen(None, from_x, from_y, team)
        elif piece_type == "king":
            self.PM.king(None, from_x, from_y, team)
        
        # Проверяем, может ли фигура атаковать целевую позицию
        can_attack = self.cells[to_x][to_y]['status'] == 'attack'
        
        # Восстанавливаем статусы клеток
        for x in range(8):
            for y in range(8):
                self.cells[x][y]['status'] = original_statuses[(x, y)]
        
        return can_attack
    
    def export_game_state(self, m):
        """Экспортирует текущее состояние игры для чита"""
        try:
            import json
            import os
            
            # Создаем директорию если нет
            export_dir = os.path.join('data', 'cheat_export')
            os.makedirs(export_dir, exist_ok=True)
            
            # Собираем состояние доски
            board_state = []
            for x in range(8):
                row = []
                for y in range(8):
                    row.append(self.cells[x][y]['value'])
                board_state.append(row)
            
            # Формируем данные
            game_state = {
                'board': board_state,
                'current_player': self.current_player,
                'game_started': self.game_started,
                'game_over': self.game_over,
                'winner': self.winner
            }
            
            # Сохраняем в файл
            export_file = os.path.join(export_dir, 'game_state.json')
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(game_state, f)
        except Exception as e:
            # Игнорируем ошибки экспорта чтобы не ломать игру
            pass
    
    def is_point_in_polygon(self,point:tuple,polygon:list) -> bool:
        
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside