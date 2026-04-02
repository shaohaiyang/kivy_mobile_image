# Kivy/Python Android 构建问题完整指南

本文档总结了常见的 Kivy/Android 构建问题及其解决方案，基于成功构建 "美化神器" 项目的经验。

## 📋 常见构建失败原因

### 1. Python 版本兼容性问题

**问题**：
```
Python 3.14.x 与 buildozer/python-for-android 不兼容
错误：远程调试模块、SDL2 bootstrap 问题、pyconfig.h 缺失
```

**解决方案**：
- ✅ 使用 Python 3.11 或 3.12（稳定版本）
- ❌ 避免 Python 3.13+（Kivy 生态系统未完全支持）

**GitHub Actions 配置**：
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # 或 '3.12'
```

---

### 2. Android 工具链版本冲突

**问题**：
```
手动指定过多版本导致冲突：
- android.api = 30 (buildozer.spec)
- 但 Actions 尝试安装 API 34 (workflow)
```

**解决方案**：
- ✅ 让 buildozer 使用默认/推荐配置
- ❌ 不要手动指定所有版本，除非有特殊需求

**buildozer.spec 配置**：
```ini
# ✅ 推荐：让 buildozer 自动选择
# android.api = 33
# android.minapi = 21
# android.build_tools_version = 33.0.0
# android.ndk = 25b

