#!/usr/bin/env python3
"""
Android APK 自动构建脚本
无需Docker或WSL，直接使用Python和python-for-android构建
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('build.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_command(cmd, cwd=None):
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
        logger.error(f"命令执行失败，返回码: {result.returncode}")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result


def install_dependencies():
    """安装构建依赖"""
    logger.info("=== 安装构建依赖 ===")
    
    # 升级pip
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # 安装python-for-android和cython
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "python-for-android", "cython"])
    
    logger.info("✅ 依赖安装完成")


def build_apk():
    """使用python-for-android构建APK"""
    logger.info("=== 开始构建APK ===")
    
    # 创建输出目录
    output_dir = Path("bin")
    output_dir.mkdir(exist_ok=True)
    logger.info(f"✅ 输出目录已创建: {output_dir.absolute()}")
    
    # 导入python-for-android的构建模块
    try:
        from pythonforandroid.build import main as p4a_main
        logger.info("✅ 成功导入python-for-android模块")
    except ImportError as e:
        logger.error(f"❌ 导入python-for-android失败: {e}")
        logger.error("请确保python-for-android已正确安装")
        return False
    
    # 准备构建参数
    build_args = [
        "apk",
        "--requirements", "python3,kivy==2.3.1,matplotlib==3.10.8,numpy==2.2.6",
        "--arch", "armeabi-v7a,arm64-v8a",
        "--bootstrap", "sdl2",
        "--name", "期货复盘",
        "--package", "org.futuresreview",
        "--version", "0.1",
        "--main", "main.py",
        "--window",
        "--permission", "INTERNET",
        "--output", str(output_dir / "futuresreview.apk"),
        "--verbose"
    ]
    
    logger.info(f"构建参数: {' '.join(build_args)}")
    
    try:
        # 调用python-for-android的构建函数
        logger.info("开始构建，首次构建可能需要30分钟以上，请耐心等待...")
        p4a_main(build_args)
        logger.info("✅ APK构建成功！")
        
        # 检查构建结果
        apk_files = list(output_dir.glob("*.apk"))
        if apk_files:
            for apk_file in apk_files:
                logger.info(f"📦 生成的APK文件: {apk_file.absolute()}")
            return True
        else:
            logger.error("❌ 构建成功但未找到APK文件")
            return False
            
    except Exception as e:
        logger.error(f"❌ APK构建失败: {e}", exc_info=True)
        logger.error("构建失败，请查看日志获取详细信息")
        return False


def main():
    """主函数"""
    logger.info("=========================================")
    logger.info("        Android APK 自动构建脚本        ")
    logger.info("=========================================")
    logger.info(f"Python版本: {sys.version}")
    logger.info(f"当前目录: {os.getcwd()}")
    
    try:
        # 安装依赖
        install_dependencies()
        
        # 构建APK
        success = build_apk()
        
        if success:
            logger.info("🎉 APK构建完成！")
            logger.info("=========================================")
            return 0
        else:
            logger.error("💥 APK构建失败！")
            logger.info("=========================================")
            return 1
            
    except Exception as e:
        logger.error(f"❌ 脚本执行失败: {e}", exc_info=True)
        logger.info("=========================================")
        return 1


if __name__ == "__main__":
    sys.exit(main())