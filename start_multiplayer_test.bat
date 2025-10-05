@echo off
chcp 65001 >nul
echo ======================================
echo    CHESS ISOMETRY MULTIPLAYER TEST
echo ======================================
echo.
echo Starting PLAYER 1 (2D mode)...
start "Player 1 - 2D" cmd /k "python Chess.pyw"
echo.
timeout /t 3 /nobreak >nul
echo.
echo Switching to 3D mode for Player 2...
python -c "import json; f=open('data/config.json','r',encoding='utf-8'); d=json.load(f); f.close(); d['engine']='panda3d'; f=open('data/config.json','w',encoding='utf-8'); json.dump(d,f,indent=4); f.close()"
timeout /t 1 /nobreak >nul
echo.
echo Starting PLAYER 2 (3D mode)...
start "Player 2 - 3D" cmd /k "python Chess.pyw"
echo.
echo ======================================
echo   Both players started!
echo   Player 1: 2D (White pieces)
echo   Player 2: 3D (Black pieces)
echo ======================================
echo.
echo Press any key to restore 2D mode...
pause >nul
python -c "import json; f=open('data/config.json','r',encoding='utf-8'); d=json.load(f); f.close(); d['engine']='pygame'; f=open('data/config.json','w',encoding='utf-8'); json.dump(d,f,indent=4); f.close()"
echo Config restored to 2D mode.
