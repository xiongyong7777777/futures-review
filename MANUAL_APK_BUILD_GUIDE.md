# Windows系统手动创建APK指南

由于自动构建脚本可能遇到环境问题，本指南提供在Windows系统下手动安装创建APK所需软件的详细步骤。

## 一、安装Python环境

1. **下载Python 3.8+**
   - 访问 [Python官网](https://www.python.org/downloads/windows/)
   - 下载最新的Python 3.8+安装包（推荐3.10）
   - 安装时勾选"Add Python to PATH"

2. **升级pip**
   ```powershell
   python -m pip install --upgrade pip
   ```

3. **安装虚拟环境（可选但推荐）**
   ```powershell
   pip install virtualenv
   ```

## 二、安装Kivy和相关依赖

1. **安装Kivy**
   ```powershell
   pip install kivy==2.3.1
   ```

2. **安装项目依赖**
   ```powershell
   pip install matplotlib==3.10.8 numpy==2.2.6
   ```

3. **安装Kivy Garden和Matplotlib后端**
   ```powershell
   pip install kivy-garden
   garden install matplotlib
   ```

## 三、安装Buildozer

1. **安装Buildozer**
   ```powershell
   pip install buildozer
   ```

2. **安装Cython**
   ```powershell
   pip install cython==0.29.32
   ```

## 四、安装Android SDK和NDK

### 方法1：使用Android Studio（推荐）

1. **下载并安装Android Studio**
   - 访问 [Android Studio官网](https://developer.android.com/studio)
   - 下载并安装最新版本

2. **安装SDK和NDK**
   - 打开Android Studio
   - 点击"Configure" > "SDK Manager"
   - 在"SDK Platforms"选项卡中，勾选以下内容：
     - Android 12.0 (S) - API级别31（与buildozer.spec中的android.api匹配）
     - Android 5.0 (Lollipop) - API级别21（最低支持版本）
   - 在"SDK Tools"选项卡中，勾选以下内容：
     - Android SDK Build-Tools
     - Android SDK Platform-Tools
     - Android SDK Tools
     - NDK (Side by Side) - 版本25.1.8937393（与buildozer.spec中的android.ndk匹配）
     - CMake
   - 点击"Apply"安装所选组件

3. **配置环境变量**
   - 打开"系统属性" > "高级" > "环境变量"
   - 在"系统变量"中添加以下变量：
     - `ANDROID_SDK_ROOT` = `C:\Users\<用户名>\AppData\Local\Android\Sdk`
     - `ANDROID_NDK_ROOT` = `C:\Users\<用户名>\AppData\Local\Android\Sdk\ndk\25.1.8937393`
   - 在"Path"变量中添加：
     - `%ANDROID_SDK_ROOT%\platform-tools`
     - `%ANDROID_SDK_ROOT%\tools`
     - `%ANDROID_SDK_ROOT%\tools\bin`

### 方法2：手动安装（不推荐）

1. **下载SDK Command Line Tools**
   - 访问 [Android开发者官网](https://developer.android.com/studio#command-tools)
   - 下载适合Windows的Command Line Tools
   - 解压到 `C:\Android\cmdline-tools`

2. **安装SDK组件**
   ```powershell
   cd C:\Android\cmdline-tools\bin
   sdkmanager "platforms;android-31" "platforms;android-21" "build-tools;31.0.0" "platform-tools" "ndk;25.1.8937393"
   ```

3. **配置环境变量**
   - 设置 `ANDROID_SDK_ROOT` = `C:\Android`
   - 设置 `ANDROID_NDK_ROOT` = `C:\Android\ndk\25.1.8937393`
   - 在Path中添加相应路径

## 五、配置Buildozer

1. **修改buildozer.spec文件**
   - 打开 `buildozer.spec` 文件
   - 确保以下配置正确：
     ```ini
     # (str) Application requirements
     requirements = python3,kivy==2.3.1,matplotlib==3.10.8,numpy==2.2.6
     
     # (int) Target Android API
     android.api = 31
     
     # (int) Minimum API your APK will support
     android.minapi = 21
     
     # (str) Android NDK version to use
     android.ndk = 25b
     
     # (int) Android NDK API to use
     android.ndk_api = 21
     
     # (str) The Android arch to build for
     android.archs = armeabi-v7a,arm64-v8a
     ```

2. **设置Android SDK和NDK路径**
   - 在 `buildozer.spec` 中添加：
     ```ini
     # (str) Android SDK directory
     android.sdk_path = C:\Users\<用户名>\AppData\Local\Android\Sdk
     
     # (str) Android NDK directory
     android.ndk_path = C:\Users\<用户名>\AppData\Local\Android\Sdk\ndk\25.1.8937393
     ```

## 六、手动构建APK

1. **进入项目目录**
   ```powershell
   cd d:\review
   ```

2. **初始化Buildozer环境**
   ```powershell
   buildozer init
   ```

3. **清理之前的构建（如果有）**
   ```powershell
   buildozer android clean
   ```

4. **开始构建APK**
   ```powershell
   buildozer android debug
   ```

5. **查看构建日志**
   - 构建过程中会显示日志
   - 完整日志保存在 `.buildozer\android\build.log`

6. **获取生成的APK**
   - 构建成功后，APK文件将生成在 `bin` 目录下
   - 文件名格式：`futuresreview-0.1-debug.apk`

## 七、常见问题及解决方案

### 1. ModuleNotFoundError: No module named 'distutils'
**解决方案：**
```powershell
pip install setuptools
```

### 2. Android SDK License Issues
**解决方案：**
```powershell
# 自动接受SDK许可证
buildozer android update_sdk --accept-licenses
```

### 3. NDK版本不匹配
**解决方案：**
- 确保buildozer.spec中的android.ndk与安装的NDK版本匹配
- 推荐使用NDK 25.1.8937393（对应25b）

### 4. 内存不足错误
**解决方案：**
- 增加Buildozer的Java堆内存
- 在buildozer.spec中添加：
  ```ini
  # (str) Java compiler options
  android.javac_options = -Xmx4g
  ```

### 5. 构建速度慢
**解决方案：**
- 确保使用高速网络（首次构建需要下载大量依赖）
- 关闭杀毒软件或防火墙（临时）

## 八、测试APK

1. **使用Kivy Launcher（快速测试）**
   - 在Google Play商店搜索并安装"Kivy Launcher"
   - 将项目文件夹复制到Android设备的 `Kivy` 文件夹下
   - 打开Kivy Launcher，选择你的应用

2. **直接安装APK**
   - 将生成的APK文件复制到Android设备
   - 在设备上启用"未知来源"安装
   - 点击APK文件进行安装
   - 打开应用进行测试

## 九、调试技巧

1. **查看应用日志**
   ```powershell
   adb logcat -s python:D
   ```

2. **使用Buildozer调试模式**
   ```powershell
   buildozer android debug deploy run logcat
   ```

3. **检查Buildozer配置**
   ```powershell
   buildozer android doctor
   ```

## 十、进阶配置

### 1. 签名发布版本

1. **生成密钥库**
   ```powershell
   keytool -genkey -v -keystore futuresreview.keystore -alias futuresreview -keyalg RSA -keysize 2048 -validity 10000
   ```

2. **配置buildozer.spec**
   ```ini
   # (str) android.apk_key_path to use for signing the APK
   android.apk_key_path = futuresreview.keystore
   android.apk_key_alias = futuresreview
   ```

3. **构建发布版本**
   ```powershell
   buildozer android release
   ```

### 2. 添加自定义图标和启动画面

1. **准备图标和启动画面**
   - 图标：512x512 PNG格式
   - 启动画面：1920x1080 PNG格式

2. **配置buildozer.spec**
   ```ini
   # (str) Presplash of the application
   presplash.filename = %(source.dir)s/data/presplash.png
   
   # (str) Icon of the application
   icon.filename = %(source.dir)s/data/icon.png
   ```

## 十一、资源链接

- [Kivy官方文档](https://kivy.org/doc/stable/)
- [Buildozer官方文档](https://buildozer.readthedocs.io/)
- [Android开发者官网](https://developer.android.com/)
- [Kivy Launcher下载](https://play.google.com/store/apps/details?id=org.kivy.pygame)

## 十二、使用指南

1. **启动应用**
   - 安装APK后，在设备上找到"期货复盘"应用图标
   - 点击图标启动应用

2. **数据录入**
   - 在数据录入界面填写交易信息
   - 点击"保存数据"保存到本地数据库
   - 点击"数据分析"切换到分析界面

3. **数据分析**
   - 在数据分析界面选择品种
   - 查看总盈亏和胜率
   - 查看各品种的盈亏和胜率图表
   - 点击"返回数据录入"切换回录入界面

---

通过以上步骤，你应该能够在Windows系统下手动安装创建APK所需的所有软件，并成功构建出期货复盘应用的APK文件。如果遇到问题，请仔细检查配置和日志，或参考提供的资源链接寻求帮助。