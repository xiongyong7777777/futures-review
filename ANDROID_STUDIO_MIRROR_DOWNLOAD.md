# Android Studio 国内镜像下载指南

由于官方网站 `https://developer.android.com/studio` 无法访问，以下提供几个可靠的国内镜像下载渠道及详细安装步骤。

## 一、可靠的国内镜像源

### 1. 清华大学开源软件镜像站
- **特点**：稳定可靠，更新及时，学术机构提供
- **Android Studio下载页面**：https://mirrors.tuna.tsinghua.edu.cn/android-studio/
- **SDK镜像配置**：在Android Studio中可直接使用清华镜像作为SDK更新源

### 2. 中国科学技术大学开源软件镜像站
- **特点**：速度快，涵盖资源广泛
- **Android Studio下载页面**：https://mirrors.ustc.edu.cn/android-studio/

### 3. 阿里云开发者社区
- **特点**：企业级服务，稳定可靠
- **SDK下载中心**：https://developer.aliyun.com/sdk/download/android-studio

### 4. 华为开发者联盟
- **特点**：国内大厂提供，资源丰富
- **Android Studio下载**：https://developer.huawei.com/consumer/cn/doc/development/Tools-Guides/install-android-studio-0000001051059322

## 二、下载步骤（以清华大学镜像站为例）

1. **访问镜像站**
   - 打开浏览器，访问：https://mirrors.tuna.tsinghua.edu.cn/android-studio/

2. **选择适合的版本**
   - 选择最新的稳定版本（推荐）
   - 对于Windows系统，下载 `.exe` 格式的安装包
   - 对于64位Windows系统，选择带有 `windows` 标识的安装包
   - 例如：`android-studio-2023.1.1.27-windows.exe`

3. **开始下载**
   - 点击下载链接，选择保存位置
   - 等待下载完成（根据网络情况，可能需要几分钟到几十分钟）

## 三、安装步骤

1. **运行安装程序**
   - 找到下载好的 `.exe` 文件，双击运行
   - 点击"Next"继续

2. **选择安装类型**
   - 推荐选择"Standard"（标准安装），适合大多数用户
   - 高级用户可以选择"Custom"（自定义安装），修改安装路径和组件
   - 点击"Next"继续

3. **选择安装位置**
   - 默认安装路径：`C:\Program Files\Android\Android Studio`
   - 可以修改为其他磁盘，但建议使用默认路径
   - 点击"Next"继续

4. **选择开始菜单文件夹**
   - 保持默认即可
   - 点击"Install"开始安装

5. **等待安装完成**
   - 安装过程可能需要几分钟
   - 安装完成后，点击"Next"，然后点击"Finish"

## 四、首次启动配置

1. **启动Android Studio**
   - 从开始菜单或桌面快捷方式启动Android Studio

2. **导入配置**
   - 首次启动会提示是否导入之前的配置，选择"Do not import settings"
   - 点击"OK"继续

3. **选择UI主题**
   - 选择适合自己的主题（Light或Darcula）
   - 点击"Next"继续

4. **SDK Components Setup**
   - Android Studio会自动检测并提示需要安装的SDK组件
   - 确保勾选以下组件：
     - Android SDK
     - Android SDK Platform
     - Android Virtual Device
     - Android SDK Build-Tools
     - NDK (Side by Side)
   - 点击"Next"继续

5. **选择SDK安装位置**
   - 默认路径：`C:\Users\<用户名>\AppData\Local\Android\Sdk`
   - 可以修改，但建议使用默认路径
   - 点击"Next"继续

6. **模拟器设置**
   - 保持默认设置即可
   - 点击"Finish"开始下载和安装SDK组件

7. **等待SDK组件安装完成**
   - 这个过程可能需要较长时间（根据网络情况和选择的组件多少）
   - 安装完成后，点击"Finish"

## 五、配置国内镜像源（提高SDK更新速度）

1. **打开SDK Manager**
   - 在Android Studio中，点击顶部工具栏的SDK Manager图标（或依次点击"File" > "Settings" > "Appearance & Behavior" > "System Settings" > "Android SDK"）

2. **选择SDK Update Sites**
   - 切换到"SDK Update Sites"选项卡
   - 点击"+"按钮添加新的镜像源

3. **添加清华镜像源**
   - 点击"+"按钮，添加以下URL：
     ```
     https://mirrors.tuna.tsinghua.edu.cn/android/repository/
     ```
   - 勾选刚添加的镜像源
   - 取消勾选"Google Repository"和"Android Repository"（可选，避免连接Google服务器）
   - 点击"OK"保存设置

4. **更新SDK**
   - 切换到"SDK Platforms"选项卡
   - 勾选需要的Android版本（至少包括API级别31和21，与buildozer.spec配置匹配）
   - 切换到"SDK Tools"选项卡
   - 勾选NDK (Side by Side) 和 CMake
   - 点击"Apply"开始更新

## 六、验证安装

1. **检查Android Studio版本**
   - 依次点击"Help" > "About"，查看Android Studio版本信息

2. **检查SDK路径**
   - 依次点击"File" > "Settings" > "Appearance & Behavior" > "System Settings" > "Android SDK"
   - 记录SDK Location，后续配置buildozer.spec需要用到

3. **检查NDK路径**
   - 在SDK Manager的"SDK Tools"选项卡中，找到NDK (Side by Side)，查看安装的版本
   - NDK通常安装在：`C:\Users\<用户名>\AppData\Local\Android\Sdk\ndk\<版本号>`

## 七、常见问题及解决方案

### 1. 安装过程中提示"无法访问远程服务器"
**解决方案**：
- 检查网络连接
- 暂时关闭防火墙和杀毒软件
- 确保使用了国内镜像源

### 2. SDK组件下载失败
**解决方案**：
- 确认已正确配置国内镜像源
- 尝试更换不同的镜像源
- 手动下载SDK组件并解压到SDK目录

### 3. Android Studio启动缓慢
**解决方案**：
- 关闭不必要的插件
- 增加JVM堆内存：在Android Studio安装目录下的`bin`文件夹中，编辑`studio64.exe.vmoptions`文件，增加`-Xmx4g`参数

### 4. NDK版本不匹配
**解决方案**：
- 在SDK Manager中安装与buildozer.spec配置匹配的NDK版本（推荐25.1.8937393）
- 在buildozer.spec中明确指定NDK路径

## 八、后续步骤

安装完成Android Studio后，继续按照《Windows系统手动创建APK指南》中的步骤：
1. 配置环境变量（ANDROID_SDK_ROOT和ANDROID_NDK_ROOT）
2. 修改buildozer.spec文件，设置正确的SDK和NDK路径
3. 开始构建APK

## 九、资源链接

- [清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/)
- [中国科学技术大学开源软件镜像站](https://mirrors.ustc.edu.cn/)
- [Android Studio官方文档（中文）](https://developer.android.google.cn/studio/intro)
- [Android开发者官网（中文）](https://developer.android.google.cn/)

通过以上步骤，您应该能够成功下载并安装Android Studio，并配置好国内镜像源，为后续构建APK做好准备。