@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo O ambiente Python do projeto nao foi encontrado.
  pause
  exit /b 1
)
echo A iniciar o Prisma. Mantem esta janela aberta enquanto usas a aplicacao.
".venv\Scripts\python.exe" -m streamlit run "app.py" --server.address 127.0.0.1 --server.headless false
pause
