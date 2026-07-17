@echo off
chcp 65001 >nul
setlocal

echo.
echo ============================================================
echo PetPulse Enterprise OS - Restore Stable Version
echo ============================================================
echo.

cd /d "%~dp0"

if not exist "assets" (
    echo [ERROR] 請把此檔案放在 dashboard 專案根目錄後再執行。
    pause
    exit /b 1
)

set "STAMP=%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
set "STAMP=%STAMP: =0%"
set "SNAPSHOT=_v3_broken_snapshot_%STAMP%"

mkdir "%SNAPSHOT%" >nul 2>&1
mkdir "%SNAPSHOT%\assets" >nul 2>&1
mkdir "%SNAPSHOT%\modules\platform" >nul 2>&1

if exist "assets\enterprise.css" copy /Y "assets\enterprise.css" "%SNAPSHOT%\assets\enterprise.css" >nul
if exist "modules\platform\platform_frame.py" copy /Y "modules\platform\platform_frame.py" "%SNAPSHOT%\modules\platform\platform_frame.py" >nul
if exist "app.py" copy /Y "app.py" "%SNAPSHOT%\app.py" >nul

echo [1/3] 已保存目前版本到 %SNAPSHOT%

if exist "assets\enterprise_v2_backup.css" (
    copy /Y "assets\enterprise_v2_backup.css" "assets\enterprise.css" >nul
    echo [OK] enterprise.css 已恢復
) else (
    echo [WARNING] 找不到 assets\enterprise_v2_backup.css
)

if exist "modules\platform\platform_frame_v2_backup.py" (
    copy /Y "modules\platform\platform_frame_v2_backup.py" "modules\platform\platform_frame.py" >nul
    echo [OK] platform_frame.py 已恢復
) else (
    echo [WARNING] 找不到 modules\platform\platform_frame_v2_backup.py
)

if exist "app_v2_backup.py" (
    copy /Y "app_v2_backup.py" "app.py" >nul
    echo [OK] app.py 已恢復
) else (
    echo [WARNING] 找不到 app_v2_backup.py
)

echo.
echo [2/3] 執行 Python 語法檢查...

python -m py_compile app.py
if errorlevel 1 (
    echo [ERROR] app.py 語法檢查失敗
    pause
    exit /b 1
)

python -m py_compile modules\platform\platform_frame.py
if errorlevel 1 (
    echo [ERROR] platform_frame.py 語法檢查失敗
    pause
    exit /b 1
)

echo [OK] Python 語法檢查通過

echo.
echo [3/3] 正式版已恢復。
echo.
echo 請執行：
echo python -m streamlit run app.py
echo.
pause
