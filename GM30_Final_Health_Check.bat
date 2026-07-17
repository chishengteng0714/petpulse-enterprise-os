@echo off
chcp 65001 >nul
setlocal

title PetPulse GM30 Final Health Check

cd /d "C:\Users\Jack.Teng\Documents\AI-Social-Listening\dashboard"

echo.
echo ============================================================
echo   PetPulse Enterprise OS v3.0 GM30 Final Health Check
echo ============================================================
echo.

echo [1/7] 檢查核心檔案...
for %%F in (
    "app.py"
    "modules\platform\shell.py"
    "modules\platform\platform_frame.py"
    "modules\platform\home\enterprise_home.py"
    "pages\2_證據中心.py"
    "assets\enterprise.css"
) do (
    if not exist %%F (
        echo [ERROR] 找不到 %%F
        pause
        exit /b 1
    )
)
echo [PASS] 核心檔案完整
echo.

echo [2/7] 檢查首頁是否錯誤匯入 platform_frame...
findstr /I /C:"from modules.platform.platform_frame import" "modules\platform\home\enterprise_home.py" >nul
if not errorlevel 1 (
    echo [ERROR] enterprise_home.py 仍匯入 platform_frame.py
    echo 這會造成 circular import。
    pause
    exit /b 1
)
echo [PASS] 首頁沒有循環匯入
echo.

echo [3/7] Python 語法檢查...
python -m py_compile "app.py"
if errorlevel 1 goto :syntax_error
python -m py_compile "modules\platform\shell.py"
if errorlevel 1 goto :syntax_error
python -m py_compile "modules\platform\platform_frame.py"
if errorlevel 1 goto :syntax_error
python -m py_compile "modules\platform\home\enterprise_home.py"
if errorlevel 1 goto :syntax_error
python -m py_compile "pages\2_證據中心.py"
if errorlevel 1 goto :syntax_error
echo [PASS] 所有 Python 檔案語法正確
echo.

echo [4/7] 匯入 Application Shell...
python -c "from modules.platform.shell import render_platform; print('[PASS] shell import OK')"
if errorlevel 1 goto :import_error
echo.

echo [5/7] 匯入 Enterprise Home...
python -c "from modules.platform.home.enterprise_home import render_enterprise_home; print('[PASS] enterprise_home import OK')"
if errorlevel 1 goto :import_error
echo.

echo [6/7] 匯入 Platform Frame...
python -c "from modules.platform.platform_frame import render_shared_sidebar_brand_and_navigation; print('[PASS] platform_frame import OK')"
if errorlevel 1 goto :import_error
echo.

echo [7/7] 啟動 Streamlit...
echo.
echo ============================================================
echo   GM30 Health Check 全部通過
echo ============================================================
echo.
echo 瀏覽器開啟：
echo http://localhost:8501
echo.
echo 啟動後按 Ctrl + F5。
echo 停止服務請按 Ctrl + C。
echo.

python -m streamlit run app.py
exit /b 0

:syntax_error
echo.
echo [ERROR] Python 語法檢查失敗
pause
exit /b 1

:import_error
echo.
echo [ERROR] 模組匯入失敗
echo 請將這個視窗中的完整錯誤貼回對話。
pause
exit /b 1
