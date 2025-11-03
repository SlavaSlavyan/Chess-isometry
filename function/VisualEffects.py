"""
Система визуальных эффектов для Chess Isometry
Пост-процессинг эффекты, имитирующие шейдеры
"""

import pygame
import numpy as np
import math
import random


class VisualEffects:
    """Менеджер визуальных эффектов"""
    
    def __init__(self, m):
        self.m = m
        
        # Настройки эффектов (можно менять через dev menu)
        self.effects_enabled = {
            'bloom': True,
            'vignette': True,
            'chromatic_aberration': False,
            'scanlines': False,
            'crt': False,
            'screen_shake': True,
            'particles': True,
            'lighting': True,
            'color_grading': False,
            'motion_blur': False
        }
        
        # Параметры эффектов
        self.bloom_intensity = 0.3
        self.vignette_intensity = 0.4
        self.chromatic_intensity = 2.0
        self.scanline_intensity = 0.15
        self.crt_distortion = 0.05
        self.color_temperature = 0.0  # -1.0 (холодный) до 1.0 (теплый)
        self.motion_blur_strength = 0.3
        
        # Screen shake
        self.shake_amplitude = 0
        self.shake_duration = 0
        self.shake_start_time = 0
        
        # Particles
        self.particles = []
        
        # Motion blur frames
        self.previous_frames = []
        self.max_blur_frames = 3
        
        # Lighting points
        self.light_sources = []
        
        # Временные поверхности для эффектов
        self.temp_surface = None
        
        print("🎨 [VisualEffects] Система визуальных эффектов инициализирована")
    
    def apply_effects(self, screen):
        """Применяет все активные эффекты к экрану"""
        if not any(self.effects_enabled.values()):
            return screen
        
        # Создаем копию для обработки
        processed = screen.copy()
        
        # Применяем эффекты в порядке
        if self.effects_enabled['lighting']:
            processed = self.apply_lighting(processed)
        
        if self.effects_enabled['bloom']:
            processed = self.apply_bloom(processed)
        
        if self.effects_enabled['chromatic_aberration']:
            processed = self.apply_chromatic_aberration(processed)
        
        if self.effects_enabled['vignette']:
            processed = self.apply_vignette(processed)
        
        if self.effects_enabled['scanlines']:
            processed = self.apply_scanlines(processed)
        
        if self.effects_enabled['crt']:
            processed = self.apply_crt_effect(processed)
        
        if self.effects_enabled['color_grading']:
            processed = self.apply_color_grading(processed)
        
        if self.effects_enabled['motion_blur']:
            processed = self.apply_motion_blur(processed)
        
        # Screen shake применяется через offset, не к surface
        
        return processed
    
    def apply_bloom(self, surface):
        """Эффект свечения (bloom)"""
        try:
            width, height = surface.get_size()
            
            # Создаем яркую версию
            bright = surface.copy()
            
            # Размываем яркие области (простое box blur)
            scale = 4  # Уменьшаем для производительности
            small = pygame.transform.smoothscale(bright, (width // scale, height // scale))
            
            # Размываем несколько раз
            for _ in range(2):
                small = pygame.transform.smoothscale(small, (width // (scale * 2), height // (scale * 2)))
                small = pygame.transform.smoothscale(small, (width // scale, height // scale))
            
            # Возвращаем к исходному размеру
            blurred = pygame.transform.smoothscale(small, (width, height))
            
            # Смешиваем с оригиналом
            blurred.set_alpha(int(255 * self.bloom_intensity))
            surface.blit(blurred, (0, 0), special_flags=pygame.BLEND_ADD)
            
        except Exception as e:
            print(f"⚠️ [Bloom] Ошибка: {e}")
        
        return surface
    
    def apply_vignette(self, surface):
        """Эффект виньетирования (затемнение краев)"""
        try:
            width, height = surface.get_size()
            
            # Создаем градиент от центра
            vignette = pygame.Surface((width, height), pygame.SRCALPHA)
            
            center_x, center_y = width // 2, height // 2
            max_distance = math.sqrt(center_x**2 + center_y**2)
            
            # Рисуем радиальный градиент
            for radius in range(int(max_distance), 0, -20):
                alpha = int(255 * self.vignette_intensity * (1 - radius / max_distance))
                pygame.draw.ellipse(vignette, (0, 0, 0, alpha), 
                                  (center_x - radius, center_y - radius, radius * 2, radius * 2))
            
            surface.blit(vignette, (0, 0))
            
        except Exception as e:
            print(f"⚠️ [Vignette] Ошибка: {e}")
        
        return surface
    
    def apply_chromatic_aberration(self, surface):
        """Хроматическая аберрация (разделение RGB каналов)"""
        try:
            width, height = surface.get_size()
            
            # Создаем 3 копии для каналов
            offset = int(self.chromatic_intensity)
            
            red_surface = surface.copy()
            red_surface.set_colorkey((0, 0, 0))
            
            # Сдвигаем красный канал
            temp = pygame.Surface((width, height))
            temp.fill((0, 0, 0))
            temp.blit(surface, (-offset, 0))
            
            # Извлекаем только красный
            red_array = pygame.surfarray.pixels3d(temp)
            result_array = pygame.surfarray.pixels3d(surface)
            result_array[:, :, 0] = red_array[:, :, 0]
            
            # Сдвигаем синий канал
            temp.fill((0, 0, 0))
            temp.blit(surface, (offset, 0))
            blue_array = pygame.surfarray.pixels3d(temp)
            result_array[:, :, 2] = blue_array[:, :, 2]
            
            del red_array, blue_array, result_array
            
        except Exception as e:
            print(f"⚠️ [ChromaticAberration] Ошибка: {e}")
        
        return surface
    
    def apply_scanlines(self, surface):
        """Эффект сканлиний (ЭЛТ монитор)"""
        try:
            width, height = surface.get_size()
            
            scanlines = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Рисуем горизонтальные линии
            for y in range(0, height, 2):
                alpha = int(255 * self.scanline_intensity)
                pygame.draw.line(scanlines, (0, 0, 0, alpha), (0, y), (width, y))
            
            surface.blit(scanlines, (0, 0))
            
        except Exception as e:
            print(f"⚠️ [Scanlines] Ошибка: {e}")
        
        return surface
    
    def apply_crt_effect(self, surface):
        """Эффект ЭЛТ монитора с искажением"""
        try:
            width, height = surface.get_size()
            
            # Применяем scanlines
            surface = self.apply_scanlines(surface)
            
            # Добавляем легкое искажение по краям (barrel distortion)
            # Для производительности делаем упрощенную версию
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Темные углы для имитации искривления
            corner_size = min(width, height) // 4
            for corner in [(0, 0), (width - corner_size, 0), 
                          (0, height - corner_size), (width - corner_size, height - corner_size)]:
                alpha = int(100 * self.crt_distortion)
                pygame.draw.rect(overlay, (0, 0, 0, alpha), 
                               (corner[0], corner[1], corner_size, corner_size))
            
            surface.blit(overlay, (0, 0))
            
        except Exception as e:
            print(f"⚠️ [CRT] Ошибка: {e}")
        
        return surface
    
    def apply_color_grading(self, surface):
        """Цветокоррекция (теплый/холодный оттенок)"""
        try:
            if self.color_temperature == 0:
                return surface
            
            width, height = surface.get_size()
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            
            if self.color_temperature > 0:  # Теплый
                color = (255, int(200 * self.color_temperature), 0)
                alpha = int(30 * abs(self.color_temperature))
            else:  # Холодный
                color = (0, int(150 * abs(self.color_temperature)), 255)
                alpha = int(30 * abs(self.color_temperature))
            
            overlay.fill((*color, alpha))
            surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_ADD)
            
        except Exception as e:
            print(f"⚠️ [ColorGrading] Ошибка: {e}")
        
        return surface
    
    def apply_motion_blur(self, surface):
        """Размытие движения"""
        try:
            # Сохраняем текущий кадр
            self.previous_frames.append(surface.copy())
            
            # Ограничиваем количество сохраненных кадров
            if len(self.previous_frames) > self.max_blur_frames:
                self.previous_frames.pop(0)
            
            # Смешиваем предыдущие кадры
            if len(self.previous_frames) > 1:
                for i, frame in enumerate(self.previous_frames[:-1]):
                    alpha = int(255 * self.motion_blur_strength * (i + 1) / len(self.previous_frames))
                    frame.set_alpha(alpha)
                    surface.blit(frame, (0, 0))
            
        except Exception as e:
            print(f"⚠️ [MotionBlur] Ошибка: {e}")
        
        return surface
    
    def apply_lighting(self, surface):
        """Динамическое освещение"""
        try:
            if not self.light_sources:
                return surface
            
            width, height = surface.get_size()
            lighting = pygame.Surface((width, height), pygame.SRCALPHA)
            lighting.fill((0, 0, 0, 150))  # Базовая темнота
            
            # Рисуем источники света
            for light in self.light_sources:
                x, y, radius, color, intensity = light
                
                # Радиальный градиент света
                for r in range(radius, 0, -10):
                    alpha = int(255 * intensity * (r / radius))
                    light_color = (*color, alpha)
                    pygame.draw.circle(lighting, light_color, (int(x), int(y)), r, 0)
            
            surface.blit(lighting, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            
        except Exception as e:
            print(f"⚠️ [Lighting] Ошибка: {e}")
        
        return surface
    
    def trigger_screen_shake(self, intensity=10, duration=500):
        """Запускает эффект тряски экрана"""
        self.shake_amplitude = intensity
        self.shake_duration = duration
        self.shake_start_time = pygame.time.get_ticks()
    
    def get_screen_shake_offset(self):
        """Возвращает смещение для тряски экрана"""
        if not self.effects_enabled['screen_shake']:
            return (0, 0)
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.shake_start_time
        
        if elapsed < self.shake_duration:
            # Затухающая тряска
            progress = 1 - (elapsed / self.shake_duration)
            amplitude = self.shake_amplitude * progress
            
            offset_x = random.uniform(-amplitude, amplitude)
            offset_y = random.uniform(-amplitude, amplitude)
            
            return (int(offset_x), int(offset_y))
        
        return (0, 0)
    
    def add_light_source(self, x, y, radius=200, color=(255, 255, 200), intensity=0.8):
        """Добавляет источник света"""
        self.light_sources.append((x, y, radius, color, intensity))
    
    def clear_light_sources(self):
        """Очищает все источники света"""
        self.light_sources.clear()
    
    def add_particle(self, x, y, velocity, color, lifetime=1000, size=3):
        """Добавляет частицу"""
        self.particles.append({
            'x': x,
            'y': y,
            'vx': velocity[0],
            'vy': velocity[1],
            'color': color,
            'lifetime': lifetime,
            'birth_time': pygame.time.get_ticks(),
            'size': size
        })
    
    def update_particles(self, dt):
        """Обновляет частицы"""
        current_time = pygame.time.get_ticks()
        
        # Удаляем мертвые частицы
        self.particles = [p for p in self.particles 
                         if current_time - p['birth_time'] < p['lifetime']]
        
        # Обновляем позиции
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt / 16.67  # Нормализация к 60 FPS
            particle['y'] += particle['vy'] * dt / 16.67
            particle['vy'] += 0.5  # Гравитация
    
    def draw_particles(self, screen):
        """Рисует частицы"""
        if not self.effects_enabled['particles']:
            return
        
        current_time = pygame.time.get_ticks()
        
        for particle in self.particles:
            # Затухание по времени жизни
            age = current_time - particle['birth_time']
            alpha = int(255 * (1 - age / particle['lifetime']))
            
            color = (*particle['color'][:3], alpha)
            
            # Рисуем частицу
            pos = (int(particle['x']), int(particle['y']))
            pygame.draw.circle(screen, color, pos, particle['size'])
    
    def create_explosion_particles(self, x, y, count=20, color=(255, 200, 50)):
        """Создает взрыв частиц"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            self.add_particle(x, y, (vx, vy), color, 
                            lifetime=random.randint(500, 1500),
                            size=random.randint(2, 5))
    
    def toggle_effect(self, effect_name, enabled=None):
        """Включает/выключает эффект"""
        if effect_name in self.effects_enabled:
            if enabled is None:
                self.effects_enabled[effect_name] = not self.effects_enabled[effect_name]
            else:
                self.effects_enabled[effect_name] = enabled
            
            print(f"🎨 [VisualEffects] {effect_name}: {'ON' if self.effects_enabled[effect_name] else 'OFF'}")
    
    def get_info(self):
        """Возвращает информацию о текущих эффектах"""
        active = [name for name, enabled in self.effects_enabled.items() if enabled]
        return {
            'active_effects': active,
            'particle_count': len(self.particles),
            'light_sources': len(self.light_sources)
        }

