#!/usr/bin/env powershell

Write-Host "=========================================" -ForegroundColor Green
Write-Host "         Docker APK Build Script         " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Pull Buildozer image
Write-Host "Pulling Buildozer Docker image..." -ForegroundColor Yellow
Write-Host "This may take a while on first run..." -ForegroundColor Cyan
docker pull jedie/buildozer

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to pull Docker image!" -ForegroundColor Red
    Write-Host "Please check your network connection." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image pulled successfully" -ForegroundColor Green
Write-Host ""

# Build APK in Docker container
Write-Host "Building APK in Docker container..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Cyan
docker run --rm -v ${PWD}:/home/user/app -w /home/user/app jedie/buildozer buildozer android debug

Write-Host ""

# Check build results
Write-Host "Checking build results..." -ForegroundColor Yellow
$apkFiles = Get-ChildItem -Path "bin" -Filter "*.apk" -ErrorAction SilentlyContinue

if ($apkFiles) {
    Write-Host "✅ APK build successful! Generated files:" -ForegroundColor Green
    $apkFiles | ForEach-Object {
        Write-Host "   - $($_.FullName)" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Usage Instructions:" -ForegroundColor Cyan
    Write-Host "1. Copy the APK file to your Android device" -ForegroundColor Cyan
    Write-Host "2. Enable 'Unknown sources' installation on your device" -ForegroundColor Cyan
    Write-Host "3. Tap the APK file to install" -ForegroundColor Cyan
    Write-Host "4. Open the app and start using it" -ForegroundColor Cyan
} else {
    Write-Host "❌ Build failed or no APK files found!" -ForegroundColor Red
    Write-Host "Check build logs: .buildozer/android/build.log" -ForegroundColor Cyan
    Write-Host "Use this command to view logs: Get-Content .buildozer/android/build.log -Tail 100" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "               Build Complete            " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green