"""
Тролльская карта - показывает рофельную гифку противнику
"""

from data.cards.base_card import BaseCard
import pygame
import os

class TrollCard(BaseCard):
    """Рофельная карта - троллит противника"""
    
    # Статические переменные класса - загружаем GIF только один раз!
    _gif_frames_loaded = False
    _gif_frames = []
    _frame_delay = 80  # мс между кадрами (увеличено для производительности)
    
    def __init__(self):
        super().__init__()
        self.name = "Ротаут"
        self.description = "Показать противнику 'сюрприз' на весь экран"
        self.icon = "🤡"
        self.rarity = "epic"
        self.cooldown = 0
        self.color = (255, 100, 150)
        
        # Загружаем GIF только один раз для всех экземпляров
        if not TrollCard._gif_frames_loaded:
            TrollCard.load_gif_static()
            TrollCard._gif_frames_loaded = True
        
        self.gif_frames = TrollCard._gif_frames
        self.frame_delay = TrollCard._frame_delay
    
    @classmethod
    def load_gif_static(cls):
        """Загружает GIF анимацию (один раз для всего класса)"""
        try:
            # Пытаемся загрузить GIF
            gif_path = 'data/troll.gif'
            
            if os.path.exists(gif_path):
                # Pygame не поддерживает GIF напрямую, используем PIL
                try:
                    from PIL import Image
                    
                    gif = Image.open(gif_path)
                    
                    # Извлекаем кадры с пропуском для оптимизации (каждый 2-й кадр)
                    frame_count = 0
                    loaded_count = 0
                    while True:
                        try:
                            gif.seek(frame_count)
                            
                            # Пропускаем каждый второй кадр для производительности
                            if frame_count % 2 == 0:
                                # Конвертируем в RGB (быстрее чем RGBA)
                                frame = gif.convert('RGB')
                                size = frame.size
                                
                                # Уменьшаем размер если очень большой
                                max_size = 800
                                if size[0] > max_size or size[1] > max_size:
                                    ratio = min(max_size / size[0], max_size / size[1])
                                    new_size = (int(size[0] * ratio), int(size[1] * ratio))
                                    frame = frame.resize(new_size, Image.Resampling.LANCZOS)
                                    size = new_size
                                
                                mode = frame.mode
                                data = frame.tobytes()
                                
                                pygame_surface = pygame.image.fromstring(data, size, mode)
                                cls._gif_frames.append(pygame_surface)
                                loaded_count += 1
                            
                            frame_count += 1
                        except EOFError:
                            break
                    
                    if loaded_count > 0:
                        print(f"🎬 [TrollCard] Загружено {loaded_count} кадров GIF (оптимизировано)")
                    else:
                        cls.use_fallback_static()
                        
                except ImportError:
                    print("⚠️ [TrollCard] PIL не установлен, используем fallback")
                    cls.use_fallback_static()
                except Exception as e:
                    print(f"⚠️ [TrollCard] Ошибка загрузки GIF: {e}")
                    cls.use_fallback_static()
            else:
                print(f"⚠️ [TrollCard] Файл {gif_path} не найден, используем fallback")
                cls.use_fallback_static()
                
        except Exception as e:
            print(f"⚠️ [TrollCard] Критическая ошибка: {e}")
            cls.use_fallback_static()
    
    @classmethod
    def use_fallback_static(cls):
        """Использует fallback анимацию если GIF не загрузился"""
        # Создаем простую лёгкую анимацию
        font = pygame.font.Font(None, 150)
        
        frames = ["TROLLED!", "🤡", "GG", "😂"]
        colors = [
            (255, 50, 50),
            (255, 150, 0),
            (50, 255, 50),
            (255, 200, 0)
        ]
        
        for text_content, color in zip(frames, colors):
            surface = pygame.Surface((600, 400))
            surface.fill((0, 0, 0))
            
            try:
                text = font.render(text_content, True, color)
            except:
                text = font.render("TROLLED!", True, color)
            
            text_rect = text.get_rect(center=(300, 200))
            surface.blit(text, text_rect)
            
            cls._gif_frames.append(surface)
        
        print("🎪 [TrollCard] Используется fallback анимация")
    
    def can_use(self, game_state):
        """Карта всегда доступна"""
        return True, ""
    
    def apply_effect(self, game_state, target=None):
        """Активирует эффект троллинга"""
        game = game_state.get('game')
        
        if not game:
            return False, "Игра не найдена"
        
        # Определяем кого троллим
        current_player = game_state.get('current_player', 'white')
        opponent = 'black' if current_player == 'white' else 'white'
        
        # Получаем размер экрана и предварительно масштабируем все кадры
        m = game_state.get('m')
        if m:
            screen_width = m.Disp.width
            screen_height = m.Disp.height
            
            # Кэшируем масштабированные кадры
            if not hasattr(game, 'troll_scaled_frames') or game.troll_scaled_size != (screen_width, screen_height):
                game.troll_scaled_frames = []
                for frame in self.gif_frames:
                    scaled = pygame.transform.scale(frame, (screen_width, screen_height))
                    game.troll_scaled_frames.append(scaled)
                game.troll_scaled_size = (screen_width, screen_height)
                print(f"🎬 [TrollCard] Предварительно масштабировано {len(game.troll_scaled_frames)} кадров")
        
        # Устанавливаем флаг активного эффекта
        game.troll_effect_active = True
        game.troll_effect_target = opponent
        game.troll_effect_frames = game.troll_scaled_frames if hasattr(game, 'troll_scaled_frames') else self.gif_frames
        game.troll_effect_duration = 5000  # 5 секунд
        game.troll_effect_start_time = pygame.time.get_ticks()
        game.troll_effect_current_frame = 0
        game.troll_effect_last_frame_time = pygame.time.get_ticks()
        game.troll_effect_frame_delay = self.frame_delay
        
        try:
            print(f"🤡 Противник ({opponent}) получил РОТАЦИЮ!")
        except:
            print(f"[TROLL] Противник ({opponent}) получил эффект!")
        
        return True, "Противник был успешно заротан! 🤡"
    
    def on_turn_start(self, game_state):
        """Вызывается в начале каждого хода"""
        pass
    
    def on_turn_end(self, game_state):
        """Вызывается в конце каждого хода"""
        pass

