import pygame

class Settings:
    
    def __init__(self, m):
        self.sliders = {}
        self.buttons = {}
        self.tabs = {}
        self.active_tab = 'Audio'
        self.hover = None
        self.dragging_slider = None
        
    def main(self, m):
        self.layout(m)
        self.handle_input(m)
    
    def layout(self, m):
        width, height = m.Disp.width, m.Disp.height
        
        # Вкладки настроек
        tab_w = int(width * 0.18)
        tab_h = 40
        spacing = 16
        tabs_total_w = tab_w * 3 + spacing * 2
        start_x = width//2 - tabs_total_w//2
        tabs_y = int(height * 0.28)
        self.tabs = {
            'General': pygame.Rect(start_x + (tab_w + spacing) * 0, tabs_y, tab_w, tab_h),
            'Audio':   pygame.Rect(start_x + (tab_w + spacing) * 1, tabs_y, tab_w, tab_h),
            'Display': pygame.Rect(start_x + (tab_w + spacing) * 2, tabs_y, tab_w, tab_h),
        }
        
        # Область контента под вкладками (единая зона)
        content_center_x = width // 2
        base_y = tabs_y + tab_h + 60
        
        # Значения по умолчанию для новых ключей конфига
        bg_mode = m.config.get('bg_mode', '3d')
        if bg_mode not in ('2d', '3d'):
            bg_mode = '3d'
            m.config['bg_mode'] = bg_mode
        
        # Общие размеры контролов
        slider_w = 300
        slider_h = 20
        slider_x = content_center_x - slider_w//2
        btn_w, btn_h = int(width*0.22), 48
        cx = width//2 - btn_w//2
        
        # Заполняем элементы управления в зависимости от активной вкладки
        self.sliders = {}
        self.buttons = {}
        
        if self.active_tab == 'Audio':
            self.sliders = {
                "music": {
                    "rect": pygame.Rect(slider_x, base_y, slider_w, slider_h),
                    "value": m.AudioManager.music_volume,
                    "label": "Music Volume"
                },
                "sfx": {
                    "rect": pygame.Rect(slider_x, base_y + 80, slider_w, slider_h),
                    "value": m.AudioManager.sfx_volume,
                    "label": "SFX Volume"
                }
            }
        elif self.active_tab == 'Display':
            self.buttons = {
                "fullscreen": pygame.Rect(cx, base_y, btn_w, btn_h),
                "bg_mode": pygame.Rect(cx, base_y + 60, btn_w, btn_h)
            }
        else:  # General
            self.buttons = {
                "f3_toggle": pygame.Rect(cx, base_y, btn_w, btn_h)
            }
        
        # Кнопка "назад" всегда внизу независимо от вкладки
        self.buttons["back"] = pygame.Rect(cx, height - 120, btn_w, btn_h)
    
    def handle_input(self, m):
        mouse_pos = m.PI.MI.mouse_pos
        self.hover = None
        
        # Наведение на вкладки
        for name, rect in self.tabs.items():
            if rect.collidepoint(mouse_pos):
                self.hover = f"tab_{name}"
        
        # Проверяем наведение на кнопки
        for name, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                self.hover = name
        
        # Проверяем наведение на слайдеры
        for name, slider in self.sliders.items():
            if slider["rect"].collidepoint(mouse_pos):
                self.hover = f"slider_{name}"
        
        # Обработка кликов
        if m.PI.MI.mouse_click['lt']:
            # Переключение вкладки
            if self.hover and self.hover.startswith("tab_"):
                tab = self.hover[4:]
                if tab in self.tabs:
                    self.active_tab = tab
                    self.layout(m)
                    return
            
            if self.hover == "fullscreen":
                m.config['fullscreen'] = not m.config['fullscreen']
                m.Disp.reload_screen_mode(m)
            elif self.hover == "bg_mode":
                # Переключение режима фона 2D/3D
                current = m.config.get('bg_mode', '3d')
                m.config['bg_mode'] = '2d' if current == '3d' else '3d'
                m.JsonManager.save("data\\config", m.config)
            elif self.hover == "back":
                m.set_scene('menu')
            elif self.hover == "f3_toggle":
                m.config['f3'] = not m.config.get('f3', False)
                m.JsonManager.save("data\\config", m.config)
            elif self.hover and self.hover.startswith("slider_"):
                slider_name = self.hover[7:]  # убираем "slider_"
                self.dragging_slider = slider_name
        
        # Обработка перетаскивания слайдеров
        if self.dragging_slider and m.PI.MI.mouse['lt']:
            slider = self.sliders[self.dragging_slider]
            rect = slider["rect"]
            relative_x = mouse_pos[0] - rect.x
            value = max(0.0, min(1.0, relative_x / rect.width))
            slider["value"] = value
            
            # Применяем значение
            if self.dragging_slider == "music":
                m.AudioManager.set_music_volume(value)
                m.config['music_volume'] = value
            elif self.dragging_slider == "sfx":
                m.AudioManager.set_sfx_volume(value)
                m.config['sfx_volume'] = value
        
        # Останавливаем перетаскивание
        if not m.PI.MI.mouse['lt']:
            self.dragging_slider = None
