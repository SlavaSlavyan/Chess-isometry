import pygame
from pathlib import Path

class AssetManager:
    
    def __init__(self,m):
 
        self.loadimg(m)
    
    def loadimg(self,m):
        
        self.img = {}
        
        images = [f for f in Path('data\\assets').iterdir() if f.is_file() and f.suffix.lower() == '.png']
        
        for img in images:
            self.img[img] = pygame.image.load(img)
        
        print(self.img)