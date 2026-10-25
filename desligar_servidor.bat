@echo off
chcp 65001 >nul
title Desligando Servidores (NGINX + Flask)
cd /d "%~dp0"

echo Encerrando Balanceador NGINX...
taskkill /f /im nginx.exe >nul 2>&1

echo Encerrando Replicas do Flask (Portas 5001 e 5002)...
taskkill /f /fi "WINDOWTITLE eq Flask Replica 1*" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq Flask Replica 2*" >nul 2>&1

for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5001 :5002" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo.
echo Todos os servidores Web (NGINX e Replicas Flask) foram desligados!
timeout /t 3
