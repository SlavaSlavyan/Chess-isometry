"""
Синхронизация состояния игры между 2D pygame и 3D Panda3D режимами
Эффективная реализация с проверкой timestamp
"""

import json
import os
import time

class GameStateSync:
    def __init__(self):
        self.state_file = 'data/game_state.json'
        self.last_check_time = 0
        self.check_interval = 0.1  # Проверка раз в 0.1 секунды (быстрее для мультиплеера)
        self.last_modified = 0
        self.cached_state = None
        self.last_turn = None  # Отслеживание смены хода
        
    def should_check(self):
        """Проверяет, нужно ли читать файл (по времени)"""
        current_time = time.time()
        if current_time - self.last_check_time >= self.check_interval:
            self.last_check_time = current_time
            return True
        return False
    
    def has_changed(self):
        """Проверяет, изменился ли файл с последнего чтения"""
        if not os.path.exists(self.state_file):
            return False
        
        try:
            modified = os.path.getmtime(self.state_file)
            if modified > self.last_modified:
                self.last_modified = modified
                return True
        except:
            pass
        return False
    
    def load_state(self):
        """Загружает состояние из файла (только если изменилось)"""
        if not self.should_check():
            return self.cached_state
        
        if not self.has_changed():
            return self.cached_state
        
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                self.cached_state = json.load(f)
                
                # Отслеживаем смену хода для уведомления
                current_turn = self.cached_state.get('current_turn')
                if self.last_turn != current_turn:
                    self.last_turn = current_turn
                    # Печатаем уведомление о ходе противника
                    if current_turn:
                        print(f"🔄 [SYNC] Ход противника! Теперь ходит: {current_turn}")
                
                return self.cached_state
        except Exception as e:
            print(f"Failed to load game state: {e}")
            return None
    
    def has_turn_changed(self, new_turn):
        """Проверяет, изменился ли текущий ход"""
        if self.last_turn != new_turn:
            self.last_turn = new_turn
            return True
        return False
    
    def save_state_from_2d(self, game):
        """Сохраняет состояние из 2D pygame игры"""
        try:
            # Конвертируем cells в простой формат
            board = {}
            for x in range(8):
                for y in range(8):
                    value = game.cells[x][y]['value']
                    if value != 'empty':
                        board[f'{x},{y}'] = value
            
            state = {
                'board': board,
                'current_turn': game.current_player,
                'camera_pos': None,  # В 2D режиме нет камеры
                'camera_heading': None,
                'camera_pitch': None,
                'last_update': time.time(),
                'mode': '2d'
            }
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save game state: {e}")
    
    def apply_state_to_2d(self, game, state):
        """Применяет загруженное состояние к 2D игре"""
        if not state or 'board' not in state:
            return False
        
        try:
            # Очищаем доску
            for x in range(8):
                for y in range(8):
                    game.cells[x][y]['value'] = 'empty'
            
            # Восстанавливаем фигуры
            for pos_str, piece in state['board'].items():
                x, y = map(int, pos_str.split(','))
                if 0 <= x < 8 and 0 <= y < 8:
                    game.cells[x][y]['value'] = piece
            
            # Обновляем текущего игрока
            if 'current_turn' in state:
                game.current_player = state['current_turn']
            
            return True
            
        except Exception as e:
            print(f"Failed to apply game state: {e}")
            return False
    
    def get_fps_player_position(self):
        """Возвращает позицию FPS игрока для отрисовки в 2D"""
        if not self.cached_state:
            return None
        
        camera_pos = self.cached_state.get('camera_pos')
        if camera_pos and len(camera_pos) >= 2:
            # Возвращаем точные координаты камеры (не округляем до клеток)
            x = camera_pos[0]
            y = camera_pos[1]
            z = camera_pos[2] if len(camera_pos) > 2 else 1.7
            return (x, y, z)
        
        return None

