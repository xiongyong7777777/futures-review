#!/usr/bin/env powershell

<#
.SYNOPSIS
自动安装Android Studio和相关依赖
.DESCRIPTION
本脚本使用Winget包管理器自动下载并安装Android Studio，
然后安装Kivy、Buildozer等构建APK所需的依赖。
#>

Write-Host "=== 自动安装Android Studio和APK构建依赖 ===" -ForegroundColor Green
Write-Host ""

# 检查Winget是否可用
Write-Host "1. 检查Winget包管理器..." -ForegroundColor Yellow
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Winget未安装！Winget是Windows 10/11内置的包管理器。" -ForegroundColor Red
    Write-Host "请确保您的Windows版本是10 1709或更高版本。" -ForegroundColor Red
    Write-Host "您可以从Microsoft Store安装'应用安装程序'来获取Winget。" -ForegroundColor Red
    Write-Host "或者访问：https://aka.ms/getwinget" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Winget已安装" -ForegroundColor Green
Write-Host "当前Winget版本：" -ForegroundColor Cyan
winget --version
Write-Host ""

# 搜索Android Studio
Write-Host "2. 搜索Android Studio..." -ForegroundColor Yellow
$androidStudio = winget search --id Google.AndroidStudio --exact
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 未找到Android Studio，请检查网络连接或稍后重试。" -ForegroundColor Red
    exit 1
}

Write-Host "✅ 找到Android Studio：" -ForegroundColor Green
Write-Host $androidStudio
Write-Host ""

# 安装Android Studio
Write-Host "3. 开始安装Android Studio..." -ForegroundColor Yellow
Write-Host "这将自动下载并安装最新版本的Android Studio，可能需要一段时间..." -ForegroundColor Yellow
winget install --id Google.AndroidStudio --exact --accept-package-agreements --accept-source-agreements

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Android Studio安装失败！" -ForegroundColor Red
    Write-Host "请检查错误信息并手动安装Android Studio。" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Android Studio安装成功！" -ForegroundColor Green
Write-Host ""

# 安装Python依赖
Write-Host "4. 安装Python依赖..." -ForegroundColor Yellow

# 升级pip
Write-Host "   4.1 升级pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# 安装Kivy及相关依赖
Write-Host "   4.2 安装Kivy、Matplotlib、NumPy..." -ForegroundColor Cyan
python -m pip install kivy==2.3.1 matplotlib==3.10.8 numpy==2.2.6

# 安装Kivy Garden和Matplotlib后端
Write-Host "   4.3 安装Kivy Garden和Matplotlib后端..." -ForegroundColor Cyan
python -m pip install kivy-garden
python -m garden install matplotlib

# 安装Buildozer和Cython
Write-Host "   4.4 安装Buildozer和Cython..." -ForegroundColor Cyan
python -m pip install buildozer cython==0.29.32

Write-Host "✅ Python依赖安装完成！" -ForegroundColor Green
Write-Host ""

# 提示后续步骤
Write-Host "=== 安装完成！后续步骤 ===" -ForegroundColor Green
Write-Host ""
Write-Host "1. 启动Android Studio进行首次配置：" -ForegroundColor Yellow
Write-Host "   - 从开始菜单找到并打开Android Studio"
Write-Host "   - 首次启动时，选择'Do not import settings'"
Write-Host "   - 选择UI主题（Light或Darcula）"
Write-Host "   - 在SDK Components Setup中，确保勾选："
Write-Host "     * Android SDK"
Write-Host "     * Android SDK Platform"
Write-Host "     * Android Virtual Device"
Write-Host "     * Android SDK Build-Tools"
Write-Host "     * NDK (Side by Side)"
Write-Host "   - 等待SDK组件下载和安装完成"
Write-Host ""
Write-Host "2. 配置环境变量：" -ForegroundColor Yellow
Write-Host "   - 打开'系统属性' > '高级' > '环境变量'"
Write-Host "   - 在'系统变量'中添加："
Write-Host "     * ANDROID_SDK_ROOT = C:\Users\<用户名>\AppData\Local\Android\Sdk"
Write-Host "     * ANDROID_NDK_ROOT = C:\Users\<用户名>\AppData\Local\Android\Sdk\ndk\<版本号>"
Write-Host "   - 在'Path'变量中添加："
Write-Host "     * %ANDROID_SDK_ROOT%\platform-tools"
Write-Host "     * %ANDROID_SDK_ROOT%\tools"
Write-Host "     * %ANDROID_SDK_ROOT%\tools\bin"
Write-Host ""
Write-Host "3. 修改buildozer.spec文件：" -ForegroundColor Yellow
Write-Host "   - 打开d:\review\buildozer.spec文件"
Write-Host "   - 设置正确的SDK和NDK路径"
Write-Host "   - 确保android.api=31，android.minapi=21"
Write-Host "   - 确保android.ndk=25b（或与实际安装版本匹配）"
Write-Host ""
Write-Host "4. 开始构建APK：" -ForegroundColor Yellow
Write-Host "   - 打开PowerShell，进入d:\review目录"
Write-Host "   - 运行命令：buildozer android debug"
Write-Host "   - 构建成功后，APK文件将生成在bin目录下"
Write-Host ""
Write-Host "5. 常见问题参考：" -ForegroundColor Yellow
Write-Host "   - 查看MANUAL_APK_BUILD_GUIDE.md获取详细指南"
Write-Host "   - 查看ANDROID_STUDIO_MIRROR_DOWNLOAD.md获取Android Studio安装帮助"
Write-Host ""
Write-Host "祝您构建APK成功！" -ForegroundColor Green