from scenes.chess.Display import Display
from scenes.chess.Function import Function

class Main:

    def __init__(self,m):
        
        m.Log.write("   |Инициализация сцены Chess.")
        
        self.Disp = Display(m)
        self.Func = Function(m)