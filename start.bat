@echo off
REM Script para iniciar la aplicación con Docker Compose en Windows

echo 🚀 Iniciando API Bancaria con Docker...

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado. Por favor, instala Docker Desktop.
    pause
    exit /b 1
)

REM Verificar si Docker está ejecutándose
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está ejecutándose. Por favor, inicia Docker Desktop.
    pause
    exit /b 1
)

REM Construir y ejecutar los contenedores
echo 📦 Construyendo y ejecutando contenedores...
docker-compose up --build -d

if %errorlevel% equ 0 (
    echo ✅ Aplicación iniciada exitosamente!
    echo.
    echo 📋 Información de acceso:
    echo   🌐 API: http://localhost:8001
    echo   📚 Documentación: http://localhost:8001/documentacion
    echo   🗄️  MongoDB: localhost:27017
    echo.
    echo 🔍 Para ver los logs: docker-compose logs -f
    echo 🛑 Para detener: docker-compose down
) else (
    echo ❌ Error al iniciar la aplicación
    pause
    exit /b 1
)

pause
