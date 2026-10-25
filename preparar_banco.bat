@echo off
chcp 65001 >nul
title Preparar Banco de Dados PostgreSQL
cd /d "%~dp0"

"%~dp0.venv\Scripts\python.exe" "%~dp0database\preparar_banco.py" %1
pause
