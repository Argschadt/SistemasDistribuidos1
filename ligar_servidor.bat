@echo off
chcp 65001 >nul
title Cluster Web Replicado (NGINX + 2 Replicas Flask)
cd /d "%~dp0"

set "PYTHON_BIN=%~dp0.venv\Scripts\python.exe"
set "NGINX_DIR=%~dp0nginx-1.31.8"

echo ======================================================================
echo   INICIANDO ARQUITETURA REPLICADA WEB (NGINX + 2 REPLICAS FLASK)
echo ======================================================================
echo   - Balanceador NGINX:  http://127.0.0.1:5000  (Porta de entrada)
echo   - Flask Replica 1:    http://127.0.0.1:5001
echo   - Flask Replica 2:    http://127.0.0.1:5002
echo ======================================================================
echo.

REM Encerra eventuais processos antigos do NGINX antes de iniciar
taskkill /f /im nginx.exe >nul 2>&1

echo [1/3] Iniciando Flask Replica 1 na porta 5001...
start "Flask Replica 1 (Porta 5001)" cmd /k "title Flask Replica 1 (Porta 5001) && set PORT=5001 && "%PYTHON_BIN%" "%~dp0app.py""

echo [2/3] Iniciando Flask Replica 2 na porta 5002...
start "Flask Replica 2 (Porta 5002)" cmd /k "title Flask Replica 2 (Porta 5002) && set PORT=5002 && "%PYTHON_BIN%" "%~dp0app.py""

echo [3/3] Iniciando Load Balancer NGINX na porta 5000...
pushd "%NGINX_DIR%"
start "" nginx.exe
popd

timeout /t 2 /nobreak >nul

echo.
echo ======================================================================
echo   TUDO PRONTO E RODANDO!
echo ======================================================================
echo   - Acesse no navegador ou JMeter: http://127.0.0.1:5000
echo   - Para simular a QUEDA de 1 servidor web nos testes, basta fechar
echo     uma das duas janelas do Flask (5001 ou 5002)!
echo   - Para desligar tudo ao terminar, execute: desligar_servidor.bat
echo ======================================================================
echo.
pause
