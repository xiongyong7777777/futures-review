#!/usr/bin/env python3
"""
直接使用python-for-android构建APK的脚本
"""

import os
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    try:
        logger.info("=== 开始直接构建APK ===")
        
        # 检查python-for-android是否安装
        try:
            from pythonforandroid.build import main as p4a_main
            logger.info("✅ python-for-android已安装")
        except ImportError:
            logger.error("❌ python-for-android未安装")
            logger.info("正在安装python-for-android...")
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "python-for-android"], check=True)
            from pythonforandroid.build import main as p4a_main
            logger.info("✅ python-for-android安装成功")
        
        # 构建命令参数
        # 这里我们使用python-for-android的API来构建APK
        # 注意：这需要配置好Android SDK和NDK环境
        
        logger.info("⚠️  注意：直接使用python-for-android需要配置好Android SDK和NDK环境")
        logger.info("⚠️  建议使用Android Studio自动配置环境")
        
        # 检查必要的环境变量
        required_vars = ["ANDROID_HOME", "ANDROID_NDK_HOME"]
        missing_vars = []
        for var in required_vars:
            if var not in os.environ:
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
            logger.info("请先配置Android SDK和NDK环境，或使用Docker方案")
            logger.info("推荐使用Android Studio安装并配置SDK和NDK")
            return 1
        
        logger.info(f"✅ ANDROID_HOME: {os.environ['ANDROID_HOME']}")
        logger.info(f"✅ ANDROID_NDK_HOME: {os.environ['ANDROID_NDK_HOME']}")
        
        # 准备构建命令
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
            "--output", "bin/futuresreview.apk"
        ]
        
        logger.info(f"构建参数: {' '.join(build_args)}")
        
        # 调用python-for-android构建
        logger.info("开始构建APK...")
        logger.info("这可能需要较长时间，首次构建会下载大量依赖...")
        
        # 注意：这里直接调用API可能需要调整参数格式
        # 由于直接API调用较为复杂，我们使用subprocess调用p4a命令
        import subprocess
        
        result = subprocess.run([sys.executable, "-m", "pythonforandroid", "apk"] + build_args[1:], 
                               capture_output=True, text=True)
        
        logger.info(f"构建返回码: {result.returncode}")
        
        if result.stdout:
            logger.info(f"构建输出:\n{result.stdout}")
        
        if result.stderr:
            logger.error(f"构建错误:\n{result.stderr}")
        
        if result.returncode == 0:
            logger.info("✅ APK构建成功！")
            logger.info(f"APK文件位置: {os.path.join(os.getcwd(), 'bin', 'futuresreview.apk')}")
            return 0
        else:
            logger.error("❌ APK构建失败！")
            logger.info("建议检查日志并配置好Android环境，或使用Docker方案")
            return 1
            
    except Exception as e:
        logger.error(f"❌ 构建过程中发生错误: {str(e)}")
        logger.error("建议使用Docker方案构建APK")
        return 1

if __name__ == "__main__":
    sys.exit(main())