import pygame

class Settings:
    
    def __init__(self, m):
        self.sliders = {}
        self.buttons = {}
        self.hover = None
        self.dragging_slider = None
        
    def main(self, m):
        self.layout(m)
        self.handle_input(m)
    
    def layout(self, m):
        width, height = m.Disp.width, m.Disp.height
        
        # Слайдеры громкости
        slider_w = 200
        slider_h = 20
        slider_x = width//2 - slider_w//2
        
        self.sliders = {
            "music": {
                "rect": pygame.Rect(slider_x, height//2 - 80, slider_w, slider_h),
                "value": m.AudioManager.music_volume,
                "label": "Music Volume"
            },
            "sfx": {
                "rect": pygame.Rect(slider_x, height//2 - 10, slider_w, slider_h),
                "value": m.AudioManager.sfx_volume,
                "label": "SFX Volume"
            }
        }
        
        # Кнопки (размещаем ниже слайдеров с большим отступом)
        btn_w, btn_h = int(width*0.22), 48
        cx = width//2 - btn_w//2
        
        self.buttons = {
            "fullscreen": pygame.Rect(cx, height//2 + 80, btn_w, btn_h),
            "back": pygame.Rect(cx, height//2 + 140, btn_w, btn_h)
        }
    
    def handle_input(self, m):
        mouse_pos = m.PI.MI.mouse_pos
        self.hover = None
        
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
            if self.hover == "fullscreen":
                m.config['fullscreen'] = not m.config['fullscreen']
                m.Disp.reload_screen_mode(m)
            elif self.hover == "back":
                m.set_scene('menu')
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
