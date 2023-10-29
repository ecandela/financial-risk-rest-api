@echo off
setlocal

:: Especifica la ubicación del entorno virtual y el nombre
set VIRTUAL_ENV_DIR=fin_risk_rest_api
set REQUIREMENTS_FILE=requirements.txt

:: Verifica si el entorno virtual ya existe
if not exist %VIRTUAL_ENV_DIR%\Scripts\activate (
    :: Crea el entorno virtual si no existe
    python -m venv  %VIRTUAL_ENV_DIR%
)

:: Activa el entorno virtual (Windows)
call %VIRTUAL_ENV_DIR%\Scripts\activate

:: Instala las dependencias desde el archivo requirements.txt
pip install -r %REQUIREMENTS_FILE%

:: Desactiva el entorno virtual
deactivate

echo Entorno virtual creado y dependencias instaladas.
pause


