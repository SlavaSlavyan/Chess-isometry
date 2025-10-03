"""
Карта: Воскрешение
Возвращает последнюю захваченную фигуру на доску
"""

from data.cards.base_card import BaseCard

class HealPiece(BaseCard):
    def __init__(self):
        super().__init__()
        self.name = "Воскрешение"
        self.description = "Верните последнюю захваченную фигуру"
        self.rarity = "rare"
        self.cooldown = 4
        self.icon = "💚"
        self.color = (50, 200, 50)
    
    def can_use(self, game_state):
        base_check, reason = super().can_use(game_state)
        if not base_check:
            return False, reason
        
        # Проверяем что есть свободные клетки
        board = game_state.get('board')
        free_cells = 0
        for y in range(8):
            for x in range(8):
                if board[y][x]['value'] == 'empty':
                    free_cells += 1
        
        if free_cells == 0:
            return False, "Нет свободных клеток на доске"
        
        return True, ""
    
    def apply_effect(self, game_state, target=None):
        """
        target должен быть позицией для размещения: {'pos': (x, y)}
        Пока просто ставит пешку текущего игрока на выбранную клетку
        """
        if not target or 'pos' not in target:
            return False, "Выберите клетку для воскрешения"
        
        pos = target['pos']
        board = game_state.get('board')
        current_player = game_state.get('current_player')
        
        # Проверяем что клетка свободна
        cell = board[pos[1]][pos[0]]
        if cell['value'] != 'empty':
            return False, "Клетка занята"
        
        # Ставим пешку текущего игрока (упрощенная версия)
        cell['value'] = f'{current_player}_pawn'
        
        print(f"💚 Воскрешена пешка {current_player} на позиции {pos}")
        
        return True, f"Пешка воскрешена!"

