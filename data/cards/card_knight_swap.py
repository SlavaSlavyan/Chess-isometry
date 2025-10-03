"""
Карта: Рыцарский прыжок
Меняет местами две любые фигуры на доске
"""

from data.cards.base_card import BaseCard

class KnightSwap(BaseCard):
    def __init__(self):
        super().__init__()
        self.name = "Рыцарский прыжок"
        self.description = "Поменяйте местами две любые фигуры"
        self.rarity = "rare"
        self.cooldown = 3
        self.icon = "♞"
        self.color = (100, 150, 255)
    
    def can_use(self, game_state):
        base_check, reason = super().can_use(game_state)
        if not base_check:
            return False, reason
        
        # Проверяем что на доске есть хотя бы 2 фигуры
        pieces_count = 0
        board = game_state.get('board')
        for y in range(8):
            for x in range(8):
                cell = board[y][x]
                if cell.get('value') != 'empty':
                    pieces_count += 1
        
        if pieces_count < 2:
            return False, "Недостаточно фигур на доске"
        
        return True, ""
    
    def apply_effect(self, game_state, target=None):
        """
        target должен быть словарем: {'pos1': (x1, y1), 'pos2': (x2, y2)}
        """
        if not target or 'pos1' not in target or 'pos2' not in target:
            return False, "Выберите две фигуры для обмена"
        
        board = game_state.get('board')
        pos1 = target['pos1']
        pos2 = target['pos2']
        
        # Проверяем что обе позиции валидны
        if not (0 <= pos1[0] < 8 and 0 <= pos1[1] < 8):
            return False, "Неверная первая позиция"
        if not (0 <= pos2[0] < 8 and 0 <= pos2[1] < 8):
            return False, "Неверная вторая позиция"
        
        # Получаем ячейки (board[y][x] автоматически преобразуется в cells[x][y])
        cell1 = board[pos1[1]][pos1[0]]
        cell2 = board[pos2[1]][pos2[0]]
        
        # Меняем местами значения фигур
        value1 = cell1['value']
        value2 = cell2['value']
        
        cell1['value'] = value2
        cell2['value'] = value1
        
        print(f"🔄 Обмен: {pos1} ({value1}) ↔ {pos2} ({value2})")
        
        return True, f"Фигуры поменялись местами!"

