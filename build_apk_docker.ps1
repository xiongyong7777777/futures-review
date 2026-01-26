#!/usr/bin/env powershell

<#
.SYNOPSIS
使用Docker构建APK
.DESCRIPTION
本脚本使用Kivy官方Docker镜像构建APK，避免本地环境配置问题
#>

Write-Host "=== 使用Docker构建APK ===" -ForegroundColor Green
Write-Host ""

# 检查Docker是否运行
Write-Host "1. 检查Docker状态..." -ForegroundColor Yellow
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker未安装！" -ForegroundColor Red
    Write-Host "请先安装Docker Desktop。" -ForegroundColor Red
    exit 1
}

try {
    docker info | Out-Null
    Write-Host "✅ Docker正在运行" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker未运行！" -ForegroundColor Red
    Write-Host "请先启动Docker Desktop。" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 拉取Kivy Docker镜像（使用国内镜像源）
Write-Host "2. 拉取Kivy Docker镜像..." -ForegroundColor Yellow
Write-Host "   注意：如果拉取失败，请先运行setup_docker_mirror.ps1配置国内镜像源" -ForegroundColor Cyan
docker pull kivy/buildozer

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 拉取镜像失败！" -ForegroundColor Red
    Write-Host "请检查网络连接或先运行setup_docker_mirror.ps1配置国内镜像源。" -ForegroundColor Red
    exit 1
}

Write-Host "✅ 镜像拉取成功" -ForegroundColor Green
Write-Host ""

# 运行Docker容器构建APK
Write-Host "3. 启动Docker容器构建APK..." -ForegroundColor Yellow
Write-Host "   这将在Docker容器中构建APK，可能需要一段时间..." -ForegroundColor Cyan
docker run --rm -v ${PWD}:/home/user/app -w /home/user/app kivy/buildozer buildozer android debug

Write-Host ""

# 检查构建结果
Write-Host "4. 检查构建结果..." -ForegroundColor Yellow
$apkFiles = Get-ChildItem -Path "bin" -Filter "*.apk" -ErrorAction SilentlyContinue

if ($apkFiles) {
    Write-Host "✅ APK构建成功！生成的文件：" -ForegroundColor Green
    $apkFiles | ForEach-Object {
        Write-Host "   - $($_.FullName)" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "使用说明：" -ForegroundColor Cyan
    Write-Host "1. 将APK文件复制到Android设备" -ForegroundColor Cyan
    Write-Host "2. 在设备上启用'未知来源'安装" -ForegroundColor Cyan
    Write-Host "3. 点击APK文件进行安装" -ForegroundColor Cyan
    Write-Host "4. 打开应用进行期货复盘数据录入和分析" -ForegroundColor Cyan
} else {
    Write-Host "❌ 构建失败，请查看日志。" -ForegroundColor Red
    Write-Host "构建日志保存在：.buildozer/android/build.log" -ForegroundColor Cyan
    Write-Host "您可以使用以下命令查看日志：" -ForegroundColor Cyan
    Write-Host "   Get-Content .buildozer/android/build.log -Tail 100" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== 构建完成 ===" -ForegroundColor Green