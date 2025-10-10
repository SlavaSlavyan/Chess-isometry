VERSION = "2.0.2 DEV"
# Файл запуска

error_log = []

try:
    from multiprocessing import Process
    from pathlib import Path
    
except: 
    start_allow = False
    error_log.append("P0")
    # Если библиотеки python не удаётся загрузить, программа не даст разрешение на запуск.

# Импорт ГЛАВНОГО класса программы.
try:
    from src.Main import Main
    start_allow = True
except: 
    error_log.append("M0")
    start_allow = False 
    # Если главный модуль не удаётся загрузить, программа не даст разрешение на запуск.


if start_allow:
    
    class ChessStart:
        
        def __init__(self):
            
            self.Chess = Main() # Экземпляр основного класса.
        
        def main(self):

            # Основной цикл.
            self.Chess.start()