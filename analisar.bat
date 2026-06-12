@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo =======================================
echo  Analisador de Testes A/B - Meliuz
echo =======================================
echo.

set COUNT=0
for %%F in ("%~dp0datasets\*.csv") do (
    set /a COUNT+=1
    set "FILE_!COUNT!=%%~nxF"
    echo [!COUNT!] %%~nxF
)

echo [0] Analisar todos
echo.

if %COUNT%==0 (
    echo Nenhum arquivo CSV encontrado em datasets\
    pause
    exit /b
)

set /p OPCAO="Escolha o numero do dataset: "

if "%OPCAO%"=="0" (
    for /l %%I in (1,1,%COUNT%) do (
        echo.
        echo Analisando: !FILE_%%I!
        python "%~dp0analyze.py" "datasets/!FILE_%%I!"
    )
) else (
    set ARQUIVO=!FILE_%OPCAO%!
    if "!ARQUIVO!"=="" (
        echo Opcao invalida.
    ) else (
        echo.
        echo Analisando: !ARQUIVO!
        python "%~dp0analyze.py" "datasets/!ARQUIVO!"
    )
)

echo.
echo Analise concluida! Verifique a pasta reports/ e o arquivo resultados.csv
pause
