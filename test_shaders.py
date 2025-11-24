"""
Тест производительности системы шейдеров PyGameShaders
Запуск: python test_shaders.py
"""

import pygame
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from function.PyGameShaders import PyGameShaders

def main():
    """Тестирование всех эффектов шейдеров"""
    pygame.init()
    
    # Создаём тестовое окно
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PyGameShaders Performance Test")
    
    # Инициализируем систему шейдеров
    shaders = PyGameShaders(width, height)
    
    # Создаём тестовую сцену (чтобы было что обрабатывать)
    test_surface = pygame.Surface((width, height))
    test_surface.fill((40, 40, 60))
    
    # Рисуем тестовые объекты
    for i in range(20):
        color = (200 + i * 2, 150 + i * 3, 100 + i * 2)
        size = 50 + i * 10
        x = (width // 4) + (i % 5) * 150
        y = (height // 4) + (i // 5) * 150
        pygame.draw.circle(test_surface, color, (x, y), size)
    
    # Текст
    font = pygame.font.Font(None, 48)
    text = font.render("PyGameShaders Performance Test", True, (255, 255, 255))
    test_surface.blit(text, (width // 2 - 300, 50))
    
    # Запускаем тест
    print("\n" + "="*60)
    print("🚀 ЗАПУСК ТЕСТА ПРОИЗВОДИТЕЛЬНОСТИ")
    print("="*60)
    
    shaders.test_effects(test_surface)
    
    print("\n✅ Тест завершён! Проверьте результаты выше.")
    print("\n📊 Рекомендации:")
    print("   - < 2ms: Отлично, можно использовать все эффекты")
    print("   - 2-5ms: Хорошо, большинство эффектов работают")
    print("   - 5-10ms: Средне, избегайте Bloom")
    print("   - > 10ms: Плохо, используйте только Vignette")
    
    pygame.quit()

if __name__ == "__main__":
    main()

