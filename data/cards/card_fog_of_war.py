"""
Карта: Туман войны
Скрывает фигуры противника на 2 хода
"""

from data.cards.base_card import BaseCard

class FogOfWar(BaseCard):
    def __init__(self):
        super().__init__()
        self.name = "Туман войны"
        self.description = "Скрыть фигуры противника на 2 хода"
        self.rarity = "epic"
        self.cooldown = 4
        self.icon = "🌫️"
        self.color = (150, 150, 150)
        self.duration = 0  # Счетчик оставшихся ходов эффекта
    
    def apply_effect(self, game_state, target=None):
        self.duration = 2
        # Устанавливаем флаг в объекте игры
        game = game_state.get('game')
        if game:
            game.fog_of_war_active = True
            game.fog_of_war_owner = game_state.get('current_player')
            game.fog_of_war_duration = 2
            print(f"🌫️ Туман войны активирован!")
        
        return True, "Фигуры противника скрыты на 2 хода!"
    
    def on_turn_end(self, game_state):
        if self.duration > 0:
            self.duration -= 1
            if self.duration == 0:
                game_state['fog_active'] = False
    
    def serialize(self):
        data = super().serialize()
        data['duration'] = self.duration
        return data
    
    def deserialize(self, data):
        super().deserialize(data)
        self.duration = data.get('duration', 0)

