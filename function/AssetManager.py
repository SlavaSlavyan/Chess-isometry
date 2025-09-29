import pygame
from pathlib import Path
import sys
import os

class AssetManager:
    
    def __init__(self,m):
 
        self.loadimg(m)
        self.old_zoom = m.config['zoom']
    
    def get_resource_path(self, relative_path):
        """Получить абсолютный путь к ресурсу, работает как в разработке, так и в PyInstaller"""
        if hasattr(sys, '_MEIPASS'):
            # Запущено из PyInstaller
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            # Запущено в обычном режиме
            return relative_path
    
    def loadimg(self,m):

        self.img = {}

        assets_path = self.get_resource_path('data/assets')
        assets_dir = Path(assets_path)
        
        if assets_dir.exists():
            for png_file in assets_dir.glob('*.png'):
                self.img[png_file.stem] = str(png_file)

        for key,value in self.img.items():
            self.img[key] = pygame.image.load(value)
    
    def check_new_zoom(self,m):

        if self.old_zoom != m.config['zoom']:

            self.loadimg(m)
            self.old_zoom = m.config['zoom']