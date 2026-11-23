@echo off
REM Executa o Static Checker. Uso: executar.bat Teste  (ou executar.bat caminho\Teste)
where uv >nul 2>nul
if %errorlevel%==0 (
  uv run --project "%~dp0." "%~dp0programa_principal.py" %*
) else (
  python "%~dp0programa_principal.py" %*
)