# ✅ 只在必要时手动指定
android.permissions = READ_MEDIA_IMAGES
android.private_storage = True
```

---

### 3. sdkmanager 路径找不到

**问题**：
```
错误：sdkmanager path ".../tools/bin/sdkmanager" does not exist
```

**原因**：
- 现代 Android SDK 使用 `cmdline-tools` 目录
- 但 buildozer 期望传统的 `tools` 目录结构

**解决方案**：

**方法 A：让 buildozer 自动处理（推荐）**
```bash
# 不手动安装 SDK，让 buildozer 下载和管理
yes | buildozer -v android debug
```

**方法 B.手动安装并创建符号链接**
```bash
# 下载 cmdline-tools
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip -d /tmp/cmdline-tools
mkdir -p ~/Android/sdk/cmdline-tools/latest
mv /tmp/cmdline-tools/cmdline-tools/* ~/Android/sdk/cmdline-tools/latest/

# 创建传统目录结构（buildozer 期望）
mkdir -p $ANDROID_HOME/tools/bin
ln -sf $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager $ANDROID_HOME/tools/bin/sdkmanager

# 设置环境变量
export ANDROID_HOME=~/Android/sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
```

---

### 4. NDK 下载失败

**问题**：
```
错误：ValueError: read of closed file
或：下载超时、版本不匹配
```

**解决方案**：
- ✅ 使用 python-for-android 推荐的 NDK 版本（当前：25b）
- ✅ 添加重试逻辑和更长的超时时间

**GitHub Actions 配置**：
```yaml
- name: Build APK
  run: |
    yes | buildozer -v android debug  # yes 自动接受许可，包括 NDK
  continue-on-error: false
  timeout-minutes: 180  # 首次构建 3 小时
```

---

### 5. 系统依赖不完整

**问题**：
```
编译错误：缺少头文件、链接失败
错误示例：sqlite3.h 找不到、gdbm 相关错误
```

**解决方案**：安装完整的依赖列表

**GitHub Actions 完整依赖列表**：
```yaml
- name: Install system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y \
      build-essential \
      git \
      ffmpeg \
      libsdl2-dev \
      libsdl2-image-dev \
      libsdl2-mixer-dev \
      libsdl2-ttf-dev \
      libportmidi-dev \
      libswscale-dev \
      libavformat-dev \
      libavcodec-dev \
      zlib1g-dev \
      libjpeg-dev \
      libpng-dev \
      libfreetype6-dev \
      libgstreamer1.0-dev \
      gstreamer1.0-plugins-base \
      gstreamer1.0-plugins-good \
      automake \
      autoconf \
      libtool \
      pkg-config \
      libncurses-dev \
      libncurses5-dev \
      libncursesw5-dev \
      libtinfo6 \
      cmake \
      libffi-dev \
      libssl-dev \
      libunwind-dev \
      libsqlite3-dev \
      sqlite3 \
      bzip2 \
      libbz2-dev \
      openssl \
      libgdbm-dev \
      libgdbm-compat-dev \
      liblzma-dev \
      libreadline-dev \
      uuid-dev \
      libgstreamer1.0 \
      zip \
      unzip \
      autoconf-archive \
      libltdl-dev \
      m4 \
      autopoint \
      gettext
```

---

### 6. Android 权限过时（Android 13+）

**问题**：
```
应用无法访问媒体文件
错误：Permission denied 或 storage 相关错误
```

**解决方案**：
- ✅ Android 13+ 使用新的精确权限模型
- ❌ 避免使用 `READ/WRITE_EXTERNAL_STORAGE`（已废弃）

**buildozer.spec 配置**：
```ini
# ✅ Android 13+ 推荐的精确权限
android.permissions = READ_MEDIA_IMAGES

# ✅ 明确启用私有存储
android.private_storage = True

# ❌ 避免（Android 13+ 已废弃）
# android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
```

---

### 7. 缺少缓存策略（构建缓慢）

**问题**：
```
每次构建都花费 20+ 分钟
日志：Downloading Android SDK... Downloading NDK...
```

**解决方案**：三级缓存策略

**GitHub Actions 缓存配置**：
```yaml
- name: Cache Buildozer global directory
  uses: actions/cache@v4
  with:
    path: ~/.buildozer
    key: ${{ runner.os }}-buildozer-global
    restore-keys: |
      ${{ runner.os }}-buildozer-global

- name: Cache Buildozer directory in app
  uses: actions/cache@v4
  with:
    path: .buildozer
    key: ${{ runner.os }}-buildozer-app
    restore-keys: |
      ${{ runner.os }}-buildozer-app

- name: Cache Android SDK
  uses: actions/cache@v4
  with:
    path: ~/.buildozer/android/platform/android-sdk
    key: ${{ runner.os }}-android-sdk
    restore-keys: |
      ${{ runner.os }}-android-sdk
```

**效果**：
- 首次构建：~20 分钟（下载 SDK/NDK）
- 后续构建：~5-8 分钟（使用缓存）

---

### 8. Cython 版本未固定

**问题**：
```
Cython 编译错误或不兼容行为
```

**解决方案**：固定 Cython 版本

**GitHub Actions 配置**：
```yaml
- name: Install Buildozer
  run: |
    pip install --upgrade pip
    pip install buildozer cython==3.0.11  # 固定版本
```

---

## 📝 完整的工作 GitHub Actions Workflow

这是一个经过验证的、完整的 GitHub Actions 配置，用于构建 Kivy Android 应用：

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04  # 使用固定版本，不使用 ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'  # 稳定版本

    - name: Set up JDK
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'

    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          build-essential git ffmpeg \
          libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
          libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev \
          zlib1g-dev libjpeg-dev libpng-dev libfreetype6-dev \
          libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
          automake autoconf libtool pkg-config \
          libncurses-dev libncurses5-dev libncursesw5-dev libtinfo6 \
          cmake libffi-dev libssl-dev libunwind-dev \
          libsqlite3-dev sqlite3 bzip2 libbz2-dev openssl \
          libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev uuid-dev \
          libgstreamer1.0 zip unzip autoconf-archive libltdl-dev m4 autopoint gettext

    # 三级缓存策略
    - name: Cache Buildozer global directory
      uses: actions/cache@v4
      with:
        path: ~/.buildozer
        key: ${{ runner.os }}-buildozer-global
        restore-keys: |
          ${{ runner.os }}-buildozer-global

    - name: Cache Buildozer directory in app
      uses: actions/cache@v4
      with:
        path: .buildozer
        key: ${{ runner.os }}-buildozer-app
        restore-keys: |
          ${{ runner.os }}-buildozer-app

    - name: Cache Android SDK
      uses: actions/cache@v4
      with:
        path: ~/.buildozer/android/platform/android-sdk
        key: ${{ runner.os }}-android-sdk
        restore-keys: |
          ${{ runner.os }}-android-sdk

    - name: Install Buildozer
      run: |
        pip install --upgrade pip
        pip install buildozer cython==3.0.11

    - name: Build APK
      run: |
        yes | buildozer -v android debug  # yes 自动接受所有提示
      continue-on-error: false
      timeout-minutes: 180

    - name: Upload APK artifact
      uses: actions/upload-artifact@v4
      with:
        name: android-apk
        path: |
          bin/*.apk
          bin/*.aab
        retention-days: 90
```

---

## 📄 推荐的 buildozer.spec 配置

```ini
[app]

title = Your App Title
package.name = yourapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 依赖
requirements = python3,kivy,pillow,plyer

# Android 配置
fullscreen = 0

# ✅ Android 13+ 推荐的精确权限
android.permissions = READ_MEDIA_IMAGES

# ✅ 明确启用私有存储
android.private_storage = True

# ✅ 双架构支持
android.archs = arm64-v8a,armeabi-v7a

# ✅ 让 buildozer 自动选择最佳版本
# android.api = 33
# android.minapi = 21
# android.build_tools_version = 33.0.0
# android.ndk = 25b

# 构建配置
log_level = 2
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
```

`