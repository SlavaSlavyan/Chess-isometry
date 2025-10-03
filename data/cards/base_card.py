"""
Базовый класс для всех карт.
Все моды должны наследоваться от этого класса.
"""

class BaseCard:
    """
    Базовый класс карты.
    
    Атрибуты:
        name: Название карты
        description: Описание эффекта
        rarity: Редкость ('common', 'rare', 'epic', 'legendary')
        cost: Стоимость использования (опционально)
        cooldown: Кулдаун в ходах (0 = можно использовать сразу)
        icon: Путь к иконке или emoji
        color: Цвет карты (R, G, B)
    """
    
    def __init__(self):
        self.name = "Base Card"
        self.description = "Base card description"
        self.rarity = "common"
        self.cost = 0
        self.cooldown = 0
        self.current_cooldown = 0
        self.icon = "🃏"
        self.color = (200, 200, 200)
        self.enabled = True  # Можно ли использовать карту
    
    def can_use(self, game_state):
        """
        Проверяет, можно ли использовать карту в текущем состоянии игры.
        
        Args:
            game_state: Объект с состоянием игры (доска, ход и т.д.)
        
        Returns:
            (bool, str): (можно ли использовать, причина если нельзя)
        """
        if not self.enabled:
            return False, "Карта отключена"
        
        if self.current_cooldown > 0:
            return False, f"Кулдаун: {self.current_cooldown} ходов"
        
        return True, ""
    
    def use(self, game_state, target=None):
        """
        Использует карту.
        
        Args:
            game_state: Объект с состоянием игры
            target: Цель карты (позиция, фигура и т.д.)
        
        Returns:
            (bool, str): (успешно ли применена, сообщение о результате)
        """
        can, reason = self.can_use(game_state)
        if not can:
            return False, reason
        
        # Применяем эффект карты (переопределяется в наследниках)
        success, message = self.apply_effect(game_state, target)
        
        if success:
            self.current_cooldown = self.cooldown
        
        return success, message
    
    def apply_effect(self, game_state, target=None):
        """
        Применяет эффект карты. ДОЛЖЕН быть переопределен в наследниках.
        
        Args:
            game_state: Объект с состоянием игры
            target: Цель карты
        
        Returns:
            (bool, str): (успешно ли применен эффект, описание результата)
        """
        return False, "Базовая карта не имеет эффекта"
    
    def on_turn_start(self, game_state):
        """Вызывается в начале хода владельца карты"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def on_turn_end(self, game_state):
        """Вызывается в конце хода владельца карты"""
        pass
    
    def get_info(self):
        """Возвращает полную информацию о карте для UI"""
        return {
            'name': self.name,
            'description': self.description,
            'rarity': self.rarity,
            'cost': self.cost,
            'cooldown': self.cooldown,
            'current_cooldown': self.current_cooldown,
            'icon': self.icon,
            'color': self.color,
            'enabled': self.enabled
        }
    
    def serialize(self):
        """Сериализует карту для сохранения/передачи по сети"""
        return {
            'class': self.__class__.__name__,
            'current_cooldown': self.current_cooldown,
            'enabled': self.enabled
        }
    
    def deserialize(self, data):
        """Восстанавливает состояние карты"""
        self.current_cooldown = data.get('current_cooldown', 0)
        self.enabled = data.get('enabled', True)

