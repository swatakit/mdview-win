@echo off
rem mdview launcher - keep this file in the same folder as mdview.py
where pythonw >nul 2>nul && (start "" pythonw "%~dp0mdview.py" "%~1" & exit /b)
where pyw >nul 2>nul && (start "" pyw "%~dp0mdview.py" "%~1" & exit /b)
where uv >nul 2>nul && (uv run --no-project --with markdown python "%~dp0mdview.py" "%~1" & exit /b)
echo Could not find Python (pythonw, pyw or uv) on this PC.
pause
