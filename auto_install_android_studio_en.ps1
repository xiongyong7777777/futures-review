#!/usr/bin/env powershell

<#
.SYNOPSIS
Auto install Android Studio and related dependencies
.DESCRIPTION
This script uses Winget package manager to automatically download and install Android Studio,
then installs Kivy, Buildozer and other dependencies required for building APK.
#>

Write-Host "=== Auto Install Android Studio and APK Build Dependencies ===" -ForegroundColor Green
Write-Host ""

# Check if Winget is available
Write-Host "1. Checking Winget package manager..." -ForegroundColor Yellow
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Winget is not installed! Winget is a built-in package manager for Windows 10/11." -ForegroundColor Red
    Write-Host "Please ensure your Windows version is 10 1709 or later." -ForegroundColor Red
    Write-Host "You can install 'App Installer' from Microsoft Store to get Winget." -ForegroundColor Red
    Write-Host "Or visit: https://aka.ms/getwinget" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Winget is installed" -ForegroundColor Green
Write-Host "Current Winget version: " -ForegroundColor Cyan
winget --version
Write-Host ""

# Search for Android Studio
Write-Host "2. Searching for Android Studio..." -ForegroundColor Yellow
$androidStudio = winget search --id Google.AndroidStudio --exact
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Android Studio not found, please check network connection or try again later." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found Android Studio: " -ForegroundColor Green
Write-Host $androidStudio
Write-Host ""

# Install Android Studio
Write-Host "3. Starting Android Studio installation..." -ForegroundColor Yellow
Write-Host "This will automatically download and install the latest version of Android Studio, which may take some time..." -ForegroundColor Yellow
winget install --id Google.AndroidStudio --exact --accept-package-agreements --accept-source-agreements

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Android Studio installation failed!" -ForegroundColor Red
    Write-Host "Please check error messages and install Android Studio manually." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Android Studio installed successfully!" -ForegroundColor Green
Write-Host ""

# Install Python dependencies
Write-Host "4. Installing Python dependencies..." -ForegroundColor Yellow

# Upgrade pip
Write-Host "   4.1 Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install Kivy and related dependencies
Write-Host "   4.2 Installing Kivy, Matplotlib, NumPy..." -ForegroundColor Cyan
python -m pip install kivy==2.3.1 matplotlib==3.10.8 numpy==2.2.6

# Install Kivy Garden and Matplotlib backend
Write-Host "   4.3 Installing Kivy Garden and Matplotlib backend..." -ForegroundColor Cyan
python -m pip install kivy-garden
python -m garden install matplotlib

# Install Buildozer and Cython
Write-Host "   4.4 Installing Buildozer and Cython..." -ForegroundColor Cyan
python -m pip install buildozer cython==0.29.32

Write-Host "✅ Python dependencies installed successfully!" -ForegroundColor Green
Write-Host ""

# Prompt for next steps
Write-Host "=== Installation Complete! Next Steps ===" -ForegroundColor Green
Write-Host ""
Write-Host "1. Launch Android Studio for first-time configuration: " -ForegroundColor Yellow
Write-Host "   - Find and open Android Studio from Start Menu"
Write-Host "   - Select 'Do not import settings' when prompted"
Write-Host "   - Choose UI theme (Light or Darcula)"
Write-Host "   - In SDK Components Setup, ensure to check:"
Write-Host "     * Android SDK"
Write-Host "     * Android SDK Platform"
Write-Host "     * Android Virtual Device"
Write-Host "     * Android SDK Build-Tools"
Write-Host "     * NDK (Side by Side)"
Write-Host "   - Wait for SDK components to download and install"
Write-Host ""
Write-Host "2. Configure environment variables: " -ForegroundColor Yellow
Write-Host "   - Open 'System Properties' > 'Advanced' > 'Environment Variables'"
Write-Host "   - Add to 'System Variables':"
Write-Host "     * ANDROID_SDK_ROOT = C:\Users\<username>\AppData\Local\Android\Sdk"
Write-Host "     * ANDROID_NDK_ROOT = C:\Users\<username>\AppData\Local\Android\Sdk\ndk\<version>"
Write-Host "   - Add to 'Path' variable:"
Write-Host "     * %ANDROID_SDK_ROOT%\platform-tools"
Write-Host "     * %ANDROID_SDK_ROOT%\tools"
Write-Host "     * %ANDROID_SDK_ROOT%\tools\bin"
Write-Host ""
Write-Host "3. Modify buildozer.spec file: " -ForegroundColor Yellow
Write-Host "   - Open d:\review\buildozer.spec file"
Write-Host "   - Set correct SDK and NDK paths"
Write-Host "   - Ensure android.api=31, android.minapi=21"
Write-Host "   - Ensure android.ndk=25b (or match your installed version)"
Write-Host ""
Write-Host "4. Start building APK: " -ForegroundColor Yellow
Write-Host "   - Open PowerShell, navigate to d:\review directory"
Write-Host "   - Run command: buildozer android debug"
Write-Host "   - After successful build, APK file will be generated in bin directory"
Write-Host ""
Write-Host "5. Reference for common issues: " -ForegroundColor Yellow
Write-Host "   - Check MANUAL_APK_BUILD_GUIDE.md for detailed guide"
Write-Host "   - Check ANDROID_STUDIO_MIRROR_DOWNLOAD.md for Android Studio installation help"
Write-Host ""
Write-Host "Good luck with your APK build!" -ForegroundColor Green