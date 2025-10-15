# Main class

import src.GL as GL

class Main:
    
    def __init__(self, args: dict):

        self.Log = args['LogClass']
        self.Log.write("Initialization of the main program class...")
        
        self.Log.write("Initializing the OpenGL class")
        self.GL = GL

        self.Log.write("End of initialization of the main class.\n")

    def main(self):
        pass
    
    def start(self):

        self.Log.write("="*20 + f"START" + "="*20 + "\n")

        self.stop()
    
    def stop(self):

        self.Log.write("="*21 + f"END" + "="*21)