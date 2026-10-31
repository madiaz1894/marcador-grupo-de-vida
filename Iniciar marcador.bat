@echo off
rem Doble clic para abrir el marcador con control remoto desde el iPhone.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY (
  echo.
  echo   No se encontro Python 3. Instalalo desde https://www.python.org/downloads/
  echo   y marca "Add python.exe to PATH" durante la instalacion.
  echo.
  pause
  exit /b 1
)
%PY% server.py
pause
