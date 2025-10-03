"""
Discord Rich Presence интеграция для Chess Isometry
"""
import time
import threading

class DiscordRPC:
    """Управление Discord Rich Presence"""
    
    def __init__(self):
        self.enabled = False
        self.rpc = None
        self.client_id = "1423695898986152027"  # Замените на ваш Application ID из Discord Developer Portal
        self.connected = False
        self.start_time = int(time.time())
        self.current_state = "В главном меню"
        self.current_details = "Изометрические шахматы"
        
        # Попытка импорта pypresence
        try:
            from pypresence import Presence
            self.Presence = Presence
            self.available = True
        except ImportError:
            self.available = False
            print("⚠️ [Discord RPC] pypresence не установлен. Установите через: pip install pypresence")
    
    def connect(self):
        """Подключение к Discord"""
        if not self.available or self.connected:
            return False
        
        try:
            self.rpc = self.Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            self.update_presence()
            print("✅ [Discord RPC] Подключено к Discord")
            return True
        except Exception as e:
            print(f"❌ [Discord RPC] Ошибка подключения: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Отключение от Discord"""
        if self.rpc and self.connected:
            try:
                self.rpc.close()
                self.connected = False
                print("🔌 [Discord RPC] Отключено от Discord")
            except:
                pass
    
    def enable(self):
        """Включение Discord RPC"""
        if not self.available:
            print("❌ [Discord RPC] pypresence не установлен")
            return False
        
        self.enabled = True
        return self.connect()
    
    def disable(self):
        """Выключение Discord RPC"""
        self.enabled = False
        self.disconnect()
    
    def update_presence(self, state=None, details=None, party_size=None, party_max=None):
        """
        Обновление статуса в Discord
        
        Args:
            state: Статус (например "В игре")
            details: Детали (например "Играет за белых")
            party_size: Количество игроков в партии
            party_max: Максимум игроков
        """
        if not self.connected or not self.enabled:
            return
        
        if state:
            self.current_state = state
        if details:
            self.current_details = details
        
        try:
            presence_data = {
                'state': self.current_state,
                'details': self.current_details,
                'start': self.start_time,
                'large_image': 'chess_logo',  # Замените на ключ изображения из Discord Developer Portal
                'large_text': 'Chess Isometry',
                'small_image': 'playing',
                'small_text': 'В игре',
            }
            
            # Добавляем информацию о партии если есть
            if party_size and party_max:
                presence_data['party_size'] = [party_size, party_max]
            
            self.rpc.update(**presence_data)
        except Exception as e:
            print(f"⚠️ [Discord RPC] Ошибка обновления: {e}")
    
    def set_menu(self):
        """Статус: в главном меню"""
        self.update_presence(state="В главном меню", details="Изометрические шахматы")
    
    def set_settings(self):
        """Статус: в настройках"""
        self.update_presence(state="В настройках", details="Настраивает игру")
    
    def set_multiplayer_lobby(self, is_host=False):
        """Статус: в лобби мультиплеера"""
        if is_host:
            self.update_presence(state="В лобби", details="Ждёт подключения игрока", party_size=1, party_max=2)
        else:
            self.update_presence(state="В лобби", details="Подключён к хосту", party_size=2, party_max=2)
    
    def set_in_game(self, player_color="white", opponent_name="Противник"):
        """Статус: в игре"""
        color_ru = "белых" if player_color == "white" else "чёрных"
        self.update_presence(
            state=f"Играет против {opponent_name}",
            details=f"Играет за {color_ru}",
            party_size=2,
            party_max=2
        )
    
    def set_watching(self):
        """Статус: наблюдает за игрой"""
        self.update_presence(state="Наблюдает за игрой", details="Режим наблюдателя")
    
    def reset_timer(self):
        """Сброс таймера (для новой игры)"""
        self.start_time = int(time.time())
        if self.connected:
            self.update_presence()

