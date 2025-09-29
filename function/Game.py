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
        self.game_started = False  # Флаг начала игры

        # Анимации
        self.anim_move = None  # {'from':(x,y),'to':(x,y),'piece':str,'start':ms,'dur':ms,'is_attack':bool}
    
    def main(self,m):

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
        
        # Обычные клавиши управления камерой
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
    
    def mouse_input(self,m):
        
        if self.game_over:
            return

        # Блокируем ввод на время анимации перемещения
        if self.anim_move is not None:
            return

        if m.PI.MI.mouse_click['lt']:
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
            
            # Проверяем, съедается ли король
            if captured_piece.endswith('_king'):
                # Игра окончена - король съеден!
                winner = self.current_player
                self.game_over = True
                self.winner = winner
                print(f"🎉 ИГРА ОКОНЧЕНА! {winner.upper()} ПОБЕДИЛ!")
        
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
            self.switch_player()
            self.clear_all_statuses()
    
    def switch_player(self):
        """Переключает текущего игрока"""
        self.current_player = "black" if self.current_player == "white" else "white"
    
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