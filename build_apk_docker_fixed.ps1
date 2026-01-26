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

# Create a custom Dockerfile for buildozer
Write-Host "Creating custom Buildozer Docker image..." -ForegroundColor Yellow
Write-Host "This will build a custom Docker image with buildozer..." -ForegroundColor Cyan

# Create Dockerfile content
$dockerfileContent = @"
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Use Aliyun mirror for faster downloads in China
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# Install system dependencies
RUN apt-get update -qq && apt-get install -qq --yes --no-install-recommends \
    ca-certificates \
    curl \
    git \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    python3-venv \
    unzip \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install buildozer and dependencies
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install buildozer cython

# Create a user for build process
RUN useradd --create-home --shell /bin/bash builduser && \
    mkdir -p /home/builduser/app && \
    chown -R builduser:builduser /home/builduser

USER builduser
WORKDIR /home/builduser/app

# Initialize buildozer config (this creates the .buildozer directory)
RUN buildozer init

# Set entrypoint to buildozer
ENTRYPOINT ["buildozer"]
"@

# Write Dockerfile to current directory
$dockerfilePath = Join-Path -Path $PSScriptRoot -ChildPath "Dockerfile.buildozer"
Set-Content -Path $dockerfilePath -Value $dockerfileContent

Write-Host "✅ Custom Dockerfile created: $dockerfilePath" -ForegroundColor Green

# Build custom Docker image
Write-Host "Building custom Buildozer Docker image..." -ForegroundColor Yellow
Write-Host "This may take a while..." -ForegroundColor Cyan

docker build --tag=custom-buildozer --file $dockerfilePath .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to build custom Docker image!" -ForegroundColor Red
    Write-Host "Please check your network connection and try again." -ForegroundColor Red
    # Clean up
    Remove-Item -Path $dockerfilePath -Force -ErrorAction SilentlyContinue
    exit 1
}

# Clean up Dockerfile
Remove-Item -Path $dockerfilePath -Force -ErrorAction SilentlyContinue

Write-Host "✅ Custom Docker image built successfully: custom-buildozer" -ForegroundColor Green
Write-Host ""

# Build APK in Docker container
Write-Host "Building APK in Docker container..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Cyan
Write-Host "First build will download many dependencies, please be patient..." -ForegroundColor Cyan

docker run --rm -v ${PWD}:/home/builduser/app -w /home/builduser/app custom-buildozer android debug

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
    Write-Host ""
    Write-Host "Alternative option: Try the direct build method if you have Android SDK/NDK configured" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "               Build Complete            " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green