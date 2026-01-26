#!/usr/bin/env powershell

Write-Host "=== Docker网络问题修复 ===" -ForegroundColor Green
Write-Host ""

# 检查网络连接
Write-Host "1. 检查网络连接..." -ForegroundColor Yellow
if (Test-Connection www.baidu.com -Count 1 -Quiet) {
    Write-Host "✅ 网络连接正常" -ForegroundColor Green
} else {
    Write-Host "❌ 网络连接异常" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 修复1：使用更可靠的阿里云镜像源
Write-Host "2. 配置阿里云Docker镜像源..." -ForegroundColor Yellow

# 生成阿里云镜像源配置
$aliyunConfig = @{
    "registry-mirrors" = @(
        "https://registry.cn-hangzhou.aliyuncs.com"
    )
}

# 保存配置文件
$dockerConfigPath = "$env:USERPROFILE\.docker\daemon.json"
$aliyunConfig | ConvertTo-Json | Set-Content $dockerConfigPath

Write-Host "✅ 阿里云镜像源已配置" -ForegroundColor Green
Write-Host "配置文件：$dockerConfigPath" -ForegroundColor Cyan
Write-Host ""

# 修复2：禁用Docker的IPv6
Write-Host "3. 禁用Docker IPv6..." -ForegroundColor Yellow

# 添加IPv6禁用配置
$dockerConfig = Get-Content $dockerConfigPath | ConvertFrom-Json
$dockerConfig | Add-Member -MemberType NoteProperty -Name "ipv6" -Value $false -Force
$dockerConfig | ConvertTo-Json | Set-Content $dockerConfigPath

Write-Host "✅ Docker IPv6已禁用" -ForegroundColor Green
Write-Host ""

Write-Host "⚠️  请手动重启Docker Desktop以应用配置！" -ForegroundColor Yellow
Write-Host "重启步骤：" -ForegroundColor Cyan
Write-Host "1. 右键点击任务栏中的Docker图标" -ForegroundColor Cyan
Write-Host "2. 选择'Quit Docker Desktop'" -ForegroundColor Cyan
Write-Host "3. 等待Docker完全退出" -ForegroundColor Cyan
Write-Host "4. 重新启动Docker Desktop" -ForegroundColor Cyan
Write-Host ""

Write-Host "=== 修复完成！ ===" -ForegroundColor Green
Write-Host "重启Docker后，尝试以下命令构建APK：" -ForegroundColor Yellow
Write-Host "docker run --rm -v ${PWD}:/home/user/app -w /home/user/app kivy/buildozer buildozer android debug" -ForegroundColor Cyan