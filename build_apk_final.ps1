Write-Host "=========================================" -ForegroundColor Green
Write-Host "        Android APK Build Script         " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# Create output directory
$binDir = Join-Path -Path $PSScriptRoot -ChildPath "bin"
if (!(Test-Path $binDir)) {
    New-Item -ItemType Directory -Path $binDir -Force | Out-Null
    Write-Host "✅ Output directory created: $binDir" -ForegroundColor Green
}

# Install dependencies
Write-Host "Installing build dependencies..." -ForegroundColor Cyan
pip install --upgrade python-for-android cython

# Build APK using p4a
Write-Host "Starting APK build..." -ForegroundColor Cyan
Write-Host "This may take a long time for the first build..." -ForegroundColor Yellow
Write-Host "First build may take 30+ minutes, please be patient..." -ForegroundColor Yellow

# Use p4a command to build APK
p4a apk --requirements python3,kivy==2.3.1,matplotlib==3.10.8,numpy==2.2.6 --arch armeabi-v7a,arm64-v8a --bootstrap sdl2 --name "FuturesReview" --package org.futuresreview --version 0.1 --main main.py --window --permission INTERNET --output $binDir/futuresreview.apk

# Check build result
Write-Host "Checking build result..." -ForegroundColor Cyan
$apkFile = Join-Path -Path $binDir -ChildPath "futuresreview.apk"
if (Test-Path $apkFile) {
    Write-Host "✅ APK build successful!" -ForegroundColor Green
    Write-Host "APK file location: $apkFile" -ForegroundColor Yellow
    Write-Host "" -ForegroundColor Green
    Write-Host "Usage Instructions:" -ForegroundColor Cyan
    Write-Host "1. Copy the APK file to your Android device" -ForegroundColor Cyan
    Write-Host "2. Enable 'Unknown sources' installation on your device" -ForegroundColor Cyan
    Write-Host "3. Tap the APK file to install" -ForegroundColor Cyan
    Write-Host "4. Open the app and start using it" -ForegroundColor Cyan
} else {
    Write-Host "❌ APK build failed!" -ForegroundColor Red
    Write-Host "Please check the command output and logs" -ForegroundColor Cyan
    Write-Host "Suggestions:" -ForegroundColor Cyan
    Write-Host "1. Ensure Android SDK and NDK are installed" -ForegroundColor Cyan
    Write-Host "2. Set ANDROID_HOME and ANDROID_NDK_HOME environment variables" -ForegroundColor Cyan
    Write-Host "3. Check network connection" -ForegroundColor Cyan
    Write-Host "4. Try using pip with Chinese mirror: pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple" -ForegroundColor Cyan
}

Write-Host "=========================================" -ForegroundColor Green
Write-Host "             Build Complete              " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green