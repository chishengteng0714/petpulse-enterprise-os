@echo off
chcp 65001 >nul
setlocal

echo.
echo ============================================================
echo PetPulse Enterprise OS - Prepare Parallel v3 Workspace
echo ============================================================
echo.

cd /d "%~dp0"

if not exist "app.py" (
    echo [ERROR] 請把此檔案放在 dashboard 專案根目錄後再執行。
    pause
    exit /b 1
)

mkdir "_v3_workspace" >nul 2>&1
mkdir "_v3_workspace\assets" >nul 2>&1
mkdir "_v3_workspace\modules\platform\home" >nul 2>&1
mkdir "_v3_workspace\pages" >nul 2>&1
mkdir "_v3_workspace\.streamlit" >nul 2>&1

copy /Y "app.py" "_v3_workspace\app_v3.py" >nul
copy /Y "assets\enterprise.css" "_v3_workspace\assets\enterprise_v3.css" >nul
copy /Y "modules\platform\platform_frame.py" "_v3_workspace\modules\platform\platform_frame_v3.py" >nul
copy /Y "modules\platform\home\enterprise_home.py" "_v3_workspace\modules\platform\home\enterprise_home_v3.py" >nul

if exist "pages\2_證據中心.py" (
    copy /Y "pages\2_證據中心.py" "_v3_workspace\pages\2_證據中心_v3.py" >nul
)

(
echo [client]
echo showSidebarNavigation = false
echo.
echo [theme]
echo base = "light"
echo primaryColor = "#7BAA3C"
echo backgroundColor = "#F6F7F3"
echo secondaryBackgroundColor = "#FFFFFF"
echo textColor = "#203129"
echo font = "sans serif"
) > "_v3_workspace\.streamlit\config.toml"

(
echo # PetPulse Enterprise OS v3 Parallel Workspace
echo.
echo 此目錄只用於 v3 Presentation Layer 平行開發。
echo.
echo 正式版檔案不會在開發期間被覆蓋。
echo 完成驗收後才一次切換。
) > "_v3_workspace\README.md"

echo [OK] v3 平行工作區已建立：
echo %CD%\_v3_workspace
echo.
pause
