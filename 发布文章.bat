@echo off
chcp 65001 >nul
echo ======================================
echo      嘉驰蓝海博客 - 文章发布工具
echo ======================================
echo.

REM 检查是否有文章文件
if not exist "posts\*.md" (
    echo [错误] posts 文件夹中没有找到 .md 文件
    echo 请先将 Markdown 文章放入 posts 文件夹
    pause
    exit /b 1
)

echo [1/4] 正在检查 Git 状态...
cd /d "%~dp0"

REM 初始化 Git 仓库（如果没有）
if not exist ".git" (
    echo [信息] 初始化 Git 仓库...
    git init
    git remote add origin https://github.com/wangtnt/jiachi-blog.git
)

echo [2/4] 正在添加文章到 Git...
git add posts\*.md
git add images\*.*

echo [3/4] 请输入文章标题（用于提交信息）：
set /p title=

echo [4/4] 正在提交并推送...
git commit -m "添加文章: %title%"

echo.
echo 正在推送到 GitHub...
git push -u origin main 2>nul || git push -u origin master 2>nul || (
    echo [提示] 推送失败，可能需要登录 GitHub
    echo 请运行: git push
    echo 然后按提示输入用户名和密码/Token
    pause
    exit /b 1
)

echo.
echo ======================================
echo      ✅ 文章发布成功！
echo ======================================
echo.
echo 网站将在几分钟后自动更新：
echo https://wangtnt.github.io/jiachi-blog
echo.
pause