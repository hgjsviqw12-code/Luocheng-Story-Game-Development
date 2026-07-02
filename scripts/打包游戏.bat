@echo off
chcp 65001 >nul
echo ========================================
echo   罗诚的故事 - 游戏打包脚本
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查PyInstaller是否安装
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装 PyInstaller...
    pip install pyinstaller
    echo.
)

:: 检查依赖
echo [检查] 正在检查游戏依赖...
python -c "import pygame; import PIL" 2>nul
if errorlevel 1 (
    echo [提示] 正在安装游戏依赖...
    pip install pygame Pillow
)

echo.
echo ========================================
echo   开始打包...
echo ========================================
echo.
echo 打包过程可能需要3-5分钟，请耐心等待...
echo.

:: 执行打包
pyinstaller main.spec --clean

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 可执行文件位置:
echo   dist\罗诚的故事\罗诚的故事.exe
echo.
echo 打包后的文件夹可以直接拷贝到其他电脑运行，
echo 无需安装Python或任何依赖。
echo.
echo 小提示：
echo   - 可以把整个"罗诚的故事"文件夹打包成ZIP分享
echo   - 可以用 Inno Setup 制作安装程序
echo.
pause
