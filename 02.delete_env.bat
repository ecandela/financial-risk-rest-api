@echo off
setlocal

:: Especifica la ubicación del entorno virtual
set VENV_DIR=fin_risk_rest_api

:: Activa el entorno virtual (Windows)
call "%VENV_DIR%\Scripts\activate"

:: Elimina el entorno virtual
rd /s /q "%VENV_DIR%"


echo Entorno virtual eliminado.
pause