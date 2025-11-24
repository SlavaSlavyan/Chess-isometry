"""
PyGameShaders - Система постобработки для Pygame
Оптимизированные визуальные эффекты без OpenGL
"""

import pygame
import numpy as np
import time
from typing import Tuple, List, Optional

class PyGameShaders:
    """Система шейдеров для постобработки изображений в Pygame"""
    
    def __init__(self, width: int, height: int):
        """
        Инициализация системы шейдеров
        
        Args:
            width: Ширина экрана
            height: Высота экрана
        """
        self.width = width
        self.height = height
        
        # === ПАРАМЕТРЫ ЭФФЕКТОВ ===
        
        # Vignette (виньетка)
        self.vignette_enabled = True
        self.vignette_intensity = 0.5  # 0.0-1.0
        
        # Bloom (свечение)
        self.bloom_enabled = False
        self.bloom_intensity = 0.3  # 0.0-1.0
        self.bloom_threshold = 200  # 0-255
        
        # Color Grading (цветокоррекция)
        self.color_grading_enabled = False
        self.saturation = 1.0  # 0.0-2.0
        self.brightness = 1.0  # 0.5-1.5
        self.contrast = 1.0  # 0.5-1.5
        
        # Chromatic Aberration (хроматическая аберрация)
        self.chromatic_aberration_enabled = False
        self.aberration_amount = 2.0  # 0.0-5.0 пикселей
        
        # Pixelation (пикселизация)
        self.pixelation_enabled = False
        self.pixel_size = 4  # 1-20
        
        # CRT Effect (эффект старого монитора)
        self.crt_enabled = False
        self.scanline_intensity = 0.3  # 0.0-1.0
        self.curve_amount = 0.0  # 0.0-0.1 (пока не реализовано)
        
        # Screen Shake (тряска экрана)
        self.shake_enabled = False
        self.shake_time = 0.0
        self.shake_intensity = 0.0
        self.shake_offset = (0, 0)
        
        # === КЭШИРОВАНИЕ ===
        self._vignette_cache = None
        self._crt_scanlines_cache = None
        self._last_screen_size = (width, height)
        
        # === ПРОИЗВОДИТЕЛЬНОСТЬ ===
        self.performance_mode = False  # Автоматически включается при низком FPS
        self.last_frame_time = 0.0
        self.fps_samples = []
        
        print("🎨 [PyGameShaders] Система инициализирована")
        self._create_vignette_cache()
        self._create_crt_scanlines_cache()
    
    # ============================================================
    # ОСНОВНОЙ МЕТОД РЕНДЕРИНГА
    # ============================================================
    
    def render(self, surface: pygame.Surface) -> pygame.Surface:
        """
        Применяет все включенные эффекты постобработки
        
        Args:
            surface: Исходная поверхность
            
        Returns:
            Обработанная поверхность
        """
        start_time = time.time()
        
        try:
            # Проверка размера экрана
            if surface.get_size() != self._last_screen_size:
                self._on_screen_resize(surface.get_size())
            
            result = surface.copy()
            
            # Применяем эффекты в правильном порядке
            
            # 1. Color Grading (первым, влияет на общую палитру)
            if self.color_grading_enabled:
                result = self._apply_color_grading(result)
            
            # 2. Bloom (работает с яркими областями)
            if self.bloom_enabled and not self.performance_mode:
                result = self._apply_bloom(result)
            
            # 3. Chromatic Aberration (искажение каналов)
            if self.chromatic_aberration_enabled:
                result = self._apply_chromatic_aberration(result)
            
            # 4. Pixelation (стилизация)
            if self.pixelation_enabled:
                result = self._apply_pixelation(result)
            
            # 5. CRT Effect (сканлайны)
            if self.crt_enabled:
                result = self._apply_crt(result)
            
            # 6. Vignette (последним, затемняет края)
            if self.vignette_enabled:
                result = self._apply_vignette(result)
            
            # Обновляем статистику производительности
            frame_time = time.time() - start_time
            self._update_performance_stats(frame_time)
            
            return result
            
        except Exception as e:
            print(f"⚠️ [PyGameShaders] Ошибка рендеринга: {e}")
            return surface
    
    # ============================================================
    # ЭФФЕКТ 1: VIGNETTE (ВИНЬЕТКА)
    # ============================================================
    
    def _create_vignette_cache(self):
        """Создаёт кэш виньетки для быстрого применения"""
        try:
            self._vignette_cache = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            center_x, center_y = self.width // 2, self.height // 2
            max_dist = ((center_x ** 2) + (center_y ** 2)) ** 0.5
            
            for y in range(self.height):
                for x in range(self.width):
                    dx, dy = x - center_x, y - center_y
                    dist = (dx * dx + dy * dy) ** 0.5
                    
                    # Нормализованное расстояние от центра
                    norm_dist = dist / max_dist
                    
                    # Плавное затухание
                    alpha = int(255 * (norm_dist ** 2) * self.vignette_intensity)
                    alpha = min(255, max(0, alpha))
                    
                    self._vignette_cache.set_at((x, y), (0, 0, 0, alpha))
            
            print("✓ [Vignette] Кэш создан")
            
        except Exception as e:
            print(f"⚠️ [Vignette] Ошибка создания кэша: {e}")
            self._vignette_cache = None
    
    def _apply_vignette(self, surface: pygame.Surface) -> pygame.Surface:
        """Применяет эффект виньетки"""
        if self._vignette_cache is None:
            return surface
        
        result = surface.copy()
        result.blit(self._vignette_cache, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return result
    
    # ============================================================
    # ЭФФЕКТ 2: BLOOM (СВЕЧЕНИЕ)
    # ============================================================
    
    def _apply_bloom(self, surface: pygame.Surface) -> pygame.Surface:
        """
        Применяет bloom эффект с оптимизацией через downsampling
        
        Алгоритм:
        1. Выделить яркие пиксели (threshold)
        2. Уменьшить разрешение в 4 раза (для скорости)
        3. Размыть box blur
        4. Увеличить обратно
        5. Добавить к оригиналу с ADD blending
        """
        try:
            w, h = surface.get_size()
            
            # Шаг 1: Извлекаем яркие области
            bright_surface = pygame.Surface((w, h))
            bright_surface.fill((0, 0, 0))
            
            # Используем numpy для быстрого threshold
            arr = pygame.surfarray.array3d(surface)
            
            # Находим яркие пиксели (среднее значение каналов выше порога)
            brightness = np.mean(arr, axis=2)
            mask = brightness > self.bloom_threshold
            
            # Создаём массив с яркими пикселями
            bright_arr = np.zeros_like(arr)
            bright_arr[mask] = arr[mask]
            
            # Конвертируем обратно в surface
            pygame.surfarray.blit_array(bright_surface, bright_arr)
            
            # Шаг 2: Downsampling (1/4 разрешения для скорости)
            small_w, small_h = w // 4, h // 4
            small_surface = pygame.transform.smoothscale(bright_surface, (small_w, small_h))
            
            # Шаг 3: Box blur (несколько проходов)
            blurred = self._box_blur(small_surface, passes=3)
            
            # Шаг 4: Upsampling обратно
            bloom_surface = pygame.transform.smoothscale(blurred, (w, h))
            
            # Шаг 5: Additive blending
            result = surface.copy()
            
            # Применяем интенсивность
            bloom_surface.set_alpha(int(255 * self.bloom_intensity))
            result.blit(bloom_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            
            return result
            
        except Exception as e:
            print(f"⚠️ [Bloom] Ошибка: {e}")
            return surface
    
    def _box_blur(self, surface: pygame.Surface, passes: int = 1) -> pygame.Surface:
        """Простое размытие методом box blur"""
        result = surface.copy()
        
        for _ in range(passes):
            w, h = result.get_size()
            arr = pygame.surfarray.array3d(result)
            
            # Простой 3x3 blur kernel
            blurred = np.zeros_like(arr)
            
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    # Сдвигаем массив
                    shifted = np.roll(np.roll(arr, dy, axis=1), dx, axis=0)
                    blurred += shifted
            
            blurred = blurred // 9  # Усреднение
            
            pygame.surfarray.blit_array(result, blurred)
        
        return result
    
    # ============================================================
    # ЭФФЕКТ 3: COLOR GRADING (ЦВЕТОКОРРЕКЦИЯ)
    # ============================================================
    
    def _apply_color_grading(self, surface: pygame.Surface) -> pygame.Surface:
        """
        Применяет цветокоррекцию: saturation, brightness, contrast
        Использует numpy для производительности
        """
        try:
            arr = pygame.surfarray.array3d(surface).astype(np.float32)
            
            # 1. BRIGHTNESS (яркость)
            arr *= self.brightness
            
            # 2. CONTRAST (контраст)
            # Формула: (pixel - 128) * contrast + 128
            arr = (arr - 128.0) * self.contrast + 128.0
            
            # 3. SATURATION (насыщенность)
            if self.saturation != 1.0:
                # Конвертируем в HSV для изменения насыщенности
                # Упрощённый метод: интерполяция между grayscale и цветным
                gray = np.mean(arr, axis=2, keepdims=True)
                arr = gray + (arr - gray) * self.saturation
            
            # Clamp значений [0, 255]
            arr = np.clip(arr, 0, 255).astype(np.uint8)
            
            # Создаём новую поверхность
            result = pygame.Surface(surface.get_size())
            pygame.surfarray.blit_array(result, arr)
            
            return result
            
        except Exception as e:
            print(f"⚠️ [ColorGrading] Ошибка: {e}")
            return surface
    
    # ============================================================
    # ЭФФЕКТ 4: CHROMATIC ABERRATION (ХРОМАТИЧЕСКАЯ АБЕРРАЦИЯ)
    # ============================================================
    
    def _apply_chromatic_aberration(self, surface: pygame.Surface) -> pygame.Surface:
        """
        Оптимизированная хроматическая аберрация через разделение каналов
        
        Метод:
        1. Создать 3 копии surface
        2. Выделить R, G, B каналы
        3. Сместить R влево, B вправо
        4. Объединить с additive blending
        """
        try:
            w, h = surface.get_size()
            offset = int(self.aberration_amount)
            
            if offset == 0:
                return surface
            
            # Создаём 3 канала
            red_surface = pygame.Surface((w, h))
            green_surface = pygame.Surface((w, h))
            blue_surface = pygame.Surface((w, h))
            
            # Извлекаем массив пикселей
            arr = pygame.surfarray.array3d(surface)
            
            # Создаём массивы для каждого канала
            red_arr = np.zeros_like(arr)
            red_arr[:, :, 0] = arr[:, :, 0]  # Только красный канал
            
            green_arr = np.zeros_like(arr)
            green_arr[:, :, 1] = arr[:, :, 1]  # Только зелёный канал
            
            blue_arr = np.zeros_like(arr)
            blue_arr[:, :, 2] = arr[:, :, 2]  # Только синий канал
            
            # Записываем в поверхности
            pygame.surfarray.blit_array(red_surface, red_arr)
            pygame.surfarray.blit_array(green_surface, green_arr)
            pygame.surfarray.blit_array(blue_surface, blue_arr)
            
            # Создаём результирующую поверхность
            result = pygame.Surface((w, h))
            result.fill((0, 0, 0))
            
            # Собираем с offset'ами
            result.blit(red_surface, (-offset, 0), special_flags=pygame.BLEND_RGB_ADD)
            result.blit(green_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            result.blit(blue_surface, (offset, 0), special_flags=pygame.BLEND_RGB_ADD)
            
            return result
            
        except Exception as e:
            print(f"⚠️ [ChromaticAberration] Ошибка: {e}")
            return surface
    
    # ============================================================
    # ЭФФЕКТ 5: PIXELATION (ПИКСЕЛИЗАЦИЯ)
    # ============================================================
    
    def _apply_pixelation(self, surface: pygame.Surface) -> pygame.Surface:
        """
        Пикселизация через downscale -> upscale
        Очень быстрый эффект
        """
        try:
            w, h = surface.get_size()
            
            # Уменьшаем
            small_w = max(1, w // self.pixel_size)
            small_h = max(1, h // self.pixel_size)
            small_surface = pygame.transform.scale(surface, (small_w, small_h))
            
            # Увеличиваем обратно (без сглаживания!)
            result = pygame.transform.scale(small_surface, (w, h))
            
            return result
            
        except Exception as e:
            print(f"⚠️ [Pixelation] Ошибка: {e}")
            return surface
    
    # ============================================================
    # ЭФФЕКТ 6: CRT SCREEN (ЭФФЕКТ СТАРОГО МОНИТОРА)
    # ============================================================
    
    def _create_crt_scanlines_cache(self):
        """Создаёт кэш горизонтальных линий сканирования"""
        try:
            self._crt_scanlines_cache = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self._crt_scanlines_cache.fill((0, 0, 0, 0))
            
            # Рисуем горизонтальные линии
            alpha = int(255 * self.scanline_intensity)
            
            for y in range(0, self.height, 2):  # Каждая 2-я линия
                pygame.draw.line(
                    self._crt_scanlines_cache,
                    (0, 0, 0, alpha),
                    (0, y),
                    (self.width, y),
                    1
                )
            
            print("✓ [CRT] Кэш сканлайнов создан")
            
        except Exception as e:
            print(f"⚠️ [CRT] Ошибка создания кэша: {e}")
            self._crt_scanlines_cache = None
    
    def _apply_crt(self, surface: pygame.Surface) -> pygame.Surface:
        """Применяет CRT эффект (сканлайны)"""
        if self._crt_scanlines_cache is None:
            return surface
        
        result = surface.copy()
        result.blit(self._crt_scanlines_cache, (0, 0))
        
        return result
    
    # ============================================================
    # ЭФФЕКТ 7: GLOW НА КОНКРЕТНЫХ ПОЗИЦИЯХ
    # ============================================================
    
    def render_with_glow(
        self,
        surface: pygame.Surface,
        positions: List[Tuple[int, int]],
        color: Tuple[int, int, int] = (255, 255, 100),
        intensity: float = 0.5
    ) -> pygame.Surface:
        """
        Добавляет свечение на указанных позициях
        
        Args:
            surface: Исходная поверхность
            positions: Список координат (x, y) центров свечения
            color: Цвет свечения (RGB)
            intensity: Интенсивность 0.0-1.0
        """
        try:
            result = surface.copy()
            glow_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            
            for pos in positions:
                self._draw_radial_glow(glow_surface, pos, color, intensity)
            
            # Размываем для мягкости
            glow_small = pygame.transform.smoothscale(
                glow_surface,
                (surface.get_width() // 2, surface.get_height() // 2)
            )
            glow_blurred = pygame.transform.smoothscale(
                glow_small,
                surface.get_size()
            )
            
            # Накладываем с ADD blending
            result.blit(glow_blurred, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            
            return result
            
        except Exception as e:
            print(f"⚠️ [Glow] Ошибка: {e}")
            return surface
    
    def _draw_radial_glow(
        self,
        surface: pygame.Surface,
        center: Tuple[int, int],
        color: Tuple[int, int, int],
        intensity: float
    ):
        """Рисует радиальное свечение"""
        radius = 100  # Радиус свечения
        
        for r in range(radius, 0, -10):
            alpha = int(255 * intensity * (1.0 - r / radius) ** 2)
            alpha = min(255, max(0, alpha))
            
            glow_color = (*color, alpha)
            pygame.draw.circle(surface, glow_color, center, r)
    
    # ============================================================
    # SCREEN SHAKE (ТРЯСКА ЭКРАНА)
    # ============================================================
    
    def trigger_shake(self, duration: float = 0.3, intensity: float = 10.0):
        """
        Запускает эффект тряски экрана
        
        Args:
            duration: Длительность в секундах
            intensity: Амплитуда тряски в пикселях
        """
        self.shake_enabled = True
        self.shake_time = duration
        self.shake_intensity = intensity
    
    def update_shake(self, dt: float):
        """Обновляет эффект тряски"""
        if self.shake_time > 0:
            self.shake_time -= dt
            
            # Генерируем случайный offset
            import random
            offset_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            offset_y = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            
            # Затухание
            fade = self.shake_time / 0.3
            self.shake_offset = (int(offset_x * fade), int(offset_y * fade))
        else:
            self.shake_enabled = False
            self.shake_offset = (0, 0)
    
    # ============================================================
    # УТИЛИТЫ И ПРОИЗВОДИТЕЛЬНОСТЬ
    # ============================================================
    
    def _on_screen_resize(self, new_size: Tuple[int, int]):
        """Обработка изменения размера экрана"""
        self.width, self.height = new_size
        self._last_screen_size = new_size
        
        print(f"🔄 [PyGameShaders] Изменение разрешения: {new_size}")
        
        # Пересоздаём кэши
        self._create_vignette_cache()
        self._create_crt_scanlines_cache()
    
    def _update_performance_stats(self, frame_time: float):
        """Обновляет статистику производительности"""
        self.fps_samples.append(1.0 / max(frame_time, 0.001))
        
        # Храним только последние 60 сэмплов
        if len(self.fps_samples) > 60:
            self.fps_samples.pop(0)
        
        # Средний FPS
        avg_fps = sum(self.fps_samples) / len(self.fps_samples)
        
        # Включаем performance mode если FPS падает
        if avg_fps < 45 and not self.performance_mode:
            self.performance_mode = True
            self.bloom_enabled = False
            print("⚠️ [PyGameShaders] Performance mode включен (низкий FPS)")
    
    def get_fps(self) -> float:
        """Возвращает средний FPS"""
        if not self.fps_samples:
            return 60.0
        return sum(self.fps_samples) / len(self.fps_samples)
    
    # ============================================================
    # МЕТОДЫ НАСТРОЙКИ
    # ============================================================
    
    def set_vignette(self, enabled: bool, intensity: float = 0.5):
        """Настройка виньетки"""
        self.vignette_enabled = enabled
        if self.vignette_intensity != intensity:
            self.vignette_intensity = intensity
            self._create_vignette_cache()
    
    def set_bloom(self, enabled: bool, intensity: float = 0.3, threshold: int = 200):
        """Настройка bloom"""
        self.bloom_enabled = enabled and not self.performance_mode
        self.bloom_intensity = intensity
        self.bloom_threshold = threshold
    
    def set_color_grading(
        self,
        enabled: bool,
        saturation: float = 1.0,
        brightness: float = 1.0,
        contrast: float = 1.0
    ):
        """Настройка цветокоррекции"""
        self.color_grading_enabled = enabled
        self.saturation = saturation
        self.brightness = brightness
        self.contrast = contrast
    
    def set_chromatic_aberration(self, enabled: bool, amount: float = 2.0):
        """Настройка хроматической аберрации"""
        self.chromatic_aberration_enabled = enabled
        self.aberration_amount = amount
    
    def set_pixelation(self, enabled: bool, pixel_size: int = 4):
        """Настройка пикселизации"""
        self.pixelation_enabled = enabled
        self.pixel_size = max(1, min(20, pixel_size))
    
    def set_crt(self, enabled: bool, scanline_intensity: float = 0.3):
        """Настройка CRT эффекта"""
        self.crt_enabled = enabled
        if self.scanline_intensity != scanline_intensity:
            self.scanline_intensity = scanline_intensity
            self._create_crt_scanlines_cache()
    
    # ============================================================
    # ТЕСТИРОВАНИЕ
    # ============================================================
    
    def test_effects(self, surface: pygame.Surface):
        """
        Тестирование всех эффектов с замером производительности
        """
        print("\n" + "="*60)
        print("🧪 ТЕСТИРОВАНИЕ ЭФФЕКТОВ PyGameShaders")
        print("="*60)
        
        # Сохраняем текущее состояние
        original_state = {
            'vignette': self.vignette_enabled,
            'bloom': self.bloom_enabled,
            'color_grading': self.color_grading_enabled,
            'chromatic': self.chromatic_aberration_enabled,
            'pixelation': self.pixelation_enabled,
            'crt': self.crt_enabled,
        }
        
        # Отключаем всё
        self.vignette_enabled = False
        self.bloom_enabled = False
        self.color_grading_enabled = False
        self.chromatic_aberration_enabled = False
        self.pixelation_enabled = False
        self.crt_enabled = False
        
        tests = [
            ("Baseline (без эффектов)", {}),
            ("Vignette", {'vignette_enabled': True}),
            ("Bloom", {'bloom_enabled': True}),
            ("Color Grading", {'color_grading_enabled': True}),
            ("Chromatic Aberration", {'chromatic_aberration_enabled': True}),
            ("Pixelation", {'pixelation_enabled': True}),
            ("CRT", {'crt_enabled': True}),
            ("Все эффекты", {
                'vignette_enabled': True,
                'bloom_enabled': True,
                'color_grading_enabled': True,
                'chromatic_aberration_enabled': True,
                'crt_enabled': True,
            }),
        ]
        
        results = []
        
        for test_name, params in tests:
            # Применяем параметры
            for key, value in params.items():
                setattr(self, key, value)
            
            # Тест (10 итераций)
            times = []
            for _ in range(10):
                start = time.time()
                _ = self.render(surface)
                elapsed = time.time() - start
                times.append(elapsed)
            
            avg_time = sum(times) / len(times)
            avg_fps = 1.0 / avg_time
            
            results.append((test_name, avg_time * 1000, avg_fps))
            
            # Отключаем обратно
            for key in params:
                setattr(self, key, False)
        
        # Выводим результаты
        print("\nРезультаты:")
        print("-" * 60)
        for name, ms, fps in results:
            print(f"{name:30s} | {ms:6.2f} ms | {fps:5.1f} FPS")
        
        print("="*60)
        
        # Восстанавливаем состояние
        for key, value in original_state.items():
            setattr(self, key, value)
        
        print("✅ Тестирование завершено\n")

