# Файл запуска программы.

import subprocess
import traceback

try:
    loading = subprocess.Popen(['python', 'func\\Loading.py'])
    loading_screen = True
except:
    print("$НЕТ ЭКРАНА ЗАГРУЗКИ!")
    loading_screen = False

try:

    from func.Main import Main

    Chess = Main({"vers":"1.0.5"})

    if loading_screen:
        loading.terminate()

    while True:
        
        Chess.main()

except Exception as err:

    try:
        Chess.Log.write(f"Ошибка в основном цикле!\n\n{traceback.format_exc()}.","WARNING")
        Chess.stop()
    except:
        print(f"Не удалось вывести ошибку в логи!\n\n{traceback.format_exc()}.")

    if loading_screen:
        loading.terminate()

    from func.Error import Error

    err_screen = Error()
    err_screen.main(traceback.format_exc())
