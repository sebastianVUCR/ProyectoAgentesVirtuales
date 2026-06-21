@echo off
:: =========================================================================
:: Script de Instalación Automatizada para la Aplicación (Setup & Run)
:: =========================================================================
:: Descripción: Instala dependencias del sistema, configura el entorno
::              virtual de Python, instala dependencias del proyecto y
::              ejecuta el controlador principal de la aplicación.
:: =========================================================================

echo [INFO] Iniciando el proceso de instalacion...
echo.

:: -------------------------------------------------------------------------
:: 1. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA
:: -------------------------------------------------------------------------
echo [1/5] Instalando dependencias del sistema...

:: Instalar Ollama a traves de PowerShell de forma silenciosa
echo [OLLAMA] Descargando e instalando Ollama...
powershell -Command "irm https://ollama.com/install.ps1 | iex"
if %errorlevel% neq 0 (
    echo [ADVERTENCIA] Hubo un problema al intentar instalar Ollama. Continuando...
) else (
    echo [OLLAMA] Ollama instalado correctamente o ya existente.
)

:: Recordatorio para Steam e Infinitode 2 (Requieren instalacion interactiva del usuario)
echo.
echo [STEAM / INFINITODE 2] Por favor, asegurese de tener instalado:
echo   - Steam (Descargar desde: https://store.steampowered.com/)
echo   - Infinitode 2 (Instalar directamente desde la tienda de Steam)
echo.
echo [CONFIGURACION JUEGO] NOTA IMPORTANTE PARA EL USUARIO:
echo   1. Abra Infinitode 2 en su pantalla principal.
echo   2. Dirigete a Ajustes (icono de engranaje).
echo   3. DESACTIVE la 'Pantalla Completa' (Modo Ventana).
echo   4. DESACTIVE la 'Musica del Juego'.
echo.
pause

:: -------------------------------------------------------------------------
:: 2. CONFIGURACIÓN DE VARIABLES DE ENTORNO (SETUP.BAT DE OLLAMA)
:: -------------------------------------------------------------------------
echo.
echo [2/5] Verificando configuracion de variables de ambiente para Ollama...
if exist "setup.bat" (
    echo [SETUP] Ejecutando setup.bat de la raiz para variables de ambiente y memoria...
    call setup.bat
) else (
    echo [SETUP] setup.bat no encontrado en la raiz. Se omiten variables personalizadas.
)

:: -------------------------------------------------------------------------
:: 3. CREACIÓN DEL ENTORNO VIRTUAL DE PYTHON
:: -------------------------------------------------------------------------
echo.
echo [3/5] Creando entorno virtual de Python (env)...
python -m venv env
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo crear el entorno virtual. Verifique que Python esta instalado y en el PATH.
    pause
    exit /b %errorlevel%
)

:: -------------------------------------------------------------------------
:: 4. ACTIVACIÓN DEL ENTORNO E ACTUALIZACIÓN DE PIP
:: -------------------------------------------------------------------------
echo.
echo [4/5] Activando entorno virtual y actualizando herramientas de empaquetado...
call .\env\Scripts\activate.bat

echo [PIP] Actualizando pip, setuptools y wheel...
python.exe -m pip install --upgrade pip
python -m pip install --upgrade pip setuptools wheel

:: -------------------------------------------------------------------------
:: 5. INSTALACIÓN DE REQUISITOS (REQUIREMENTS.TXT)
:: -------------------------------------------------------------------------
echo.
echo [5/5] Instalandos paquetes y dependencias desde requirements.txt...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [ERROR] Archivo requirements.txt no encontrado en el directorio actual.
    pause
    exit /b 1
)



echo.
echo [INFO] Proceso finalizado. El entorno virtual se cerrara.
call deactivate
pause