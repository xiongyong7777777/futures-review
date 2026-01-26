#!/bin/bash
set -e

# 使用国内镜像源
sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# 安装依赖
apt-get update -qq
apt-get install -qq --yes --no-install-recommends python3 python3-pip openjdk-17-jdk

# 安装buildozer
pip3 install --upgrade buildozer cython

# 构建APK
buildozer android debug
