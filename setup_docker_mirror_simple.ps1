#!/usr/bin/env powershell

Write-Host "=== 配置Docker国内镜像源 ===" -ForegroundColor Green
Write-Host ""

# 检查Docker是否安装
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker未安装！请先安装Docker Desktop。" -ForegroundColor Red
    exit 1
}

# 国内镜像源配置
$mirrorConfig = @{
    "registry-mirrors" = @(
        "https://docker.mirrors.ustc.edu.cn",
        "https://hub-mirror.c.163.com",
        "https://registry.docker-cn.com"
    )
}

# 保存配置文件
$dockerConfigPath = "$env:USERPROFILE\.docker\daemon.json"
$mirrorConfig | ConvertTo-Json | Set-Content $dockerConfigPath

Write-Host "✅ Docker镜像源配置已保存到: $dockerConfigPath" -ForegroundColor Green
Write-Host ""
Write-Host "📋 配置内容：" -ForegroundColor Cyan
$mirrorConfig | ConvertTo-Json
Write-Host ""
Write-Host "⚠️  请手动重启Docker Desktop以应用配置！" -ForegroundColor Yellow
Write-Host "重启步骤：" -ForegroundColor Cyan
Write-Host "1. 右键点击任务栏中的Docker图标" -ForegroundColor Cyan
Write-Host "2. 选择'Quit Docker Desktop'" -ForegroundColor Cyan
Write-Host "3. 等待Docker完全退出" -ForegroundColor Cyan
Write-Host "4. 重新启动Docker Desktop" -ForegroundColor Cyan
Write-Host ""
Write-Host "=== 配置完成！ ===" -ForegroundColor Green