"""
Система управления картами с поддержкой моддинга.
Автоматически загружает все карты из папки data/cards/
"""

import os
import sys
import importlib.util
import random
from typing import Dict, List, Optional

class CardSystem:
    """
    Менеджер карт с автоматической загрузкой из файлов.
    Поддерживает моддинг - любой файл card_*.py автоматически загружается.
    """
    
    def __init__(self):
        self.available_cards = {}  # Все доступные типы карт {class_name: CardClass}
        self.player_decks = {
            'white': [],  # Карты белого игрока
            'black': []   # Карты черного игрока
        }
        self.card_drop_chance = 0.3  # 30% шанс дропа карты после хода
        self.max_cards_per_player = 5
        
        # Загружаем все карты из папки
        self.load_all_cards()
    
    def get_resource_path(self, relative_path):
        """Получить абсолютный путь к ресурсу (для PyInstaller)"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return relative_path
    
    def load_all_cards(self):
        """Автоматически загружает все карты из data/cards/"""
        cards_dir = self.get_resource_path('data/cards')
        
        if not os.path.exists(cards_dir):
            print(f"[CardSystem] Папка карт не найдена: {cards_dir}")
            return
        
        loaded_count = 0
        
        # Проходим по всем файлам в папке
        for filename in os.listdir(cards_dir):
            if filename.startswith('card_') and filename.endswith('.py'):
                card_name = filename[:-3]  # Убираем .py
                
                try:
                    # Динамически импортируем модуль
                    spec = importlib.util.spec_from_file_location(
                        card_name,
                        os.path.join(cards_dir, filename)
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Ищем класс карты в модуле
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        
                        # Проверяем что это класс и наследник BaseCard
                        if (isinstance(attr, type) and 
                            hasattr(attr, '__bases__') and 
                            attr_name != 'BaseCard'):
                            
                            # Пытаемся создать экземпляр
                            try:
                                from data.cards.base_card import BaseCard
                                if issubclass(attr, BaseCard):
                                    self.available_cards[attr_name] = attr
                                    loaded_count += 1
                                    print(f"[CardSystem] ✓ Загружена карта: {attr_name} из {filename}")
                            except:
                                pass
                
                except Exception as e:
                    print(f"[CardSystem] ✗ Ошибка загрузки {filename}: {e}")
        
        print(f"[CardSystem] Загружено карт: {loaded_count}")
    
    def give_random_card(self, player: str) -> Optional[object]:
        """
        Дает случайную карту игроку.
        
        Args:
            player: 'white' или 'black'
        
        Returns:
            Экземпляр карты или None
        """
        if len(self.player_decks[player]) >= self.max_cards_per_player:
            return None
        
        if not self.available_cards:
            return None
        
        # Выбираем случайный класс карты с учетом редкости
        card_class = self._weighted_random_card()
        
        if card_class:
            card_instance = card_class()
            self.player_decks[player].append(card_instance)
            return card_instance
        
        return None
    
    def _weighted_random_card(self):
        """Выбирает случайную карту с учетом редкости"""
        if not self.available_cards:
            return None
        
        # Веса для редкостей
        rarity_weights = {
            'common': 50,
            'rare': 25,
            'epic': 15,
            'legendary': 10
        }
        
        # Создаем список (класс, вес)
        weighted_cards = []
        for card_class in self.available_cards.values():
            try:
                temp_instance = card_class()
                weight = rarity_weights.get(temp_instance.rarity, 25)
                weighted_cards.append((card_class, weight))
            except:
                continue
        
        if not weighted_cards:
            return None
        
        # Выбираем случайную карту с учетом весов
        total_weight = sum(w for _, w in weighted_cards)
        rand = random.uniform(0, total_weight)
        
        current = 0
        for card_class, weight in weighted_cards:
            current += weight
            if rand <= current:
                return card_class
        
        return weighted_cards[0][0]  # Fallback
    
    def try_drop_card(self, player: str) -> Optional[object]:
        """
        Пытается выдать карту с учетом шанса дропа.
        
        Args:
            player: 'white' или 'black'
        
        Returns:
            Карта если выпала, иначе None
        """
        if random.random() < self.card_drop_chance:
            return self.give_random_card(player)
        return None
    
    def use_card(self, player: str, card_index: int, game_state: dict, target=None) -> tuple:
        """
        Использует карту из колоды игрока.
        
        Args:
            player: 'white' или 'black'
            card_index: Индекс карты в колоде
            game_state: Состояние игры
            target: Цель для карты
        
        Returns:
            (success: bool, message: str)
        """
        deck = self.player_decks.get(player, [])
        
        if card_index < 0 or card_index >= len(deck):
            return False, "Неверный индекс карты"
        
        card = deck[card_index]
        success, message = card.use(game_state, target)
        
        if success:
            # Удаляем карту после использования (одноразовая)
            deck.pop(card_index)
        
        return success, message
    
    def get_player_cards(self, player: str) -> List[object]:
        """Возвращает все карты игрока"""
        return self.player_decks.get(player, [])
    
    def on_turn_start(self, player: str, game_state: dict):
        """Вызывается в начале хода игрока"""
        for card in self.player_decks.get(player, []):
            card.on_turn_start(game_state)
    
    def on_turn_end(self, player: str, game_state: dict):
        """Вызывается в конце хода игрока"""
        for card in self.player_decks.get(player, []):
            card.on_turn_end(game_state)
    
    def serialize(self) -> dict:
        """Сериализует состояние всех карт для сохранения"""
        return {
            'white': [card.serialize() for card in self.player_decks['white']],
            'black': [card.serialize() for card in self.player_decks['black']],
            'drop_chance': self.card_drop_chance,
            'max_cards': self.max_cards_per_player
        }
    
    def deserialize(self, data: dict):
        """Восстанавливает состояние карт"""
        self.card_drop_chance = data.get('drop_chance', 0.3)
        self.max_cards_per_player = data.get('max_cards', 5)
        
        # Восстанавливаем карты игроков
        for player in ['white', 'black']:
            self.player_decks[player] = []
            for card_data in data.get(player, []):
                class_name = card_data.get('class')
                if class_name in self.available_cards:
                    card_class = self.available_cards[class_name]
                    card_instance = card_class()
                    card_instance.deserialize(card_data)
                    self.player_decks[player].append(card_instance)
    
    def reload_cards(self):
        """Перезагружает все карты из файлов (для тестирования модов)"""
        self.available_cards = {}
        self.load_all_cards()
        print("[CardSystem] Карты перезагружены")
    
    def get_card_info_list(self, player: str) -> List[dict]:
        """Возвращает информацию обо всех картах игрока для UI"""
        return [card.get_info() for card in self.player_decks.get(player, [])]

