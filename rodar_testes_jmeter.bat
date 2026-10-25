@echo off
chcp 65001 >nul
title Executar Testes JMeter + Preparacao Automatica do Banco
cd /d "%~dp0"

set "JMETER_HOME=C:\Users\WINDOWS 10 PRO\Documents\apache-jmeter-5.6.3"
set "JMETER_BIN=C:\Users\WINDOWS 10 PRO\Documents\apache-jmeter-5.6.3\bin\"
set "JMETER_EXE=%JMETER_BIN%jmeter.bat"
set "PYTHON_BIN=%~dp0.venv\Scripts\python.exe"

if not exist "%JMETER_EXE%" (
    echo [ERRO] JMeter nao encontrado em: "%JMETER_EXE%"
    pause
    exit /b 1
)

echo ======================================================================
echo   EXECUCAO AUTOMATICA DE TESTES JMETER + PREPARACAO DO POSTGRESQL
echo ======================================================================
echo   Verificando servidor na porta 5000 (http://127.0.0.1:5000/saude)...
"%PYTHON_BIN%" -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/saude', timeout=3)" 2>nul
if errorlevel 1 (
    echo   [AVISO] Servidor na porta 5000 nao respondeu!
    echo   Execute 'ligar_servidor.bat' antes de iniciar os testes.
    pause
    exit /b 1
) else (
    echo   [OK] Servidor online na porta 5000!
)

echo.
echo Escolha qual situacao deseja testar:
echo   1) 100k SEM indice  (3 testes: 50/50, 75/25, 25/75)
echo   2) 100k COM indice  (3 testes: 50/50, 75/25, 25/75)
echo   3) 20k  SEM indice  (3 testes: 50/50, 75/25, 25/75)
echo   4) 20k  COM indice  (3 testes: 50/50, 75/25, 25/75)
echo   5) RODAR OS 3 CENARIOS DE UMA VEZ (100k Sem Indice + 100k Com Indice + 20k Sem Indice)
echo.
set /p "OPCAO=Digite a opcao (1-5, ou ENTER para 5): "
if "%OPCAO%"=="" set "OPCAO=5"

if "%OPCAO%"=="1" call :RODAR_BATERIA "100k_sem_indice"
if "%OPCAO%"=="2" call :RODAR_BATERIA "100k_com_indice"
if "%OPCAO%"=="3" call :RODAR_BATERIA "20k_sem_indice"
if "%OPCAO%"=="4" call :RODAR_BATERIA "20k_com_indice"
if "%OPCAO%"=="5" (
    call :RODAR_BATERIA "100k_sem_indice"
    call :RODAR_BATERIA "100k_com_indice"
    call :RODAR_BATERIA "20k_sem_indice"
)

echo.
echo ======================================================================
echo   TODOS OS TESTES FINALIZADOS COM SUCESSO!
echo   Resultados exportados na pasta: "%~dp0resultados_jmeter"
echo ======================================================================
pause
exit /b 0


:RODAR_BATERIA
set "MODO_DB=%~1"
set "OUT_DIR=%~dp0resultados_jmeter\%MODO_DB%"

if exist "%OUT_DIR%" (
    rmdir /s /q "%OUT_DIR%"
)
mkdir "%OUT_DIR%"

echo.
echo ######################################################################
echo   INICIANDO BATERIA: %MODO_DB%
echo ######################################################################

REM --- CENARIO A (50% L / 50% E) ---
echo [Preparando Banco antes do Cenario A - %MODO_DB%...]
"%PYTHON_BIN%" "%~dp0database\preparar_banco.py" %MODO_DB%
echo [1/3] Executando JMeter Cenario A (50%% L / 50%% E) - %MODO_DB%...
call "%JMETER_EXE%" -n -t "%~dp0jmeter\Test Plan.jmx" -l "%OUT_DIR%\cenario_A_50L_50E.jtl" -e -o "%OUT_DIR%\cenario_A_50L_50E"
timeout /t 2 /nobreak >nul

REM --- CENARIO B (75% L / 25% E) ---
echo [Preparando Banco antes do Cenario B - %MODO_DB%...]
"%PYTHON_BIN%" "%~dp0database\preparar_banco.py" %MODO_DB%
echo [2/3] Executando JMeter Cenario B (75%% L / 25%% E) - %MODO_DB%...
call "%JMETER_EXE%" -n -t "%~dp0jmeter\Leituras1200.jmx" -l "%OUT_DIR%\cenario_B_75L_25E.jtl" -e -o "%OUT_DIR%\cenario_B_75L_25E"
timeout /t 2 /nobreak >nul

REM --- CENARIO C (25% L / 75% E) ---
echo [Preparando Banco antes do Cenario C - %MODO_DB%...]
"%PYTHON_BIN%" "%~dp0database\preparar_banco.py" %MODO_DB%
echo [3/3] Executando JMeter Cenario C (25%% L / 75%% E) - %MODO_DB%...
call "%JMETER_EXE%" -n -t "%~dp0jmeter\Escritas1200.jmx" -l "%OUT_DIR%\cenario_C_25L_75E.jtl" -e -o "%OUT_DIR%\cenario_C_25L_75E"

echo.
echo --- RESUMO DA BATERIA: %MODO_DB% ---
"%PYTHON_BIN%" "%~dp0jmeter\resumo_resultados.py" "%OUT_DIR%"
exit /b 0
