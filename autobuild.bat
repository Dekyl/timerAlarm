@echo off
color 0A
echo === Compiling Timer Alarm ===

where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PyInstaller not installed. Run: pip install pyinstaller
    pause
    exit /b
)

if exist dist (
    echo === Removing dist folder ===
    rmdir /s /q dist
) else (
    echo dist folder not found, skipping delete.
)

pyinstaller --noconfirm --onefile --windowed ^
--icon "res\alarm.ico" ^
--name "alarm" ^
--add-data "res;res" ^
"src\main.py"

echo Cleaning temp files...
if exist "timer_alarm.spec" (
    echo === Removing timer_alarm.spec ===
    del "timer_alarm.spec"
)

if exist "build" (
    echo === Removing build folder ===
    rmdir /s /q build
) else (
    echo build folder not found, skipping delete.
)

echo.
echo === Build ready! ===
echo Output: dist\timer_alarm.exe

pause