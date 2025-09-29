import pygame
import math
import sys
import os

class AvatarEditor:
    """Редактор аватаров с возможностью перемещения и масштабирования"""
    
    def __init__(self):
        # Состояние редактора
        self.active = False
        self.image_path = None
        self.original_image = None
        self.preview_image = None
        
        # Параметры изображения
        self.image_x = 0
        self.image_y = 0
        self.image_scale = 1.0
        self.min_scale = 0.1  # Позволяем уменьшать до 10% от оригинала
        self.max_scale = 5.0  # Увеличиваем максимум тоже
        
        # Параметры области редактирования
        self.editor_size = 200  # Размер области редактирования
        self.preview_size = 64  # Финальный размер аватара
        
        # Состояние взаимодействия
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        
        # Кнопки
        self.buttons = {}
        
        # Шрифты
        try:
            self.title_font = pygame.font.Font(self.get_resource_path('data/font/title.ttf'), 24)
            self.text_font = pygame.font.Font(self.get_resource_path('data/font/text.ttf'), 16)
        except:
            self.title_font = pygame.font.Font(None, 24)
            self.text_font = pygame.font.Font(None, 16)
    
    def get_resource_path(self, relative_path):
        """Получить абсолютный путь к ресурсу"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            return relative_path
    
    def start_editing(self, image_path: str) -> bool:
        """Начинает редактирование изображения"""
        try:
            # Загружаем изображение
            self.original_image = pygame.image.load(image_path)
            self.image_path = image_path
            
            # Сбрасываем параметры
            self.image_x = 0
            self.image_y = 0
            
            # Подбираем начальный масштаб чтобы изображение помещалось
            img_w, img_h = self.original_image.get_size()
            scale_x = self.editor_size / img_w
            scale_y = self.editor_size / img_h
            
            # Выбираем масштаб который позволит изображению поместиться
            auto_scale = min(scale_x, scale_y, 1.0)
            self.image_scale = auto_scale  # Используем автоматически вычисленный масштаб
            
            # Центрируем изображение
            scaled_w = int(img_w * self.image_scale)
            scaled_h = int(img_h * self.image_scale)
            self.image_x = (self.editor_size - scaled_w) // 2
            self.image_y = (self.editor_size - scaled_h) // 2
            
            print(f"🎯 Начальный масштаб: auto={auto_scale:.3f}, final={self.image_scale:.3f}")
            
            self.active = True
            print(f"🎨 Редактор аватара: {image_path}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка загрузки изображения: {e}")
            return False
    
    def update_preview(self):
        """Обновляет предпросмотр изображения"""
        if not self.original_image:
            return
        
        # Масштабируем изображение
        img_w, img_h = self.original_image.get_size()
        scaled_w = int(img_w * self.image_scale)
        scaled_h = int(img_h * self.image_scale)
        
        if scaled_w > 0 and scaled_h > 0:
            self.preview_image = pygame.transform.scale(self.original_image, (scaled_w, scaled_h))
        else:
            self.preview_image = self.original_image.copy()
    
    def handle_input(self, events, mouse_pos, screen_size=(1200, 800)):
        """Обрабатывает пользовательский ввод"""
        if not self.active:
            return None
        
        # Получаем правильные размеры экрана
        screen_w, screen_h = screen_size
        editor_rect = self.get_editor_rect(screen_w, screen_h)
        
        # Проверяем наведение на кнопки
        hover = None
        for name, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                hover = name
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка
                    if hover == "confirm":
                        return "confirm"
                    elif hover == "cancel":
                        return "cancel"
                    elif hover == "reset":
                        self.reset_position()
                    else:
                        # Начинаем перетаскивание
                        if editor_rect.collidepoint(mouse_pos):
                            self.dragging = True
                            self.last_mouse_pos = mouse_pos
                            print(f"🖱️ Начинаем перетаскивание в {mouse_pos}")
                
                elif event.button == 4:  # Колесо вверх - увеличить
                    if editor_rect.collidepoint(mouse_pos):
                        print(f"🔍 Увеличение (кнопка 4) в {mouse_pos}")
                        self.zoom_in(mouse_pos, editor_rect)
                elif event.button == 5:  # Колесо вниз - уменьшить
                    if editor_rect.collidepoint(mouse_pos):
                        print(f"🔍 Уменьшение (кнопка 5) в {mouse_pos}")
                        self.zoom_out(mouse_pos, editor_rect)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    # Перемещаем изображение
                    dx = mouse_pos[0] - self.last_mouse_pos[0]
                    dy = mouse_pos[1] - self.last_mouse_pos[1]
                    self.image_x += dx
                    self.image_y += dy
                    self.last_mouse_pos = mouse_pos
            
            elif event.type == pygame.MOUSEWHEEL:
                # Обработка колесика мыши (современный способ)
                if editor_rect.collidepoint(mouse_pos):
                    print(f"🎡 Колесико мыши: y={event.y} в {mouse_pos}, масштаб: {self.image_scale}")
                    if event.y > 0:  # Прокрутка вверх - увеличить
                        self.zoom_in(mouse_pos, editor_rect)
                    elif event.y < 0:  # Прокрутка вниз - уменьшить
                        self.zoom_out(mouse_pos, editor_rect)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "confirm"
                elif event.key == pygame.K_ESCAPE:
                    return "cancel"
                elif event.key == pygame.K_r:
                    self.reset_position()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # Альтернативный способ увеличения
                    print("🔍 Увеличение через клавишу +")
                    self.zoom_in(mouse_pos, editor_rect)
                elif event.key == pygame.K_MINUS:
                    # Альтернативный способ уменьшения
                    print("🔍 Уменьшение через клавишу -")
                    self.zoom_out(mouse_pos, editor_rect)
        
        return hover
    
    def zoom_in(self, mouse_pos, editor_rect):
        """Увеличивает масштаб"""
        old_scale = self.image_scale
        if self.image_scale < self.max_scale:
            self.image_scale = min(self.max_scale, self.image_scale * 1.1)
            
            # Масштабируем относительно центра области редактирования
            center_x = editor_rect.centerx
            center_y = editor_rect.centery
            
            # Вычисляем смещение для центрирования масштабирования
            scale_factor = self.image_scale / old_scale
            offset_x = (center_x - editor_rect.x - self.image_x) * (scale_factor - 1)
            offset_y = (center_y - editor_rect.y - self.image_y) * (scale_factor - 1)
            
            self.image_x -= int(offset_x * 0.5)  # Уменьшаем смещение для более плавного зума
            self.image_y -= int(offset_y * 0.5)
            
            print(f"✅ Увеличение: {old_scale:.2f} -> {self.image_scale:.2f}")
        else:
            print(f"⚠️ Максимальный масштаб достигнут: {self.image_scale:.2f}")
    
    def zoom_out(self, mouse_pos, editor_rect):
        """Уменьшает масштаб"""
        old_scale = self.image_scale
        
        # Вычисляем новый масштаб
        new_scale = self.image_scale / 1.1
        
        # Проверяем что новый масштаб не меньше минимального
        if new_scale >= self.min_scale:
            self.image_scale = new_scale
            
            # Масштабируем относительно центра области редактирования
            center_x = editor_rect.centerx
            center_y = editor_rect.centery
            
            # Вычисляем смещение для центрирования масштабирования
            scale_factor = self.image_scale / old_scale
            offset_x = (center_x - editor_rect.x - self.image_x) * (scale_factor - 1)
            offset_y = (center_y - editor_rect.y - self.image_y) * (scale_factor - 1)
            
            self.image_x -= int(offset_x * 0.5)  # Уменьшаем смещение для более плавного зума
            self.image_y -= int(offset_y * 0.5)
            
            print(f"✅ Уменьшение: {old_scale:.2f} -> {self.image_scale:.2f}")
        else:
            print(f"⚠️ Минимальный масштаб достигнут: {self.image_scale:.2f} (min: {self.min_scale})")
    
    def reset_position(self):
        """Сбрасывает позицию и масштаб"""
        if not self.original_image:
            return
        
        # Подбираем масштаб чтобы изображение помещалось
        img_w, img_h = self.original_image.get_size()
        scale_x = self.editor_size / img_w
        scale_y = self.editor_size / img_h
        
        # Выбираем масштаб который позволит изображению поместиться
        auto_scale = min(scale_x, scale_y, 1.0)
        self.image_scale = auto_scale  # Используем автоматически вычисленный масштаб
        
        # Центрируем
        scaled_w = int(img_w * self.image_scale)
        scaled_h = int(img_h * self.image_scale)
        self.image_x = (self.editor_size - scaled_w) // 2
        self.image_y = (self.editor_size - scaled_h) // 2
        
        print(f"🔄 Сброс: масштаб установлен в {self.image_scale:.3f}")
    
    def get_editor_rect(self, screen_w, screen_h):
        """Возвращает прямоугольник области редактирования"""
        x = (screen_w - self.editor_size) // 2
        y = (screen_h - self.editor_size) // 2 - 30
        return pygame.Rect(x, y, self.editor_size, self.editor_size)
    
    def get_cropped_image(self):
        """Возвращает обрезанное изображение аватара"""
        if not self.original_image:
            return None
        
        try:
            # Создаем поверхность финального размера сразу
            final_surface = pygame.Surface((self.preview_size, self.preview_size), pygame.SRCALPHA)
            final_surface.fill((0, 0, 0, 0))  # Прозрачный фон
            
            # Масштабируем изображение
            img_w, img_h = self.original_image.get_size()
            scaled_w = int(img_w * self.image_scale)
            scaled_h = int(img_h * self.image_scale)
            
            if scaled_w > 0 and scaled_h > 0:
                scaled_image = pygame.transform.smoothscale(self.original_image, (scaled_w, scaled_h))
                
                # Вычисляем масштабный коэффициент для перехода от области редактирования к финальному размеру
                scale_factor = self.preview_size / self.editor_size
                
                # Позиция изображения на финальной поверхности
                final_x = int(self.image_x * scale_factor)
                final_y = int(self.image_y * scale_factor)
                final_img_w = int(scaled_w * scale_factor)
                final_img_h = int(scaled_h * scale_factor)
                
                # Масштабируем изображение для финальной поверхности
                if final_img_w > 0 and final_img_h > 0:
                    final_image = pygame.transform.smoothscale(scaled_image, (final_img_w, final_img_h))
                    
                    # Рисуем изображение на финальной поверхности
                    final_surface.blit(final_image, (final_x, final_y))
            
            # Теперь делаем круглую обрезку
            # Создаем временную поверхность для маскирования
            temp_surface = pygame.Surface((self.preview_size, self.preview_size), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 0))
            
            # Копируем только круглую область
            center = self.preview_size // 2
            radius = self.preview_size // 2
            
            for x in range(self.preview_size):
                for y in range(self.preview_size):
                    dx = x - center
                    dy = y - center
                    if dx*dx + dy*dy <= radius*radius:
                        pixel = final_surface.get_at((x, y))
                        temp_surface.set_at((x, y), pixel)
            
            # Добавляем рамку
            pygame.draw.circle(temp_surface, (50, 50, 50), (center, center), radius, 2)
            
            return temp_surface
            
        except Exception as e:
            print(f"❌ Ошибка создания аватара: {e}")
            return None
    
    def draw(self, screen, screen_w, screen_h, colors):
        """Рисует интерфейс редактора"""
        if not self.active:
            return
        
        # Полупрозрачный фон
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Основное окно редактора
        window_w, window_h = 400, 350
        window_x = (screen_w - window_w) // 2
        window_y = (screen_h - window_h) // 2
        
        # Фон окна
        window_rect = pygame.Rect(window_x, window_y, window_w, window_h)
        pygame.draw.rect(screen, colors['bg'], window_rect, border_radius=10)
        pygame.draw.rect(screen, colors['light_cell'], window_rect, 3, border_radius=10)
        
        # Заголовок
        title_text = self.title_font.render("РЕДАКТОР АВАТАРА", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=window_x + window_w//2, y=window_y + 15)
        screen.blit(title_text, title_rect)
        
        # Область редактирования
        editor_rect = self.get_editor_rect(screen_w, screen_h)
        editor_rect.x = window_x + (window_w - self.editor_size) // 2
        editor_rect.y = window_y + 50
        
        # Фон области редактирования
        pygame.draw.rect(screen, (40, 40, 40), editor_rect)
        pygame.draw.rect(screen, colors['chessboard'], editor_rect, 2)
        
        # Сетка для лучшей видимости
        grid_color = (60, 60, 60)
        for i in range(0, self.editor_size, 20):
            pygame.draw.line(screen, grid_color, 
                           (editor_rect.x + i, editor_rect.y), 
                           (editor_rect.x + i, editor_rect.bottom))
            pygame.draw.line(screen, grid_color, 
                           (editor_rect.x, editor_rect.y + i), 
                           (editor_rect.right, editor_rect.y + i))
        
        # Рисуем изображение
        if self.original_image:
            self.update_preview()
            if self.preview_image:
                screen.blit(self.preview_image, (editor_rect.x + self.image_x, editor_rect.y + self.image_y))
        
        # Круглая рамка области обрезки
        center_x = editor_rect.centerx
        center_y = editor_rect.centery
        radius = self.editor_size // 2 - 5
        
        # Затемняем области вне круга
        mask_surface = pygame.Surface((self.editor_size, self.editor_size), pygame.SRCALPHA)
        mask_surface.fill((0, 0, 0, 100))
        pygame.draw.circle(mask_surface, (0, 0, 0, 0), (self.editor_size//2, self.editor_size//2), radius)
        screen.blit(mask_surface, editor_rect)
        
        # Рамка обрезки
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius, 2)
        pygame.draw.circle(screen, (100, 100, 100), (center_x, center_y), radius + 1, 1)
        
        # Предпросмотр финального аватара
        preview_x = window_x + window_w - 80
        preview_y = window_y + 60
        
        final_avatar = self.get_cropped_image()
        if final_avatar:
            screen.blit(final_avatar, (preview_x, preview_y))
        
        preview_label = self.text_font.render("Результат:", True, (200, 200, 200))
        screen.blit(preview_label, (preview_x - 10, preview_y - 20))
        
        # Инструкции
        instructions = [
            "Перетаскивайте мышью",
            "Колесико - масштаб",
            "R - сброс позиции"
        ]
        
        y_offset = window_y + window_h - 100
        for instruction in instructions:
            text = self.text_font.render(instruction, True, (180, 180, 180))
            text_rect = text.get_rect(centerx=window_x + window_w//2, y=y_offset)
            screen.blit(text, text_rect)
            y_offset += 18
        
        # Кнопки
        button_w, button_h = 80, 30
        buttons_y = window_y + window_h - 45
        
        self.buttons = {
            "cancel": pygame.Rect(window_x + 20, buttons_y, button_w, button_h),
            "reset": pygame.Rect(window_x + window_w//2 - button_w//2, buttons_y, button_w, button_h),
            "confirm": pygame.Rect(window_x + window_w - button_w - 20, buttons_y, button_w, button_h)
        }
        
        button_labels = {
            "cancel": "ОТМЕНА",
            "reset": "СБРОС", 
            "confirm": "ГОТОВО"
        }
        
        button_colors = {
            "cancel": (150, 50, 50),
            "reset": (100, 100, 100),
            "confirm": (50, 150, 50)
        }
        
        for name, rect in self.buttons.items():
            color = button_colors.get(name, colors['dark_cell'])
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, colors['chessboard'], rect, 2, border_radius=5)
            
            label = self.text_font.render(button_labels[name], True, (255, 255, 255))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)
    
    def close(self):
        """Закрывает редактор"""
        self.active = False
        self.original_image = None
        self.preview_image = None
        self.image_path = None
