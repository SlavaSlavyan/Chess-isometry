import pygame
import json
import os
import hashlib
from typing import Dict, Optional

class PlayerProfile:
    """Система профилей игроков для мультиплеера"""
    
    def __init__(self):
        self.profile_file = "data/player_profile.json"
        self.avatars_path = "data/avatars/"
        
        # Данные профиля
        self.nickname = "Player"
        self.avatar_hash = None
        self.stats = {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0,
            "games_draw": 0
        }
        
        # Аватар по умолчанию (генерируется процедурно)
        self.default_avatar_size = 64
        self.avatar_surface = None
        
        # Убеждаемся, что директория для аватаров существует
        try:
            os.makedirs(self.avatars_path, exist_ok=True)
        except Exception:
            pass

        # Загружаем профиль
        self.load_profile()

        # Пытаемся загрузить сохранённый кастомный аватар, иначе генерируем дефолтный
        if not self._load_avatar_from_disk():
            self.generate_default_avatar()
    
    def load_profile(self):
        """Загружает профиль из файла"""
        try:
            if os.path.exists(self.profile_file):
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.nickname = data.get('nickname', 'Player')
                    self.avatar_hash = data.get('avatar_hash', None)
                    self.stats = data.get('stats', self.stats)
                    print(f"✅ Профиль загружен: {self.nickname}")
            else:
                print("📁 Создается новый профиль")
                self.save_profile()
        except Exception as e:
            print(f"❌ Ошибка загрузки профиля: {e}")
    
    def save_profile(self):
        """Сохраняет профиль в файл"""
        try:
            # Создаем директорию если не существует
            os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)
            
            data = {
                'nickname': self.nickname,
                'avatar_hash': self.avatar_hash,
                'stats': self.stats
            }
            
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print(f"💾 Профиль сохранен: {self.nickname}")
        except Exception as e:
            print(f"❌ Ошибка сохранения профиля: {e}")

    def _avatar_file_path(self) -> str:
        """Возвращает путь к файлу с аватаром по его хэшу."""
        if not self.avatar_hash:
            return None
        return os.path.join(self.avatars_path, f"{self.avatar_hash}.png")

    def _save_avatar_to_disk(self):
        """Сохраняет текущий аватар на диск (data/avatars/<hash>.png)."""
        try:
            if not self.avatar_surface or not self.avatar_hash:
                return False
            os.makedirs(self.avatars_path, exist_ok=True)
            path = self._avatar_file_path()
            pygame.image.save(self.avatar_surface, path)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения файла аватара: {e}")
            return False

    def _load_avatar_from_disk(self) -> bool:
        """Пытается загрузить сохранённый аватар с диска по avatar_hash."""
        try:
            path = self._avatar_file_path()
            if path and os.path.exists(path):
                image = pygame.image.load(path).convert_alpha()
                # Подстраховка: приводим к нужному размеру
                image = pygame.transform.smoothscale(image, (self.default_avatar_size, self.default_avatar_size))
                self.avatar_surface = image
                return True
        except Exception as e:
            print(f"❌ Ошибка загрузки файла аватара: {e}")
        return False
    
    def set_nickname(self, nickname: str):
        """Устанавливает никнейм"""
        if len(nickname.strip()) > 0 and len(nickname) <= 20:
            self.nickname = nickname.strip()
            self.save_profile()
            return True
        return False
    
    def generate_default_avatar(self):
        """Генерирует аватар по умолчанию на основе никнейма"""
        # Создаем хэш из никнейма для получения уникального цвета
        hash_obj = hashlib.md5(self.nickname.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Извлекаем цвета из хэша
        r = int(hash_hex[0:2], 16)
        g = int(hash_hex[2:4], 16) 
        b = int(hash_hex[4:6], 16)
        
        # Делаем цвета более яркими и контрастными
        r = min(255, r + 100)
        g = min(255, g + 100)
        b = min(255, b + 100)
        
        size = self.default_avatar_size
        self.avatar_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Фон (круг)
        pygame.draw.circle(self.avatar_surface, (r, g, b), (size//2, size//2), size//2)
        
        # Темная обводка
        pygame.draw.circle(self.avatar_surface, (50, 50, 50), (size//2, size//2), size//2, 3)
        
        # Инициалы (первые 1-2 буквы никнейма)
        initials = self.get_initials()
        
        # Шрифт для инициалов
        font_size = size // 3
        try:
            font = pygame.font.Font("data/font/text.ttf", font_size)
        except:
            font = pygame.font.Font(None, font_size)
        
        # Рендерим инициалы
        text_surface = font.render(initials, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(size//2, size//2))
        self.avatar_surface.blit(text_surface, text_rect)
    
    def get_initials(self) -> str:
        """Получает инициалы из никнейма"""
        words = self.nickname.upper().split()
        if len(words) >= 2:
            return words[0][0] + words[1][0]
        elif len(words) == 1 and len(words[0]) >= 2:
            return words[0][:2]
        elif len(words) == 1:
            return words[0][0]
        else:
            return "?"
    
    def get_avatar_surface(self) -> pygame.Surface:
        """Возвращает поверхность с аватаром"""
        if self.avatar_surface is None:
            # Попробуем подхватить сохранённый файл, если есть хэш
            if not self._load_avatar_from_disk():
                self.generate_default_avatar()
        return self.avatar_surface
    
    def update_stats(self, result: str):
        """Обновляет статистику игрока"""
        self.stats["games_played"] += 1
        
        if result == "win":
            self.stats["games_won"] += 1
        elif result == "lose":
            self.stats["games_lost"] += 1
        elif result == "draw":
            self.stats["games_draw"] += 1
        
        self.save_profile()
    
    def get_win_rate(self) -> float:
        """Возвращает процент побед"""
        if self.stats["games_played"] == 0:
            return 0.0
        return (self.stats["games_won"] / self.stats["games_played"]) * 100
    
    def get_profile_data(self) -> Dict:
        """Возвращает данные профиля для отправки по сети"""
        # Сериализуем аватар в base64 если есть пользовательский
        avatar_data = None
        if self.avatar_surface and self.avatar_hash:
            try:
                import base64
                # Конвертируем поверхность в строку
                avatar_string = pygame.image.tostring(self.avatar_surface, 'RGBA')
                avatar_data = base64.b64encode(avatar_string).decode('utf-8')
            except:
                avatar_data = None
        
        return {
            'nickname': self.nickname,
            'avatar_hash': self.avatar_hash,
            'avatar_data': avatar_data,
            'avatar_size': self.default_avatar_size,
            'stats': self.stats,
            'win_rate': self.get_win_rate()
        }
    
    def load_custom_avatar(self, image_path: str) -> bool:
        """Загружает пользовательский аватар"""
        try:
            # Загружаем изображение
            image = pygame.image.load(image_path)
            
            # Масштабируем до нужного размера
            image = pygame.transform.scale(image, (self.default_avatar_size, self.default_avatar_size))
            
            # Создаем круглую маску
            mask = pygame.Surface((self.default_avatar_size, self.default_avatar_size), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255), 
                             (self.default_avatar_size//2, self.default_avatar_size//2), 
                             self.default_avatar_size//2)
            
            # Применяем маску
            self.avatar_surface = pygame.Surface((self.default_avatar_size, self.default_avatar_size), pygame.SRCALPHA)
            self.avatar_surface.blit(image, (0, 0))
            self.avatar_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
            
            # Добавляем обводку
            pygame.draw.circle(self.avatar_surface, (50, 50, 50), 
                             (self.default_avatar_size//2, self.default_avatar_size//2), 
                             self.default_avatar_size//2, 3)
            
            # Создаем хэш для аватара
            self.avatar_hash = hashlib.md5(pygame.image.tostring(self.avatar_surface, 'RGBA')).hexdigest()
            # Сохраняем файл аватара и профиль
            self._save_avatar_to_disk()
            self.save_profile()
            
            print(f"🎨 Аватар загружен: {image_path}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка загрузки аватара: {e}")
            return False
    
    def load_avatar_from_data(self, avatar_data: str, avatar_hash: str) -> bool:
        """Загружает аватар из base64 данных"""
        try:
            import base64
            
            # Декодируем base64
            avatar_bytes = base64.b64decode(avatar_data.encode('utf-8'))
            
            # Создаем поверхность из данных
            temp_surface = pygame.image.fromstring(avatar_bytes, (self.default_avatar_size, self.default_avatar_size), 'RGBA')
            
            # Создаем финальную поверхность с круглой маской
            self.avatar_surface = pygame.Surface((self.default_avatar_size, self.default_avatar_size), pygame.SRCALPHA)
            
            # Создаем круглую маску
            mask = pygame.Surface((self.default_avatar_size, self.default_avatar_size), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255), 
                             (self.default_avatar_size//2, self.default_avatar_size//2), 
                             self.default_avatar_size//2)
            
            # Применяем изображение и маску
            self.avatar_surface.blit(temp_surface, (0, 0))
            self.avatar_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
            
            # Добавляем обводку
            pygame.draw.circle(self.avatar_surface, (50, 50, 50), 
                             (self.default_avatar_size//2, self.default_avatar_size//2), 
                             self.default_avatar_size//2, 3)
            
            # Сохраняем хэш
            self.avatar_hash = avatar_hash
            # Сохраняем файл аватара
            self._save_avatar_to_disk()
            
            print(f"📩 Аватар получен от игрока: {avatar_hash[:8]}...")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка загрузки аватара из данных: {e}")
            return False

# Глобальный кеш аватаров игроков
_avatar_cache = {}

class PlayerAvatarCache:
    """Кеш аватаров других игроков"""
    
    @staticmethod
    def get_avatar(nickname: str, avatar_hash: str, avatar_data: str = None) -> Optional[pygame.Surface]:
        """Получает аватар игрока из кеша или создает новый"""
        cache_key = f"{nickname}_{avatar_hash}"
        
        # Проверяем кеш
        if cache_key in _avatar_cache:
            return _avatar_cache[cache_key]
        
        # Создаем новый аватар
        if avatar_data:
            # Загружаем из данных
            temp_profile = PlayerProfile()
            if temp_profile.load_avatar_from_data(avatar_data, avatar_hash):
                _avatar_cache[cache_key] = temp_profile.avatar_surface
                return temp_profile.avatar_surface
        
        # Создаем процедурный аватар
        temp_profile = PlayerProfile()
        temp_profile.nickname = nickname
        temp_profile.generate_default_avatar()
        _avatar_cache[cache_key] = temp_profile.avatar_surface
        return temp_profile.avatar_surface
    
    @staticmethod
    def clear_cache():
        """Очищает кеш аватаров"""
        global _avatar_cache
        _avatar_cache.clear()
