import json
import sys
import os

class JsonManager:

    def __init__(self,m):
        m.config = self.load('data/config')
        if m.config is None:
            # Если не удалось загрузить, используем дефолтные значения
            m.config = {
                'fullscreen': False,
                'start-size': [1200, 800],
                'them': 'base',
                'zoom': 1.0,
                'f3': False,
                'bg_mode': '2d',
                'music_volume': 0.5,
                'sfx_volume': 0.5,
                'engine': 'pygame'
            }

    def get_resource_path(self, relative_path):
        """Получить абсолютный путь к ресурсу, работает как в разработке, так и в PyInstaller"""
        if hasattr(sys, '_MEIPASS'):
            # Запущено из PyInstaller
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            # Запущено в обычном режиме
            return relative_path

    def load(self, path:str):
        
        try:
            full_path = self.get_resource_path(f'{path}.json')
            # Сначала пробуем utf-8-sig (удаляет BOM если есть)
            try:
                with open(full_path, 'r', encoding='utf-8-sig') as file:
                    data = json.load(file)
            except:
                # Если не получилось, пробуем обычный utf-8
                with open(full_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            
            return data

        except Exception as err:
            print(f'[Error][JsonManager][Load]: {err}')
            return None  # Возвращаем None явно при ошибке

    def save(self, path:str, data: any):
        
        try:
            # Для сохранения используем обычный путь (в папке пользователя или рабочей директории)
            with open(f'{path}.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except Exception as err:
            print(f'[Error][JsonManager][Save]: {err}')