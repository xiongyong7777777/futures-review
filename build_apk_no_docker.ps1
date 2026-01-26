Write-Host "=========================================" -ForegroundColor Green
Write-Host "        Android APK 直接构建脚本        " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# 设置执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# 安装依赖
Write-Host "安装构建依赖..." -ForegroundColor Cyan
pip install --upgrade python-for-android cython

# 创建输出目录
$binDir = Join-Path -Path $PSScriptRoot -ChildPath "bin"
if (!(Test-Path $binDir)) {
    New-Item -ItemType Directory -Path $binDir -Force | Out-Null
    Write-Host "✅ 输出目录已创建: $binDir" -ForegroundColor Green
}

# 构建APK
Write-Host "开始构建APK..." -ForegroundColor Cyan
Write-Host "这可能需要较长时间，首次构建会下载大量依赖..." -ForegroundColor Yellow
Write-Host "首次构建可能需要30分钟以上，请耐心等待..." -ForegroundColor Yellow

# 使用p4a命令构建APK
p4a apk --requirements python3,kivy==2.3.1,matplotlib==3.10.8,numpy==2.2.6 --arch armeabi-v7a,arm64-v8a --bootstrap sdl2 --name "期货复盘" --package org.futuresreview --version 0.1 --main main.py --window --permission INTERNET --output $binDir/futuresreview.apk

# 检查构建结果
Write-Host "检查构建结果..." -ForegroundColor Cyan
$apkFile = Join-Path -Path $binDir -ChildPath "futuresreview.apk"
if (Test-Path $apkFile) {
    Write-Host "✅ APK构建成功！" -ForegroundColor Green
    Write-Host "APK文件位置: $apkFile" -ForegroundColor Yellow
    Write-Host "" -ForegroundColor Green
    Write-Host "使用说明：" -ForegroundColor Cyan
    Write-Host "1. 将APK文件复制到Android设备" -ForegroundColor Cyan
    Write-Host "2. 在设备上启用'未知来源'安装" -ForegroundColor Cyan
    Write-Host "3. 点击APK文件进行安装" -ForegroundColor Cyan
    Write-Host "4. 打开应用开始使用" -ForegroundColor Cyan
} else {
    Write-Host "❌ APK构建失败！" -ForegroundColor Red
    Write-Host "请检查命令输出和日志" -ForegroundColor Cyan
    Write-Host "建议：" -ForegroundColor Cyan
    Write-Host "1. 确保已安装并配置好Android SDK和NDK" -ForegroundColor Cyan
    Write-Host "2. 设置ANDROID_HOME和ANDROID_NDK_HOME环境变量" -ForegroundColor Cyan
    Write-Host "3. 检查网络连接是否稳定" -ForegroundColor Cyan
    Write-Host "4. 尝试使用VPN或更换网络" -ForegroundColor Cyan
}

Write-Host "=========================================" -ForegroundColor Green
Write-Host "               构建完成                 " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green