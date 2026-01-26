#!/usr/bin/env powershell

Write-Host "=========================================" -ForegroundColor Green
Write-Host "        Android APK Auto Build Script    " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Create output directory
$binDir = Join-Path -Path $PSScriptRoot -ChildPath "bin"
if (!(Test-Path $binDir)) {
    New-Item -ItemType Directory -Path $binDir -Force | Out-Null
    Write-Host "✅ Output directory created: $binDir" -ForegroundColor Green
}

# Display build options
Write-Host "\n=== Please Select Build Option ===" -ForegroundColor Yellow
Write-Host "1. Docker Build (Recommended, no complex setup)" -ForegroundColor Cyan
Write-Host "2. Direct Build (Requires Android SDK & NDK)" -ForegroundColor Cyan
Write-Host "3. Exit" -ForegroundColor Cyan

$choice = Read-Host -Prompt "Enter option (1-3)"

switch ($choice) {
    "1" {
        Write-Host "\nYou selected Docker Build..." -ForegroundColor Green
        Write-Host "Executing Docker build script..." -ForegroundColor Cyan
        
        # Run Docker build script
        $dockerBuildScript = Join-Path -Path $PSScriptRoot -ChildPath "build_apk_docker_fixed.ps1"
        if (Test-Path $dockerBuildScript) {
            & $dockerBuildScript
            exit $LASTEXITCODE
        } else {
            Write-Host "❌ Docker build script not found: $dockerBuildScript" -ForegroundColor Red
            exit 1
        }
    }
    "2" {
        Write-Host "\nYou selected Direct Build..." -ForegroundColor Green
        Write-Host "Executing direct build script..." -ForegroundColor Cyan
        
        # Run direct build script
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
        Write-Host "\nExiting build process..." -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "\n❌ Invalid option, please enter a number between 1-3" -ForegroundColor Red
        exit 1
    }
}