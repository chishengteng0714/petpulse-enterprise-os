@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

echo.
echo ============================================================
echo PetPulse Repair + Prepare v3 Workspace
echo ============================================================
echo.

if not exist "app.py" (
    echo [ERROR] 請把本檔放在 dashboard 根目錄。
    pause
    exit /b 1
)

echo [1/6] 備份目前檔案...
if not exist "_repair_snapshot" mkdir "_repair_snapshot"
copy /Y "app.py" "_repair_snapshot\app_current.py" >nul
copy /Y "modules\platform\platform_frame.py" "_repair_snapshot\platform_frame_current.py" >nul
copy /Y "pages\2_證據中心.py" "_repair_snapshot\2_證據中心_current.py" >nul
copy /Y "assets\enterprise.css" "_repair_snapshot\enterprise_current.css" >nul

echo [2/6] 還原相容的 platform_frame.py...
if exist "modules\platform\platform_frame_v2_backup.py" (
    copy /Y "modules\platform\platform_frame_v2_backup.py" "modules\platform\platform_frame.py" >nul
    echo [OK] platform_frame.py 已還原為 v2 相容版
) else (
    echo [ERROR] 找不到 modules\platform\platform_frame_v2_backup.py
    pause
    exit /b 1
)

echo [3/6] 移出 pages 裡的備份頁...
if not exist "backup" mkdir "backup"

if exist "pages\2_證據中心_GM26_backup.py" (
    move /Y "pages\2_證據中心_GM26_backup.py" "backup\" >nul
)

if exist "pages\2_證據中心_GM27.py" (
    move /Y "pages\2_證據中心_GM27.py" "backup\" >nul
)

echo [4/6] 執行語法與 import 檢查...
python -m py_compile "app.py"
if errorlevel 1 (
    echo [ERROR] app.py 語法檢查失敗
    pause
    exit /b 1
)

python -m py_compile "modules\platform\platform_frame.py"
if errorlevel 1 (
    echo [ERROR] platform_frame.py 語法檢查失敗
    pause
    exit /b 1
)

python -m py_compile "pages\2_證據中心.py"
if errorlevel 1 (
    echo [ERROR] 2_證據中心.py 語法檢查失敗
    pause
    exit /b 1
)

python -c "from modules.platform.platform_frame import render_shared_sidebar_brand_and_navigation; print('[OK] 共用 Sidebar 函式可正常匯入')"
if errorlevel 1 (
    echo [ERROR] 共用 Sidebar 函式仍無法匯入
    pause
    exit /b 1
)

echo [5/6] 建立 v3 平行工作區...
if not exist "_v3_workspace" mkdir "_v3_workspace"
if not exist "_v3_workspace\assets" mkdir "_v3_workspace\assets"
if not exist "_v3_workspace\modules\platform\home" mkdir "_v3_workspace\modules\platform\home"
if not exist "_v3_workspace\pages" mkdir "_v3_workspace\pages"
if not exist "_v3_workspace\.streamlit" mkdir "_v3_workspace\.streamlit"

copy /Y "app.py" "_v3_workspace\app_v3.py" >nul
copy /Y "assets\enterprise.css" "_v3_workspace\assets\enterprise_v3.css" >nul
copy /Y "modules\platform\platform_frame.py" "_v3_workspace\modules\platform\platform_frame_v3.py" >nul
copy /Y "modules\platform\home\enterprise_home.py" "_v3_workspace\modules\platform\home\enterprise_home_v3.py" >nul
copy /Y "pages\2_證據中心.py" "_v3_workspace\pages\2_證據中心_v3.py" >nul

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

echo [6/6] 完成
echo.
echo 正式版已修復，v3 工作區也已建立。
echo.
echo 請關閉原本 Streamlit 視窗後執行：
echo python -m streamlit run app.py
echo.
pause
