@echo off
chcp 65001 > nul
echo 正在打包读书记录工具...
echo.

REM 检查图标文件
if not exist "book_icon.ico" (
    echo 警告: 未找到图标文件 book_icon.ico
    echo 将使用程序生成的图标
    set ICON_PARAM=
) else (
    echo 找到图标文件: book_icon.ico
    set ICON_PARAM=--icon=book_icon.ico --add-data="book_icon.ico;."
)

REM 清理旧的构建文件
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "BookRecordTool.spec" del BookRecordTool.spec

echo.
echo 开始打包...
echo.

REM 使用英文可执行文件名，但应用程序标题还是中文
pyinstaller --onefile ^
            --windowed ^
            --name="BookRecordTool" ^
            %ICON_PARAM% ^
            --clean ^
            Book_Record_Tool_v1.0.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo 打包成功！
    echo.
    echo 可执行文件位置: dist\BookRecordTool.exe
    echo 窗口标题: 读书记录工具 v1.0
    echo.
    echo 图标说明:
    echo 1. 如果存在 book_icon.ico 文件，会使用该文件作为图标
    echo 2. 如果不存在，会使用程序内置的图标
    echo 3. 窗口标题和界面仍然是中文
) else (
    echo.
    echo 打包失败！
    echo 错误代码: %ERRORLEVEL%
)

pause