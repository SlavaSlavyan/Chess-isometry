VERSION = "2.1.3 DEV"
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
    
    error_text = f"Error #{error_id} {datetime.datetime.now().strftime('%H:%M:%S')}\n\n{text}\n\n{traceback.format_exc()}" + "-"*50 + "\n"
    
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
    
    crash_log(f"Сan not load the log class.\nPython:{err}\nLogs will not be saved.",0)
    
    class StartLog:
        def write(text,str_type='debug'):
            print(str_type,text)
            
    # The class is a dummy so that the rest of 
    # the code doesn't fail due to the lack of logs
            
    logging = False
    
# --------------------------------------------------------------------------------------------------------------------------------- #

# function for opening simple windows

def new_simple_display(screen: str) -> any | None:
    '''
        ### Calls a function inside src\\SimpleDisplay.py
        - **screen** - ID of the screen to be displayed
        - **add_info** - Some functions require additional information to work correctly
        
        Available functions:
        - *loading_screen*
        - *crash_log_screen* [ADDITIONAL INFORMATION NEEDED] - crash log
    '''
    
    try:
        
        StartLog.write(f"Launching the Simple display screen id:{screen}.")
        s_disp = subprocess.Popen([sys.executable,"src\\SimpleDisplay.py",screen],
                                        stderr=subprocess.PIPE,
                                        text=True)

        time.sleep(1)
        
        if s_disp.poll() == None:
            return s_disp
            
        else:
            # s_disp.communicate()[1] will communicate 
            # the error that was inside simple display
            raise ValueError(s_disp.communicate()[1])
        
    except Exception as err:
        
        error_info = f"Error opening new simple display with args:{screen}.\nPython:{err}"
        StartLog.write(error_info,"error")
        crash_log(error_info,1)
        
        return None

# Let's create a loading screen right away
loading_screen = new_simple_display("loading_screen")

# --------------------------------------------------------------------------------------------------------------------------------- #

# Importing the main module
try:
    
    StartLog.write(f"Loading the main module.")
    from src.Main import Main
    
    run = True

except Exception as err:
    
    error_info = f"Сan not load the main module.\nPython:{err}\nThe program will not start."
    StartLog.write(error_info,"warning")
    crash_log(error_info,2)
    new_simple_display("crash_log_screen")
    
    run = False
    
    # closing the loading window
    if loading_screen != None: loading_screen.terminate()

# --------------------------------------------------------------------------------------------------------------------------------- #

# Class to start the game

class ChessStart:
    
    def __init__(self):
        StartLog.write(f"Initializing the Start class.")
    
    def main(self):
        '''
            This function is responsible for launching the game
        '''
        
        start_allow = self.init_main_class()
        
        if start_allow: self.start_main_class()
    
    def init_main_class(self) -> bool:
        
        try:
            
            self.Chess = Main({
                "LogClass":StartLog
            })
            
            return True
            
        except Exception as err:
            
            error_info = f"Error in initialization of main class\nPython:{err}\nThe program will not start."
            StartLog.write(error_info,"warning")
            crash_log(error_info,3)
            new_simple_display("crash_log_screen")
            if loading_screen != None: loading_screen.terminate()
            
            return False
    
    def start_main_class(self):
        
        try:
        
            if loading_screen != None:
                
                # There's a slight delay to ensure 
                # the loading screen appears
                time.sleep(1)
                
                if loading_screen.poll() == None:
                    
                    loading_screen.terminate()
                    self.Chess.start()
                
                else:
                    self.Chess.Log.write("The user interrupted the boot cycle. The program will not start.","info")
                
            else:

                self.Chess.start()
        
        except:
            
            error_info = f"Error in the main program loop\nPython:{err}\nThe program will end."
            StartLog.write(error_info,"warning")
            crash_log(error_info)
            new_simple_display("crash_log_screen")

# --------------------------------------------------------------------------------------------------------------------------------- #

# Well, I think everything is clear here 
# (_　_)。゜zｚＺ

if __name__ == "__main__":
    
    if run:
        Start = ChessStart()
        Start.main()