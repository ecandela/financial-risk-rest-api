@echo off
setlocal

:: Especifica la ubicación de tu entorno virtual
set VIRTUAL_ENV_DIR=fin_risk_rest_api

:: Activa el entorno virtual (Windows)
call %VIRTUAL_ENV_DIR%\Scripts\activate

:: Tu código y comandos dentro del entorno virtual van aquí

cmd

echo Entorno virtual activado.
