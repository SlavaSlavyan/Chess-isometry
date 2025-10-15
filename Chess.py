VERSION = "2.1.0 DEV"
# Launch file

import datetime
import subprocess
import sys
import time

def crash_log(text: str):
    with open(f"Error {datetime.datetime.now().strftime('%Y.%m.%d %H-%M-%S')}.log","a",encoding='utf-8') as file:
        file.write(f"{text}\n")

try:
    from src.LogManager import Log
    StartLog = Log()
    
    StartLog.write(f"Program version: {VERSION}")
    
    logging = True
    
except Exception as err:
    
    crash_log(f"Сan not load the log class.\n{err}\n\nLogs will not be saved.")
    
    class StartLog:
        def write(text):
            print(text)
            
    logging = False
        
try:
    StartLog.write(f"Launching the loading screen.")
    loading_screen = subprocess.Popen([sys.executable,"src\\SimpleDisplay.py","loading_screen"])
    loading_screen_allow = True
    time.sleep(1)
    
except Exception as err:
    crash_log(f"Сan't display the loading screen.\n{err}")
    loading_screen_allow = False

try:
    StartLog.write(f"Loading the main module.")
    from src.Main import Main
    run = True

except Exception as err:
    crash_log(f"Сan not load the main module.\n{err}\n\nThe program will not start.")
    run = True

class ChessStart:
    
    def __init__(self):
        StartLog.write(f"Initializing the Start class.")
    
    def main(self):
        
        self.Chess = Main({
            "LogClass":StartLog
        })
        
        if loading_screen_allow:
            
            if loading_screen.poll() == None:
                loading_screen.terminate()
                self.Chess.start()
            
            else:
                print(0)
            
        else:
            print('n')
            self.Chess.start()
                
if __name__ == "__main__":
    
    if run:
        Start = ChessStart()
        Start.main()