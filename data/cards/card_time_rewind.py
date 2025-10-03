"""
Карта: Возврат времени
Отменяет последний ход противника
"""

from data.cards.base_card import BaseCard

class TimeRewind(BaseCard):
    def __init__(self):
        super().__init__()
        self.name = "Возврат времени"
        self.description = "Отменить последний ход противника"
        self.rarity = "legendary"
        self.cooldown = 5
        self.icon = "⏪"
        self.color = (200, 100, 255)
    
    def can_use(self, game_state):
        base_check, reason = super().can_use(game_state)
        if not base_check:
            return False, reason
        
        # Проверяем что есть история ходов
        if not game_state.get('move_history') or len(game_state['move_history']) < 1:
            return False, "Нет ходов для отмены"
        
        return True, ""
    
    def apply_effect(self, game_state, target=None):
        move_history = game_state.get('move_history', [])
        
        if not move_history:
            return False, "История ходов пуста"
        
        # Отменяем последний ход
        last_move = move_history.pop()
        
        # Восстанавливаем доску (это упрощенная версия, нужно будет интегрировать с реальной логикой)
        board = game_state.get('board')
        
        # Возвращаем фигуру на исходную позицию
        from_pos = last_move.get('from')
        to_pos = last_move.get('to')
        captured = last_move.get('captured')
        
        if from_pos and to_pos:
            # Возвращаем фигуру назад
            board[from_pos[1]][from_pos[0]] = board[to_pos[1]][to_pos[0]]
            board[to_pos[1]][to_pos[0]] = captured  # Восстанавливаем захваченную фигуру
        
        return True, "Ход отменен!"

