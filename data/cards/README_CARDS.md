# 🃏 Создание собственных карт

## Как создать свою карту

### 1. Создайте новый файл
Создайте файл с именем `card_ваше_название.py` в папке `data/cards/`

### 2. Импортируйте базовый класс
```python
from data.cards.base_card import BaseCard
```

### 3. Создайте класс карты
```python
class ВашаКарта(BaseCard):
    def __init__(self):
        super().__init__()
        self.name = "Название карты"
        self.description = "Описание эффекта"
        self.rarity = "rare"  # common, rare, epic, legendary
        self.cooldown = 3  # Кулдаун в ходах
        self.icon = "🎴"  # Emoji иконка
        self.color = (255, 100, 100)  # RGB цвет
```

### 4. Реализуйте эффект
```python
    def apply_effect(self, game_state, target=None):
        """
        game_state - словарь с состоянием игры:
            - board: доска 8x8
            - current_player: 'white' или 'black'
            - move_history: история ходов
            - captured_pieces: захваченные фигуры
            
        target - цель карты (зависит от карты):
            - {'pos': (x, y)} - позиция на доске
            - {'pos1': (x1, y1), 'pos2': (x2, y2)} - две позиции
            - None - если цель не нужна
        
        Возвращает:
            (True, "Успешно!") - если эффект применен
            (False, "Причина") - если не удалось
        """
        # Ваш код здесь
        return True, "Эффект применен!"
```

## Примеры карт

### Простая карта без цели
```python
from data.cards.base_card import BaseCard

class SkipTurn(BaseCard):
    def __init__(self):
        super().__init__()
        self.name = "Пропуск хода"
        self.description = "Противник пропускает следующий ход"
        self.rarity = "common"
        self.cooldown = 2
        self.icon = "⏭️"
        self.color = (150, 150, 150)
    
    def apply_effect(self, game_state, target=None):
        game_state['skip_next_turn'] = True
        return True, "Противник пропустит ход!"
```

### Карта с выбором позиции
```python
from data.cards.base_card import BaseCard

class Teleport(BaseCard):
    def __init__(self):
        super().__init__()
        self.name = "Телепортация"
        self.description = "Переместите фигуру в любое место"
        self.rarity = "epic"
        self.cooldown = 4
        self.icon = "✨"
        self.color = (200, 100, 255)
    
    def can_use(self, game_state):
        # Дополнительная проверка
        base_check, reason = super().can_use(game_state)
        if not base_check:
            return False, reason
        
        # Ваши проверки
        return True, ""
    
    def apply_effect(self, game_state, target=None):
        if not target or 'from' not in target or 'to' not in target:
            return False, "Выберите фигуру и место назначения"
        
        board = game_state['board']
        from_pos = target['from']
        to_pos = target['to']
        
        # Перемещаем фигуру
        piece = board[from_pos[1]][from_pos[0]]
        board[to_pos[1]][to_pos[0]] = piece
        board[from_pos[1]][from_pos[0]] = None
        
        return True, "Фигура телепортирована!"
```

### Карта с длительным эффектом
```python
from data.cards.base_card import BaseCard

class Shield(BaseCard):
    def __init__(self):
        super().__init__()
        self.name = "Щит"
        self.description = "Защищает от захвата на 2 хода"
        self.rarity = "rare"
        self.cooldown = 5
        self.icon = "🛡️"
        self.color = (100, 200, 255)
        self.duration = 0
    
    def apply_effect(self, game_state, target=None):
        self.duration = 2
        game_state['shield_active'] = True
        return True, "Щит активирован!"
    
    def on_turn_end(self, game_state):
        if self.duration > 0:
            self.duration -= 1
            if self.duration == 0:
                game_state['shield_active'] = False
    
    def serialize(self):
        data = super().serialize()
        data['duration'] = self.duration
        return data
    
    def deserialize(self, data):
        super().deserialize(data)
        self.duration = data.get('duration', 0)
```

## Редкости карт

- **common** (50% шанс): Простые эффекты
- **rare** (25% шанс): Средние эффекты
- **epic** (15% шанс): Мощные эффекты
- **legendary** (10% шанс): Уникальные эффекты

## Полезные поля game_state

```python
game_state = {
    'board': [],              # Доска 8x8
    'current_player': 'white', # Текущий игрок
    'move_history': [],       # История ходов
    'captured_pieces': {      # Захваченные фигуры
        'white': [],
        'black': []
    },
    'extra_move': False,      # Дополнительный ход
    'fog_active': False,      # Туман войны
    # Добавляйте свои поля!
}
```

## Методы базового класса

### `can_use(game_state)` 
Проверяет можно ли использовать карту

### `use(game_state, target)` 
Использует карту (вызывает apply_effect)

### `apply_effect(game_state, target)` 
**Переопределите этот метод!** Применяет эффект карты

### `on_turn_start(game_state)` 
Вызывается в начале хода владельца

### `on_turn_end(game_state)` 
Вызывается в конце хода владельца

### `get_info()` 
Возвращает информацию о карте для UI

### `serialize() / deserialize()` 
Для сохранения/загрузки состояния

## Тестирование

1. Создайте файл карты в `data/cards/`
2. Запустите игру
3. Карта автоматически загрузится
4. Смотрите консоль для сообщений о загрузке

## Советы

✅ Всегда проверяйте валидность данных в `can_use()`  
✅ Возвращайте понятные сообщения об ошибках  
✅ Используйте `serialize()/deserialize()` для карт с состоянием  
✅ Тестируйте карты в разных ситуациях  
✅ Используйте emoji иконки для красоты  

❌ Не изменяйте `base_card.py`  
❌ Не используйте одинаковые имена классов  
❌ Не создавайте слишком мощные карты  

## Примеры в проекте

Посмотрите на существующие карты для вдохновения:
- `card_knight_swap.py` - обмен фигур
- `card_time_rewind.py` - отмена хода
- `card_fog_of_war.py` - туман войны
- `card_double_move.py` - двойной ход
- `card_heal_piece.py` - воскрешение

Удачи в создании карт! 🎴✨

