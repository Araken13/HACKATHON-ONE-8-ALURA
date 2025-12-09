@echo off
title ChurnInsight Launcher 🚀

echo ==========================================
echo      INICIANDO PLATAFORMA CHURNINSIGHT
echo ==========================================

echo [1/2] Iniciando Backend API (Python)...
start "Backend API" cmd /k "cd /d %~dp0 & python api.py || echo ERRO: Certifique-se que o Python esta no PATH e as libs estao instaladas."

echo [2/2] Iniciando Frontend (React)...
start "Frontend Dashboard" cmd /k "cd /d %~dp0frontend & npm run dev"

echo.
echo ==========================================
echo      SISTEMAS INICIADOS EM JANELAS SEPARADAS
echo      Acesse: http://localhost:5173
echo ==========================================
pause
