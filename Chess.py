VERSION = "2.0.3 DEV"
# Файл запуска
import time

from multiprocessing import Process, Manager

from src.Main import Main
from src.SimpleDisplay import SimpleDisplay
    
class ChessStart:
        
    def __init__(self):
            
        self.SplDisp = SimpleDisplay()
        
    def main(self):

        with Manager() as manager:

            LoadingScreen = Process(target=self.SplDisp.loading_screen)
            LoadingScreen.start()

            self.Chess = Main()

            if LoadingScreen.is_alive():

                print(1)
                LoadingScreen.terminate()
                self.Chess.start()
            
            else:
                print('err')

if __name__ == "__main__":

    SLL = ChessStart()
    SLL.main()