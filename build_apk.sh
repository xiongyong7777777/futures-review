#!/bin/bash

# 构建脚本：自动创建期货复盘APK

echo "开始构建期货复盘APK..."

# 1. 设置环境变量
export ANDROID_SDK_ROOT="$HOME/Android/Sdk"
export ANDROID_NDK_ROOT="$ANDROID_SDK_ROOT/ndk/25.2.9519653"

# 2. 创建并激活虚拟环境
echo "创建虚拟环境..."
python3 -m venv buildozer-venv
source buildozer-venv/bin/activate

# 3. 安装依赖
echo "安装依赖..."
pip install --upgrade buildozer cython

# 4. 构建APK
echo "开始构建APK..."
buildozer -v android debug

echo "构建完成！APK文件位于 ./bin/ 目录中。"
