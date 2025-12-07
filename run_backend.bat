@echo off
"c:\Users\D. SHIV KUMAR\Desktop\consulting\.venv\Scripts\python.exe" "c:\Users\D. SHIV KUMAR\Desktop\consulting\backend\app.py" > "c:\Users\D. SHIV KUMAR\Desktop\consulting\backend_output.txt" 2>&1
if %errorlevel% neq 0 echo Error: %errorlevel% >> "c:\Users\D. SHIV KUMAR\Desktop\consulting\backend_output.txt"
