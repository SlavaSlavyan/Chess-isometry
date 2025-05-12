import pygame
from pathlib import Path

class AssetManager:
    
    def __init__(self,m):
 
        self.loadimg(m)
    
    def loadimg(self,m):

        self.img = {}

        for png_file in Path('data\\assets').glob('*.png'):
            self.img[png_file.stem] = str(png_file)

        for key,value in self.img.items():
            self.img[key] = pygame.image.load(value)