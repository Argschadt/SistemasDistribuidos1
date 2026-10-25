@echo off
chcp 65001 >nul
title Servidor Flask - Sistemas Distribuidos 1
cd /d "%~dp0"

if "%~1"=="" (
    set "PORT=5000"
) else (
    set "PORT=%~1"
)

echo ============================================================
echo   INICIANDO SERVIDOR WEB FLASK (PORTA %PORT%)
echo ============================================================
echo   URL Local:   http://127.0.0.1:%PORT%
echo   Healthcheck: http://127.0.0.1:%PORT%/saude
echo   Para encerrar o servidor, pressione CTRL+C
echo ============================================================
echo.

if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" "%~dp0app.py"
) else (
    python "%~dp0app.py"
)

echo.
echo O servidor foi encerrado.
pause
