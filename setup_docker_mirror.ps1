#!/usr/bin/env powershell

<#
.SYNOPSIS
配置Docker使用国内镜像源加速
.DESCRIPTION
本脚本修改Docker配置，添加国内镜像源，解决Docker Hub连接问题
#>

Write-Host "=== 配置Docker国内镜像源 ===" -ForegroundColor Green
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

# Docker配置文件路径
$dockerConfigPath = "$env:USERPROFILE\.docker\daemon.json"

# 国内镜像源列表
$mirrorList = @(
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://registry.docker-cn.com",
    "https://cr.console.aliyun.com"
)

# 创建或修改配置文件
Write-Host "2. 配置Docker镜像源..." -ForegroundColor Yellow

$dockerConfig = @{}

# 如果配置文件存在，读取现有配置
if (Test-Path $dockerConfigPath) {
    Write-Host "   读取现有配置文件..." -ForegroundColor Cyan
    $dockerConfig = Get-Content $dockerConfigPath | ConvertFrom-Json
}

# 添加镜像源配置
if (-not $dockerConfig.psobject.properties.name -contains "registry-mirrors") {
    $dockerConfig | Add-Member -MemberType NoteProperty -Name "registry-mirrors" -Value $mirrorList
    Write-Host "   添加镜像源配置..." -ForegroundColor Cyan
} else {
    # 合并现有镜像源和新镜像源
    $existingMirrors = $dockerConfig."registry-mirrors"
    $mergedMirrors = ($existingMirrors + $mirrorList) | Select-Object -Unique
    $dockerConfig."registry-mirrors" = $mergedMirrors
    Write-Host "   合并镜像源配置..." -ForegroundColor Cyan
}

# 保存配置文件
Write-Host "   保存配置文件..." -ForegroundColor Cyan
$dockerConfig | ConvertTo-Json | Set-Content $dockerConfigPath

# 重启Docker服务
Write-Host "3. 重启Docker服务..." -ForegroundColor Yellow

# 在Windows上，我们需要重启Docker Desktop
Write-Host "   请手动重启Docker Desktop以应用配置！" -ForegroundColor Yellow
Write-Host "   重启步骤：" -ForegroundColor Cyan
Write-Host "   1. 右键点击任务栏中的Docker图标" -ForegroundColor Cyan
Write-Host "   2. 选择'Quit Docker Desktop'" -ForegroundColor Cyan
Write-Host "   3. 等待Docker完全退出" -ForegroundColor Cyan
Write-Host "   4. 重新启动Docker Desktop" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== 配置完成！ ===" -ForegroundColor Green
Write-Host ""
Write-Host "镜像源已添加到Docker配置文件：" -ForegroundColor Yellow
$mirrorList | ForEach-Object {
    Write-Host "   - $_" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "重启Docker后，运行以下命令测试：" -ForegroundColor Yellow
Write-Host "   docker pull kivy/buildozer" -ForegroundColor Cyan
Write-Host ""
Write-Host "然后运行构建脚本：" -ForegroundColor Yellow
Write-Host "   .\build_apk_docker.ps1" -ForegroundColor Cyan