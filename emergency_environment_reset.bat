@echo off
  taskkill /f /im ollama.exe
  taskkill /f /im lmstudio.exe
  taskkill /f /im python.exe
  taskkill /f /im python3.exe
  netsh winsock reset
  ipconfig /flushdns
  echo ¡Entorno de IA cerrado y red limpia!
  pause