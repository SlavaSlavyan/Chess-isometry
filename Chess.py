VERSION = "2.1.1 DEV"
# Launch file

import datetime
import subprocess
import sys
import time
import traceback

# Crash log function
def crash_log(text: str, error_id: int = "Unexpected") -> str:
    '''
        - **text** - Brief description of the error
        - **error_id** - Specifies the error ID
        
        The function has a built-in **traceback**
        
        Returns a **formatted error string** if it needs to be sent elsewhere.
    '''
    
    error_text = f"Error #{error_id} {datetime.datetime.now().strftime('%H:%M:%S')}\n\n{text}\n\n{traceback.format_exc()}" + "-"*50
    
    with open(f"Crash report {datetime.datetime.now().strftime('%Y.%m.%d %H-%M-%S')}.log","a",encoding='utf-8') as file:
        file.write(error_text)
        
    with open(f"Crash report ALL.log","a",encoding='utf-8') as file:
        file.write(error_text)
    
    return error_text

# --------------------------------------------------------------------------------------------------------------------------------- #

# Importing logs
try:
    
    from src.LogManager import Log
    StartLog = Log()
    
    StartLog.write(f"Program version: {VERSION}")
    
    logging = True
    
except Exception as err:
    
    crash_log(f"Сan not load the log class.\nPython:{err}\nLogs will not be saved.")
    
    class StartLog:
        def write(text,str_type='debug'):
            print(str_type,text)
            
    # The class is a dummy so that the rest of 
    # the code doesn't fail due to the lack of logs
            
    logging = False
    
# --------------------------------------------------------------------------------------------------------------------------------- #

# Loading loading screen 
# DUHH
try:
    
    StartLog.write(f"Launching the loading screen.")
    loading_screen = subprocess.Popen([sys.executable,"src\\SimpleDisplay.py","loading_screen"],
                                      stderr=subprocess.PIPE,
                                      text=True)
    
    # A little delay just to be sure everything is ok
    time.sleep(1) 
    
    if loading_screen.poll() == None:
        loading_screen_allow = True
        
    else:
        # Loading_screen.communicate()[1] will communicate 
        # the error that was inside loading_screen
        raise ValueError(loading_screen.communicate()[1])
    
except Exception as err:
    
    StartLog.write("Сan't display the loading screen.","error")
    crash_log(f"Сan't display the loading screen.\nPython:{err}")
    
    loading_screen_allow = False

# --------------------------------------------------------------------------------------------------------------------------------- #

# Importing the main module
try:
    
    StartLog.write(f"Loading the main module.")
    from src.Main import Main
    
    run = True

except Exception as err:
    
    crash_log(f"Сan not load the main module.\nPython:{err}\nThe program will not start.")
    
    run = False
    
    # closing the loading window
    if loading_screen_allow: loading_screen.terminate()

# --------------------------------------------------------------------------------------------------------------------------------- #


class ChessStart:
    
    def __init__(self):
        StartLog.write(f"Initializing the Start class.")
    
    def main(self):
        
        start_allow = self.init_main_class()
        
        if start_allow: self.start_main_class()
    
    def init_main_class(self) -> bool:
        
        try:
            
            self.Chess = Main({
                "LogClass":StartLog
            })
            
            return True
            
        except Exception as err:
            
            crash_log(f"Error in initialization of main class\n{err}\n\nThe program will not start.\n\n{traceback.format_exc()}")
            if loading_screen_allow: loading_screen.terminate()
            
            return False
    
    def start_main_class(self):
        
        if loading_screen_allow:
            
            if loading_screen.poll() == None:
                loading_screen.terminate()
                self.Chess.start()
            
            else:
                self.Chess.Log.write("The user interrupted the boot cycle. The program will not start.")
            
        else:

            self.Chess.start()

# --------------------------------------------------------------------------------------------------------------------------------- #
                
if __name__ == "__main__":
    
    if run:
        Start = ChessStart()
        Start.main()