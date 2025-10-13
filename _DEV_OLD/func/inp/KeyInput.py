import pygame

class KeyInput:

    def __init__(self,m):

        m.Log.write("   |Инициализация класса эвентов клавиатуры.","DEBUG")

        self.keys = m.Json.load(m,"data\\keys",True)

        for name,id in self.keys.items():
            
            self.keys[name] = {"id":id,"press":False,"hold":False,"release":False}

    def main(self,m,event):

        if event.type == pygame.KEYDOWN:
            
            for name,value in self.keys.items():
            
                if event.key == value['id']:
                    
                    self.keys[name]['press'] = True
                    self.keys[name]['hold'] = True

                    m.Log.write(f"[1] Клавиша {name} id:{value['id']} была зажата.")

            m.Log.write(f"Key: {event.key}.","DEBUG")
            
        if event.type == pygame.KEYUP:
            
            for name,value in self.keys.items():
            
                if event.key == value['id']:
                    
                    self.keys[name]['release'] = True
                    self.keys[name]['hold'] = False

                    m.Log.write(f"[0] Клавиша {name} id:{value['id']} больше не зажата.")