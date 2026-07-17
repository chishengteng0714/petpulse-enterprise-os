@echo off
chcp 65001 >nul
setlocal

title PetPulse Enterprise OS GM29 Demo Check

cd /d "C:\Users\Jack.Teng\Documents\AI-Social-Listening\dashboard"

echo.
echo ============================================================
echo   PetPulse Enterprise OS v3.0 GM29 Demo Check
echo ============================================================
echo.

echo [1/6] 檢查核心檔案...
if not exist "app.py" (
    echo [ERROR] 找不到 app.py
    pause
    exit /b 1
)

if not exist "assets\enterprise.css" (
    echo [ERROR] 找不到 assets\enterprise.css
    pause
    exit /b 1
)

if not exist "modules\platform\platform_frame.py" (
    echo [ERROR] 找不到 modules\platform\platform_frame.py
    pause
    exit /b 1
)

if not exist "modules\platform\home\enterprise_home.py" (
    echo [ERROR] 找不到 modules\platform\home\enterprise_home.py
    pause
    exit /b 1
)

if not exist "pages\2_證據中心.py" (
    echo [ERROR] 找不到 pages\2_證據中心.py
    pause
    exit /b 1
)

echo [PASS] 核心檔案存在
echo.

echo [2/6] 驗證 platform_frame.py...
python -m py_compile "modules\platform\platform_frame.py"
if errorlevel 1 (
    echo [ERROR] platform_frame.py 語法檢查失敗
    pause
    exit /b 1
)
echo [PASS] platform_frame.py
echo.

echo [3/6] 驗證 enterprise_home.py...
python -m py_compile "modules\platform\home\enterprise_home.py"
if errorlevel 1 (
    echo [ERROR] enterprise_home.py 語法檢查失敗
    pause
    exit /b 1
)
echo [PASS] enterprise_home.py
echo.

echo [4/6] 驗證證據中心...
python -m py_compile "pages\2_證據中心.py"
if errorlevel 1 (
    echo [ERROR] 證據中心語法檢查失敗
    pause
    exit /b 1
)
echo [PASS] 證據中心
echo.

echo [5/6] 檢查 Enterprise CSS...
for %%A in ("assets\enterprise.css") do set CSS_SIZE=%%~zA
if "%CSS_SIZE%"=="0" (
    echo [ERROR] enterprise.css 是空檔案
    pause
    exit /b 1
)
echo [PASS] enterprise.css 大小：%CSS_SIZE% bytes
echo.

echo [6/6] 啟動 PetPulse Enterprise OS...
echo.
echo 請在瀏覽器開啟：
echo http://localhost:8501
echo.
echo 啟動後請按 Ctrl + F5 強制重新整理。
echo 若要停止服務，回到此視窗按 Ctrl + C。
echo.

python -m streamlit run app.py

endlocal
