@echo off
title Shoppy Agent - Launcher
color 0A

echo ======================================================================
echo                 STARTING SHOPPY AGENT / AGENTCART
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Ollama AI model (qwen2.5:1.5b)...
where ollama >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Ollama detected. Ensuring model is available...
    start /min "Ollama Service" ollama run qwen2.5:1.5b
) else (
    echo [WARNING] Ollama is not installed or not in PATH.
    echo If using LLM fallback, make sure Ollama is running on localhost:11434.
)

echo.
echo [2/3] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Shoppy Agent - Backend API" cmd /k "cd backend && .venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo.
echo [3/3] Starting Vite Frontend on http://localhost:8080 ...
start "Shoppy Agent - Frontend UI" cmd /k "npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ======================================================================
echo   ALL SERVICES STARTED SUCCESSFULLY!
echo.
echo   - Frontend:    http://localhost:8080
echo   - Backend API: http://127.0.0.1:8000
echo   - API Docs:    http://127.0.0.1:8000/docs
echo   - Admin Login: http://localhost:8080/admin/login
echo                  (admin@agentcart.local / admin123)
echo ======================================================================
echo.

start http://localhost:8080
pause

