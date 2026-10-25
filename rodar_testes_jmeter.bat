@echo off
chcp 65001 >nul
title Executar 3 Testes JMeter - Sistemas Distribuidos 1
cd /d "%~dp0"

set "JMETER_BIN=C:\Users\WINDOWS 10 PRO\Documents\apache-jmeter-5.6.3\bin\jmeter.bat"
set "PYTHON_BIN=%~dp0.venv\Scripts\python.exe"

if not exist "%JMETER_BIN%" (
    echo [ERRO] JMeter nao encontrado em: "%JMETER_BIN%"
    echo Ajuste a variavel JMETER_BIN no topo deste arquivo .bat.
    pause
    exit /b 1
)

echo ======================================================================
echo   EXECUCAO AUTOMATICA DOS 3 CENARIOS DO APACHE JMETER (1200 THREADS)
echo ======================================================================
echo   1) Cenario A - 50%% Leituras / 50%% Escritas (jmeter\Test Plan.jmx)
echo   2) Cenario B - 75%% Leituras / 25%% Escritas (jmeter\Leituras1200.jmx)
echo   3) Cenario C - 25%% Leituras / 75%% Escritas (jmeter\Escritas1200.jmx)
echo ======================================================================
echo.

set /p "NOME_BATERIA=Digite um nome para identificar esta bateria (ou ENTER para 'padrao'): "
if "%NOME_BATERIA%"=="" set "NOME_BATERIA=padrao"

set "OUT_DIR=%~dp0resultados_jmeter\%NOME_BATERIA%"

echo.
echo Verificando se o servidor esta ativo em http://127.0.0.1:5000/saude ...
"%PYTHON_BIN%" -c "import urllib.request, sys; urllib.request.urlopen('http://127.0.0.1:5000/saude', timeout=3)" 2>nul
if errorlevel 1 (
    echo [AVISO] O servidor na porta 5000 nao respondeu!
    echo Certifique-se de executar 'ligar_servidor.bat' antes de rodar os testes.
    set /p "CONTINUAR=Deseja continuar mesmo assim? (S/N): "
    if /i not "%CONTINUAR%"=="S" exit /b 1
) else (
    echo [OK] Servidor online na porta 5000!
)

if exist "%OUT_DIR%" (
    echo Limpando pasta anterior "%OUT_DIR%" para nova exportacao...
    rmdir /s /q "%OUT_DIR%"
)
mkdir "%OUT_DIR%"

echo.
echo ----------------------------------------------------------------------
echo [1/3] Executando Cenario A: 50%% Leituras / 50%% Escritas ...
echo ----------------------------------------------------------------------
call "%JMETER_BIN%" -n -t "%~dp0jmeter\Test Plan.jmx" -l "%OUT_DIR%\cenario_A_50L_50E.jtl" -e -o "%OUT_DIR%\cenario_A_50L_50E"

echo.
echo Aguardando 3 segundos antes do proximo teste...
timeout /t 3 /nobreak >nul

echo.
echo ----------------------------------------------------------------------
echo [2/3] Executando Cenario B: 75%% Leituras / 25%% Escritas ...
echo ----------------------------------------------------------------------
call "%JMETER_BIN%" -n -t "%~dp0jmeter\Leituras1200.jmx" -l "%OUT_DIR%\cenario_B_75L_25E.jtl" -e -o "%OUT_DIR%\cenario_B_75L_25E"

echo.
echo Aguardando 3 segundos antes do proximo teste...
timeout /t 3 /nobreak >nul

echo.
echo ----------------------------------------------------------------------
echo [3/3] Executando Cenario C: 25%% Leituras / 75%% Escritas ...
echo ----------------------------------------------------------------------
call "%JMETER_BIN%" -n -t "%~dp0jmeter\Escritas1200.jmx" -l "%OUT_DIR%\cenario_C_25L_75E.jtl" -e -o "%OUT_DIR%\cenario_C_25L_75E"

echo.
echo ======================================================================
echo   TESTES CONCLUIDOS! GERANDO TABELA DE RESUMO...
echo ======================================================================
"%PYTHON_BIN%" "%~dp0jmeter\resumo_resultados.py" "%OUT_DIR%"

echo.
echo Todos os relatorios HTML, JTL e CSV foram exportados em:
echo   "%OUT_DIR%"
echo.
pause
