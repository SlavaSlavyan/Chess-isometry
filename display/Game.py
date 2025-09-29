import pygame
import math
import sys
import os

class Game:

    def __init__(self,m):

        self.rotate = [0,-90]
        self.pulse = 0
        # Эффект тряски экрана
        self.shake_time_ms = 0
        self.shake_amp = 0
        self.shake_seed = 0
        
        def get_resource_path(relative_path):
            """Получить абсолютный путь к ресурсу, работает как в разработке, так и в PyInstaller"""
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            else:
                return relative_path
        
        # Загружаем шрифты
        self.font_text = pygame.font.Font(get_resource_path('data/font/text.ttf'), 24)
        self.font_title = pygame.font.Font(get_resource_path('data/font/title.ttf'), 48)
        self.font_small = pygame.font.Font(get_resource_path('data/font/text.ttf'), 18)
        
        # Система частиц для эффекта распада
        self.particles = []

    def main(self,m):
        
        # Смещение экрана из-за тряски
        ox, oy = 0, 0
        if self.shake_time_ms > 0:
            # Псевдослучайное дрожание в пределах амплитуды
            import random
            random.seed(self.shake_seed + int(self.shake_time_ms / 16))
            ox = random.randint(-self.shake_amp, self.shake_amp)
            oy = random.randint(-self.shake_amp, self.shake_amp)
        
        # Фон
        m.Disp.screen.fill(m.Disp.colors['Game']['bg'])
        
        if self.rotate[1] < 0:
            self.chessboard(m)
            self.cells(m, (ox, oy))
        else:
            self.cells(m, (ox, oy))
            self.chessboard(m)
        
        # Обновляем и рисуем частицы
        self.update_particles()
        self.draw_particles(m)
        
        # Отображаем индикатор текущего игрока или результат игры
        if m.PI.Game.game_over:
            self.draw_game_over(m)
        else:
            self.draw_player_indicator(m)
            # Показываем инструкции только если F3 выключен
            if not m.config['f3']:
                self.draw_game_info(m)
        
        if m.config['f3']:
            pygame.draw.line(m.Disp.screen,(0,255,0),(m.Disp.width//2,0),(m.Disp.width//2,m.Disp.height))
            pygame.draw.line(m.Disp.screen,(0,0,255),(0,m.Disp.height//2),(m.Disp.width,m.Disp.height//2))
        
        self.pulse += 0.05
    
    def draw_player_indicator(self, m):
        """Отображает индикатор текущего игрока"""
        current_player = m.PI.Game.current_player
        
        # Позиция индикатора в правом верхнем углу
        indicator_x = m.Disp.width - 150
        indicator_y = 30
        
        # Цвет индикатора в зависимости от игрока
        color = (255, 255, 255) if current_player == "white" else (100, 100, 100)
        
        # Рисуем круг-индикатор
        pygame.draw.circle(m.Disp.screen, color, (indicator_x, indicator_y), 20, 3)
        
        # Добавляем текст
        text_color = (255, 255, 255)
        player_text = "White" if current_player == "white" else "Black"
        text = self.font_text.render(f"Turn: {player_text}", True, text_color)
        text_rect = text.get_rect()
        text_rect.right = indicator_x - 30
        text_rect.centery = indicator_y
        m.Disp.screen.blit(text, text_rect)
    
    def draw_game_over(self, m):
        """Отображает экран окончания игры"""
        winner = m.PI.Game.winner
        
        # Полупрозрачный фон
        overlay = pygame.Surface((m.Disp.width, m.Disp.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        m.Disp.screen.blit(overlay, (0, 0))
        
        # Основной текст победы
        winner_text = f"{winner.upper()} WINS!"
        text_color = (255, 215, 0)  # Золотой цвет
        
        # Рендерим и центрируем главный текст с title шрифтом
        main_text = self.font_title.render(winner_text, True, text_color)
        main_rect = main_text.get_rect()
        main_rect.center = (m.Disp.width // 2, m.Disp.height // 2 - 50)
        m.Disp.screen.blit(main_text, main_rect)
        
        # Дополнительный текст с обычным шрифтом
        sub_text1 = "Press R to restart"
        sub_text2 = "Press ESC to exit"
        
        sub_render1 = self.font_text.render(sub_text1, True, (255, 255, 255))
        sub_rect1 = sub_render1.get_rect()
        sub_rect1.center = (m.Disp.width // 2, m.Disp.height // 2 + 20)
        m.Disp.screen.blit(sub_render1, sub_rect1)
        
        sub_render2 = self.font_small.render(sub_text2, True, (200, 200, 200))
        sub_rect2 = sub_render2.get_rect()
        sub_rect2.center = (m.Disp.width // 2, m.Disp.height // 2 + 50)
        m.Disp.screen.blit(sub_render2, sub_rect2)
    
    def draw_game_info(self, m):
        """Отображает информацию об игре в левом верхнем углу"""
        info_x = 20
        info_y = 20
        
        # Заголовок игры
        title_text = "CHESS ISOMETRY"
        title_render = self.font_text.render(title_text, True, (255, 255, 255))
        m.Disp.screen.blit(title_render, (info_x, info_y))
        
        # Инструкции по управлению
        controls = [
            "Controls:",
            "WASD/Arrows - Rotate board",
            "Mouse wheel - Zoom",
            "F11 - Fullscreen",
            "Click piece to select",
            "Click green/red to move"
        ]
        
        for i, control in enumerate(controls):
            color = (200, 200, 200) if i == 0 else (150, 150, 150)
            font = self.font_small if i > 0 else self.font_text
            control_render = font.render(control, True, color)
            m.Disp.screen.blit(control_render, (info_x, info_y + 40 + i * 20))
    
    def create_destruction_effect(self, m, cell_pos, piece_type):
        """Создает эффект распада фигуры из кусочков спрайта"""
        import random
        
        x, y = cell_pos
        cell_screen_pos = m.PI.Game.cells[x][y]['pos']
        
        # Получаем спрайт фигуры
        if piece_type in m.AssetManager.img:
            original_image = m.AssetManager.img[piece_type]
            z = m.config['zoom']
            scaled_image = pygame.transform.scale(original_image, (int(50*z), int(50*z)))
            
            # Создаем кусочки изображения
            piece_width = scaled_image.get_width()
            piece_height = scaled_image.get_height()
            
            # Размер одного кусочка (фиксированный для всей фигуры)
            base_chunk_size = 6
            chunks_x = piece_width // base_chunk_size
            chunks_y = piece_height // base_chunk_size
            
            # Создаем частицы из кусочков
            for chunk_x in range(chunks_x):
                for chunk_y in range(chunks_y):
                    # Случайный размер для каждого кусочка
                    chunk_size = random.randint(4, 8)
                    # Пропускаем некоторые кусочки случайно для реалистичности
                    if random.random() < 0.2:  # 20% шанс пропустить кусочек
                        continue
                    
                    # Вырезаем кусочек из изображения
                    chunk_rect = pygame.Rect(
                        chunk_x * base_chunk_size, 
                        chunk_y * base_chunk_size, 
                        base_chunk_size, 
                        base_chunk_size
                    )
                    
                    # Проверяем, что кусочек не выходит за границы
                    if chunk_rect.right <= piece_width and chunk_rect.bottom <= piece_height:
                        chunk_surface = pygame.Surface((base_chunk_size, base_chunk_size), pygame.SRCALPHA)
                        chunk_surface.blit(scaled_image, (0, 0), chunk_rect)
                        
                        # Создаем частицу с кусочком изображения
                        particle = {
                            'x': cell_screen_pos[0] + chunk_x * base_chunk_size - piece_width//2 + random.randint(-5, 5),
                            'y': cell_screen_pos[1] + chunk_y * base_chunk_size - piece_height//2 + random.randint(-5, 5),
                            'vx': random.uniform(-4, 4),
                            'vy': random.uniform(-5, -1),
                            'rotation': random.uniform(0, 360),
                            'rotation_speed': random.uniform(-10, 10),
                            'life': random.randint(80, 120),  # Разное время жизни
                            'max_life': 100,
                            'image': chunk_surface,
                            'size': base_chunk_size
                        }
                        self.particles.append(particle)
    
    def update_particles(self):
        """Обновляет состояние всех частиц"""
        for particle in self.particles[:]:  # Создаем копию списка для безопасного удаления
            # Обновляем позицию
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Гравитация
            particle['vy'] += 0.15
            
            # Сопротивление воздуха
            particle['vx'] *= 0.99
            particle['vy'] *= 0.99
            
            # Вращение
            if 'rotation' in particle:
                particle['rotation'] += particle['rotation_speed']
            
            # Уменьшаем время жизни
            particle['life'] -= 1
            
            # Удаляем мертвые частицы
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, m):
        """Рисует все частицы"""
        for particle in self.particles:
            if 'image' in particle:
                # Рисуем частицы-кусочки изображения
                alpha = int(255 * (particle['life'] / particle['max_life']))
                
                # Поворачиваем изображение
                rotated_image = pygame.transform.rotate(particle['image'], particle['rotation'])
                
                # Применяем прозрачность
                rotated_image.set_alpha(alpha)
                
                # Получаем новые размеры после поворота
                rotated_rect = rotated_image.get_rect()
                rotated_rect.center = (int(particle['x']), int(particle['y']))
                
                # Отображаем на экране
                m.Disp.screen.blit(rotated_image, rotated_rect)
            
            else:
                # Старый код для цветных частиц (на случай если что-то пойдет не так)
                alpha = int(255 * (particle['life'] / particle['max_life']))
                
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
                particle_surface.set_alpha(alpha)
                
                color = particle.get('color', (255, 255, 255))
                pygame.draw.circle(particle_surface, color, 
                                 (particle['size'], particle['size']), particle['size'])
                
                m.Disp.screen.blit(particle_surface, 
                                 (int(particle['x'] - particle['size']), 
                                  int(particle['y'] - particle['size'])))
    
    def square(self,m,center:tuple,size:float) -> list:
        
        z = m.config['zoom']

        points = []

        for pos in range(4):
            points.append((center[0] + math.cos(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*size*z,
                          center[1] + math.sin(math.pi*(self.rotate[0]+45)/180+math.pi/2*pos)*math.sin(math.pi*self.rotate[1]/180)*size*z))
        
        return points
    
    def chessboard(self,m):
        
        z = m.config['zoom']
        
        board = self.square(m,(m.Disp.width//2,m.Disp.height//2),400)
        boardcolor = m.Disp.colors['Game']['bg']
        if self.rotate[1] < 0:
            back = self.square(m,(m.Disp.width//2,m.Disp.height//2),283)
            boardcolor = m.Disp.colors['Game']['chessboard']

        pygame.draw.polygon(m.Disp.screen,boardcolor,board)
        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['light_cell'],board,1)
        if self.rotate[1] < 0:
            pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['dark_cell'],back)

            for y in range(8):
                for x in range(8):
                        
                    if m.PI.Game.cells[x][y]['status'] == 'selected':
                        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['selected_cell'],m.PI.Game.cells[x][y]['points'])
                    
                    elif m.PI.Game.cells[x][y]['status'] == 'move':
                        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['move_cell'],m.PI.Game.cells[x][y]['points'])
                    
                    elif m.PI.Game.cells[x][y]['status'] == 'attack':
                        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['attack_cell'],m.PI.Game.cells[x][y]['points'])

                    elif (x+y)%2 == 1:
                        pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['light_cell'],m.PI.Game.cells[x][y]['points'])
            
            #pygame.draw.polygon(m.Disp.screen,m.Disp.colors['Game']['chessboard'],back,3)
        
    def cells(self,m, offset=(0,0)):
        
        z = m.config['zoom']

        images = m.AssetManager.img
        cells = m.PI.Game.cells

        if self.rotate[0] > 90 or self.rotate[0] < -90:
            Y = range(8)
        else:
            Y = range(7,-1,-1)

        if self.rotate[0] > 0:
            X = range(7,-1,-1)
        else:
            X = range(8)

        for y in Y:
            for x in X:

                if cells[x][y]['value'] in images:
                    image = images[cells[x][y]['value']]
                    image = pygame.transform.scale(image, (50*z, 50*z))
                    if self.rotate[1] < -90 or self.rotate[1] > 90:
                        image = pygame.transform.flip(image, False, True)
                    image_size = image.get_size()
                    pos = [cells[x][y]['pos'][0]-image_size[0]/2 + offset[0],
                           cells[x][y]['pos'][1]-image_size[1] + image_size[1]/2*(self.rotate[1]/-90) + offset[1]]

                    # Лёгкий подскок выбранной фигуры
                    if m.PI.Game.selected_cell and [x,y] == m.PI.Game.selected_cell:
                        lift = 6
                        pos[1] -= lift
                    m.Disp.screen.blit(image,pos)
                
                if m.config['f3']:

                    pygame.draw.circle(m.Disp.screen,(255,255,0),(cells[x][y]['pos'][0]+offset[0],cells[x][y]['pos'][1]+offset[1]),5,1)
                    if cells[x][y]['value'] in images:pygame.draw.circle(m.Disp.screen,(255,0,255),(cells[x][y]['pos'][0]+offset[0],cells[x][y]['pos'][1] + image_size[1]/2*(self.rotate[1]/-90)+offset[1]),5,1)
                    pygame.draw.circle(m.Disp.screen,(0,255,255),pos,2,1)

    def start_shake(self, duration_ms:int, amplitude:int):
        self.shake_time_ms = duration_ms
        self.shake_amp = amplitude
        self.shake_seed = pygame.time.get_ticks()

    def update_shake(self, m):
        if self.shake_time_ms <= 0:
            return
        dt = m.Disp.clock.get_time()
        self.shake_time_ms = max(0, self.shake_time_ms - dt)