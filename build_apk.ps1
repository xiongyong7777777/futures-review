Write-Host "=========================================" -ForegroundColor Green
Write-Host "        Android APK 自动构建脚本        " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# 设置执行策略（如果需要）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# 检测操作系统
$os = [Environment]::OSVersion
Write-Host "当前操作系统：$($os.Platform) $($os.Version)" -ForegroundColor Cyan

# 创建输出目录
$binDir = Join-Path -Path $PSScriptRoot -ChildPath "bin"
if (!(Test-Path $binDir)) {
    New-Item -ItemType Directory -Path $binDir -Force | Out-Null
    Write-Host "✅ 输出目录已创建: $binDir" -ForegroundColor Green
}

# 提供构建方案选择
Write-Host "\n=== 请选择构建方案 ===" -ForegroundColor Yellow
Write-Host "1. Docker方案（推荐，无需配置复杂环境）" -ForegroundColor Cyan
Write-Host "2. 直接构建方案（需要配置Android SDK和NDK）" -ForegroundColor Cyan
Write-Host "3. 退出" -ForegroundColor Cyan

$choice = Read-Host -Prompt "请输入选项 (1-3)"

switch ($choice) {
    "1" {
        Write-Host "\n您选择了Docker方案构建APK..." -ForegroundColor Green
        Write-Host "正在执行Docker构建脚本..." -ForegroundColor Cyan
        
        # 运行Docker构建脚本
        $dockerBuildScript = Join-Path -Path $PSScriptRoot -ChildPath "build_apk_docker_simple.ps1"
        if (Test-Path $dockerBuildScript) {
            & $dockerBuildScript
            exit $LASTEXITCODE
        } else {
            Write-Host "❌ Docker build script not found: $dockerBuildScript" -ForegroundColor Red
            exit 1
        }
    }
    "2" {
        Write-Host "\n您选择了直接构建方案..." -ForegroundColor Green
        Write-Host "正在执行直接构建脚本..." -ForegroundColor Cyan
        
        # 运行直接构建脚本
        $directBuildScript = Join-Path -Path $PSScriptRoot -ChildPath "build_apk_direct.py"
        if (Test-Path $directBuildScript) {
            python $directBuildScript
            exit $LASTEXITCODE
        } else {
            Write-Host "❌ Direct build script not found: $directBuildScript" -ForegroundColor Red
            exit 1
        }
    }
    "3" {
        Write-Host "\n已退出构建程序" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "\n❌ 无效选项，请输入1-3之间的数字" -ForegroundColor Red
        exit 1
    }
}