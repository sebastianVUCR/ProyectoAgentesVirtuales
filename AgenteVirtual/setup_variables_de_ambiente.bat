@echo off
:: Validar si el script se esta ejecutando como Administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Por favor, ejecuta este script dando CLIC DERECHO y seleccionando "Ejecutar como administrador".
    pause
    exit /b
)

echo Configurando variables de entorno permanentes para Ollama...
echo -----------------------------------------------------------

:: Setear variables en el entorno del Sistema (Permanentes)
setx /M OLLAMA_GPU_OVERHEAD "0"
setx /M GGML_CUDA_ENABLE_UNIFIED_MEMORY "0"
setx /M OLLAMA_FLASH_ATTENTION "1"

echo -----------------------------------------------------------
echo [OK] Variables guardadas con exito en el Registro de Windows.
echo [INFO] Cerrando cualquier instancia activa de Ollama para aplicar los cambios...

:: Cerrar Ollama si esta abierto en segundo plano
taskkill /f /im ollama.exe >nul 2>&1
taskkill /f /im "ollama app.exe" >nul 2>&1

echo [OK] Proceso terminado. Ya puedes reiniciar tu script de Python.
pause