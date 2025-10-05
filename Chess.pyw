import pygame
import json
import math
import os
import time
import random
import sys

# Настройка кодировки для Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def load_config():
    try:
        with open(os.path.join('data', 'config.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # Значения по умолчанию, если конфиг не найден
        return {
            'start-size': [1280, 720],
            'fullscreen': False,
            'them': 'base',
            'f3': False,
        }


def load_theme(theme_name: str):
    try:
        with open(os.path.join('data', 'them', f'{theme_name}.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # Минимальный фоллбек
        return {
            'Game': {
                'bg': [30, 30, 35],
                'chessboard': [45, 50, 60],
                'light_cell': [110, 110, 120],
                'dark_cell': [70, 70, 80],
                'selected_cell': [140, 170, 255],
            },
            'Global': {
                'f3_text': [120, 255, 120]
            }
        }


def iso_diamond_points(cx: int, cy: int, w: float, h: float, scale: float = 1.0):
    # Ромб (изометрическая клетка)
    hw = (w * scale) / 2
    hh = (h * scale) / 2
    return [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]


def to_iso(center_x: int, center_y: int, grid_x: int, grid_y: int, tile_w: int, tile_h: int):
    # Простейшая изометрическая проекция 2:1
    sx = center_x + (grid_x - grid_y) * (tile_w // 2)
    sy = center_y + (grid_x + grid_y) * (tile_h // 2)
    return sx, sy


def show_loading():
    cfg = load_config()
    theme = load_theme(cfg.get('them', 'base'))
    colors = theme.get('Game', {})
    bg = tuple(colors.get('bg', [30, 30, 35]))
    chessboard_color = tuple(colors.get('chessboard', [45, 50, 60]))
    light_cell = tuple(colors.get('light_cell', [110, 110, 120]))
    dark_cell = tuple(colors.get('dark_cell', [70, 70, 80]))

    pygame.init()

    start_w, start_h = cfg.get('start-size', [1280, 720])
    flags = pygame.DOUBLEBUF | pygame.RESIZABLE
    if cfg.get('fullscreen', False):
        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
        start_w, start_h = 0, 0

    screen = pygame.display.set_mode((start_w, start_h), flags)
    pygame.display.set_caption('Chess Isometry')
    clock = pygame.time.Clock()

    # Шрифты
    try:
        title_font = pygame.font.Font(os.path.join('data', 'font', 'title.ttf'), 56)
        text_font = pygame.font.Font(os.path.join('data', 'font', 'text.ttf'), 18)
    except Exception:
        title_font = pygame.font.SysFont(None, 56)
        text_font = pygame.font.SysFont(None, 18)

    # Параметры изометрической доски
    W, H = screen.get_size()
    center_x, center_y = W // 2, H // 2
    tile_w, tile_h = 80, 40  # 2:1 ромб

    # Подготовка сетки клеток (8x8)
    grid = []
    for gy in range(8):
        for gx in range(8):
            sx, sy = to_iso(center_x, center_y - 40, gx - 4, gy - 4, tile_w, tile_h)
            grid.append((gx, gy, sx, sy))

    # Анимация «волны» появления клеток от центра доски
    start_time = time.time()
    reveal_duration = 1.35  # время общей волны
    hold_duration = 0.35    # пауза после полного появления

    running = True
    phase = 'reveal'
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t = time.time() - start_time
        screen.fill(bg)

        # Фоновая «подложка» доски
        pygame.draw.polygon(
            screen,
            chessboard_color,
            iso_diamond_points(center_x, center_y - 40, tile_w * 8 * 0.72, tile_h * 8 * 0.72, 1.0),
            0
        )

        # Волна появления клеток (по расстоянию от центра)
        max_dist = math.hypot(3.5, 3.5)
        for gx, gy, sx, sy in grid:
            dx = gx - 3.5
            dy = gy - 3.5
            dist = math.hypot(dx, dy)
            # локальное время клетки
            local = (t / reveal_duration) - (dist / max_dist) * 0.75
            local = max(0.0, min(1.0, local))
            scale = local  # масштаб клетки 0..1
            if scale <= 0:
                continue

            color = light_cell if ((gx + gy) % 2 == 1) else dark_cell
            pts = iso_diamond_points(sx, sy, tile_w, tile_h, scale)
            # Подложка (тень) для приятного объёма
            shadow = [(x + 2, y + 3) for (x, y) in pts]
            pygame.draw.polygon(screen, (0, 0, 0, 0), shadow, 0)
            pygame.draw.polygon(screen, color, pts, 0)

        # Заголовок и подпись (с лёгким слайдом и импульсом)
        pulse = math.sin(t * 2.0) * 0.5 + 0.5
        title = title_font.render('CHESS ISOMETRY', True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, int(center_y - 140 - (1.0 - min(1.0, t * 2)) * 40)))
        screen.blit(title, title_rect)

        subtitle = text_font.render('loading...', True, (200, 200, 200))
        sub_rect = subtitle.get_rect(center=(center_x, title_rect.bottom + 26))
        screen.blit(subtitle, sub_rect)

        # Переход: частицы разлетаются + плавное растворение
        if phase == 'reveal' and t > reveal_duration + hold_duration:
            phase = 'transition'
            transition_start = time.time()
            # Создаём частицы из углов доски
            particles = []
            for _ in range(60):
                angle = math.radians(random.uniform(0, 360))
                speed = random.uniform(150, 400)
                px = center_x + random.uniform(-50, 50)
                py = center_y + random.uniform(-50, 50)
                particles.append({
                    'x': px,
                    'y': py,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'life': random.uniform(0.5, 1.0),
                    'size': random.randint(2, 6),
                    'color': random.choice([light_cell, dark_cell, (255, 255, 255)])
                })
        
        if phase == 'transition':
            ct = time.time() - transition_start
            dt = 1/60.0
            
            # Обновляем и рисуем частицы
            for p in particles[:]:
                p['x'] += p['vx'] * dt
                p['y'] += p['vy'] * dt
                p['life'] -= dt
                if p['life'] > 0:
                    alpha = int(255 * p['life'])
                    size = int(p['size'] * p['life'])
                    if size > 0:
                        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                        pygame.draw.circle(s, (*p['color'], alpha), (size, size), size)
                        screen.blit(s, (int(p['x'] - size), int(p['y'] - size)))
            
            # Затемнение с пульсацией
            fade_progress = max(0.0, min(1.0, ct / 0.8))
            fade_alpha = int(255 * fade_progress)
            fade_surf = pygame.Surface((W, H))
            fade_surf.fill(bg)
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))
            
            if ct >= 1.2:
                break

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    # Красивая загрузка в нашем стиле
    show_loading()

    # Переход к основной игре
    cfg = load_config()

if cfg.get('engine', 'pygame') == 'panda3d':
    # Запуск Panda3D варианта
    pygame.quit()
    from function.p3d.app import run_panda_app
    run_panda_app()
    sys.exit(0)
else:
    from function.main import Main
    Chess = Main()
    Chess.start()