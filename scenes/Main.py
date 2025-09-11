from scenes.chess.Main import Main as Chess

class Main:

    def __init__(self,m):
        
        m.Log.write("Инициализация класса сцен.","DEBUG")
        
        m.Log.write("Загрузка всех сцен...","DEBUG")
        
        self.Chess = Chess(m)
        
        m.Log.write("Загрузка всех сцен завершена.","DEBUG")