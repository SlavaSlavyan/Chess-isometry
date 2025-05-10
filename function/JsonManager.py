import json

class JsonManager:

    def __init__(self,m):
        m.config = self.load('data\\config')

    def load(self, path:str):
        
        try:

            with open(f'{path}.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            return data

        except Exception as err:
            print(f'[Error][JsonManager][Load]: {err}')

    def save(self, path:str, data: any):
        
        try:
          
            with open(f'{path}.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except Exception as err:
            print(f'[Error][JsonManager][Save]: {err}')