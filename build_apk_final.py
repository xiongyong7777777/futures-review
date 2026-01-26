#!/usr/bin/env python3
"""
Android APK 最终构建脚本
自动检测操作系统，Windows下使用Docker容器构建
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# 配置日志（修复中文编码问题）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('build.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def is_windows():
    """检查是否为Windows系统"""
    return sys.platform.startswith('win')


def run_command(cmd, cwd=None, ignore_error=False):
    """运行命令并返回结果"""
    logger.info(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        shell=False
    )
    if result.stdout:
        logger.info(f"命令输出:\n{result.stdout}")
    if result.stderr:
        logger.warning(f"命令错误:\n{result.stderr}")
    if result.returncode != 0:
        error_msg = f"命令执行失败，返回码: {result.returncode}"
        if ignore_error:
            logger.warning(error_msg)
        else:
            logger.error(error_msg)
            raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def check_docker():
    """检查Docker是否可用"""
    try:
        run_command(["docker", "--version"])
        run_command(["docker", "info"])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Docker不可用: {e}")
        return False


def build_without_docker():
    """不使用Docker的简化构建方案"""
    logger.info("=== 尝试不使用Docker的简化构建方案 ===")
    
    # 创建输出目录
    output_dir = Path("bin")
    output_dir.mkdir(exist_ok=True)
    logger.info(f"✅ 输出目录已创建: {output_dir.absolute()}")
    
    # 安装依赖
    logger.info("安装构建依赖...")
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "kivy==2.3.1", "matplotlib==3.10.8", "numpy==2.2.6"])
    
    # 生成一个简单的构建说明文件
    build_info = """# Android APK 构建说明

由于您的环境无法使用Docker或python-for-android，这里提供一个替代方案：

## 方案1：使用GitHub Actions在线构建
1. 将项目上传到GitHub仓库
2. 创建`.github/workflows/build.yml`文件，内容如下：

```yaml
name: Build Android APK
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install system dependencies
        run: |
          sudo apt update
          sudo apt install -y openjdk-17-jdk
      
      - name: Install Python dependencies
        run: |
          pip install --upgrade pip
          pip install buildozer cython
      
      - name: Build APK
        run: buildozer android debug --verbose
      
      - name: Upload APK artifact
        uses: actions/upload-artifact@v3
        with:
          name: futures-review-apk
          path: bin/*.apk
```

3. 推送代码，GitHub Actions会自动构建APK
4. 从Actions页面下载构建好的APK

## 方案2：手动构建
1. 安装Android Studio
2. 创建一个新的Android项目
3. 将您的Python代码集成到Android项目中
4. 使用Android Studio构建APK

## 方案3：使用云服务
1. 注册一个云服务器（如阿里云、腾讯云）
2. 选择Ubuntu 22.04系统
3. 在服务器上运行：
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y openjdk-17-jdk python3 python3-pip
   pip3 install buildozer cython
   buildozer android debug
   ```
4. 下载构建好的APK到本地
"""
    
    build_info_path = output_dir / "BUILD_INSTRUCTIONS.md"
    build_info_path.write_text(build_info, encoding='utf-8')
    logger.info(f"✅ 构建说明已生成: {build_info_path.absolute()}")
    logger.info("请查看BUILD_INSTRUCTIONS.md文件获取详细构建方案")
    return False


def main():
    """主函数"""
    logger.info("=========================================")
    logger.info("        Android APK 最终构建脚本        ")
    logger.info("=========================================")
    logger.info(f"Python版本: {sys.version}")
    logger.info(f"当前操作系统: {sys.platform}")
    logger.info(f"当前目录: {os.getcwd()}")
    
    try:
        if is_windows():
            logger.info("检测到Windows系统，尝试使用Docker容器构建APK")
            
            # 检查Docker是否可用
            if not check_docker():
                logger.warning("Docker不可用，尝试简化构建方案")
                return build_without_docker()
            
            # 尝试使用简化的Docker构建方式
            logger.info("尝试使用简化的Docker构建方式...")
            
            # 创建一个简单的构建脚本
            build_script_content = """#!/bin/bash
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
"""
            
            build_script_path = Path("build_android.sh")
            build_script_path.write_text(build_script_content, encoding='utf-8')
            
            try:
                # 尝试使用kivy/buildozer镜像
                logger.info("尝试使用kivy/buildozer镜像构建...")
                run_command([
                    "docker", "run", "--rm", 
                    "-v", f"{os.getcwd()}:/home/user/app", 
                    "-w", "/home/user/app", 
                    "kivy/buildozer",
                    "bash", "-c", "pip install --upgrade buildozer cython && buildozer android debug"
                ])
            except subprocess.CalledProcessError:
                # 尝试使用ubuntu镜像
                logger.info("尝试使用ubuntu镜像构建...")
                run_command([
                    "docker", "run", "--rm", 
                    "-v", f"{os.getcwd()}:/app", 
                    "-w", "/app", 
                    "ubuntu:22.04",
                    "bash", "-c", build_script_content
                ])
            except subprocess.CalledProcessError as e:
                logger.error(f"Docker构建失败: {e}")
                logger.info("尝试使用简化构建方案...")
                return build_without_docker()
            
            # 清理构建脚本
            build_script_path.unlink()
            
            # 检查构建结果
            output_dir = Path("bin")
            apk_files = list(output_dir.glob("*.apk"))
            if apk_files:
                for apk_file in apk_files:
                    logger.info(f"🎉 构建成功！APK文件: {apk_file.absolute()}")
                return 0
            else:
                logger.error("❌ 构建失败，未找到APK文件")
                return 1
                
        else:
            logger.info("检测到Linux/macOS系统，将直接构建APK")
            
            # 安装依赖
            run_command([sys.executable, "-m", "pip", "install", "--upgrade", "python-for-android", "cython"])
            
            # 直接构建APK
            run_command([
                sys.executable, "-m", "pythonforandroid", "apk",
                "--requirements", "python3,kivy==2.3.1,matplotlib==3.10.8,numpy==2.2.6",
                "--arch", "armeabi-v7a,arm64-v8a",
                "--bootstrap", "sdl2",
                "--name", "期货复盘",
                "--package", "org.futuresreview",
                "--version", "0.1",
                "--main", "main.py",
                "--window",
                "--permission", "INTERNET",
                "--output", "bin/futuresreview.apk"
            ])
            
            # 检查构建结果
            output_dir = Path("bin")
            apk_files = list(output_dir.glob("*.apk"))
            if apk_files:
                for apk_file in apk_files:
                    logger.info(f"🎉 构建成功！APK文件: {apk_file.absolute()}")
                return 0
            else:
                logger.error("❌ 构建失败，未找到APK文件")
                return 1
                
    except Exception as e:
        logger.error(f"❌ 脚本执行失败: {e}", exc_info=True)
        logger.info("=========================================")
        logger.error("💥 APK构建失败！")
        logger.info("尝试使用简化构建方案...")
        build_without_docker()
        logger.info("=========================================")
        return 1


if __name__ == "__main__":
    sys.exit(main())