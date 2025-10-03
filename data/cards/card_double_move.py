"""
Карта: Двойной ход
Позволяет сделать два хода подряд
"""

from data.cards.base_card import BaseCard

class DoubleMove(BaseCard):
    def __init__(self):
        super().__init__()
        self.name = "Двойной ход"
        self.description = "Сделайте два хода подряд"
        self.rarity = "epic"
        self.cooldown = 6
        self.icon = "⚡"
        self.color = (255, 200, 50)
    
    def apply_effect(self, game_state, target=None):
        # Устанавливаем флаг в объекте игры
        game = game_state.get('game')
        if game:
            game.extra_move_active = True
            game.extra_move_player = game_state.get('current_player')
            print(f"⚡ Двойной ход активирован для {game.extra_move_player}!")
        
        return True, "Сделайте дополнительный ход!"

