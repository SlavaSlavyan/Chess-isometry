import random
import math

class SplashManager:
    
    def __init__(self, m):
        self.splashes = []
        self.current_splash = ""
        self.splash_angle = 0.0
        self.splash_scale = 1.0
        self.splash_alpha = 255
        
        self.load_splashes(m)
        self.pick_random_splash()
    
    def load_splashes(self, m):
        """Загружает список splash-текстов"""
        try:
            splash_data = m.JsonManager.load("data/splashes")
            self.splashes = splash_data.get("splashes", [])
            print(f"Загружено {len(self.splashes)} splash-текстов")
        except:
            # Запасные splash-тексты на случай ошибки
            self.splashes = [
                "Изометрические шахматы!",
                "Королевская игра!",
                "Мат в три хода!",
                "Шах и мат!"
            ]
            print("Использованы запасные splash-тексты")
    
    def pick_random_splash(self):
        """Выбирает случайный splash-текст"""
        if self.splashes:
            self.current_splash = random.choice(self.splashes)
        else:
            self.current_splash = "Chess Isometry!"
    
    def update_animation(self, pulse_time):
        """Обновляет анимацию splash-текста"""
        # Базовый угол как в Minecraft (слегка наклонён) + лёгкое покачивание
        base_angle = -20.0  # Основной наклон
        wobble = math.sin(pulse_time * 0.8) * 2.0  # Лёгкое покачивание
        self.splash_angle = base_angle + wobble
        
        # Пульсация размера
        self.splash_scale = 1.0 + math.sin(pulse_time * 1.2) * 0.03
        
        # Мерцание альфы (более стабильное)
        self.splash_alpha = int(255 * (0.85 + 0.15 * math.sin(pulse_time * 1.5)))
    
    def get_current_splash(self):
        """Возвращает текущий splash-текст"""
        return self.current_splash
    
    def get_animation_params(self):
        """Возвращает параметры анимации"""
        return {
            'angle': self.splash_angle,
            'scale': self.splash_scale,
            'alpha': self.splash_alpha
        }
    
    def refresh_splash(self):
        """Выбирает новый случайный splash-текст"""
        self.pick_random_splash()
