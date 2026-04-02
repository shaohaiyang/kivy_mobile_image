# 美化神器 - Image Enhancer

一个跨平台的图像增强应用，使用 Kivy 框架构建，支持 macOS 和 Android。

## ✨ 功能特性

- 🖼️ **一键美化**：自动调整图像的对比度、亮度、色彩和锐度
- 📱 **跨平台**：支持 macOS 和 Android
- 🎨 **多格式支持**：PNG、JPG、JPEG、BMP、GIF、WebP
- 🌏 **中文支持**：优化的中文字体渲染
- 💾 **智能保存**：自动转换 RGBA 到 RGB（JPEG 兼容）

## 🚀 快速开始

### macOS

1. **克隆仓库**
   ```bash
   git clone https://github.com/shaohaiyang/kivy_mobile_image.git
   cd kivy_mobile_image
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**
   ```bash
   python main.py
   ```

### Android

#### 方法 1：从 GitHub Actions 下载（推荐）

1. 访问 [Actions 页面](https://github.com/shaohaiyang/kivy_mobile_image/actions)
2. 找到最新的构建记录
3. 下载 `android-apk` 产物
4. 在 Android 设备上安装 APK

#### 方法 2：本地构建

```bash
# 安装 buildozer
pip install buildozer cython==3.0.11

# 构建 APK
yes | buildozer -v android debug

# APK 文件在 bin/ 目录中
```

## 📋 系统要求

- **Python**: 3.11 或 3.12
- **依赖**: Kivy 2.3.0+, Pillow 10.0.0+, Plyer 2.1.0+

## 🛠️ 技术栈

- **框架**: Kivy 2.3.0+
- **图像处理**: Pillow (PIL Fork)
- **平台适配**: Plyer
- **打包工具**: Buildozer
- **CI/CD**: GitHub Actions

## 📁 项目结构

```
kivy_mobile_image/
├── main.py                    # 主应用文件
├── buildozer.spec             # Android 构建配置
├── requirements.txt           # Python 依赖
├── README.md                  # 项目文档
├── IMPLEMENTATION_COMPLETE.md # 实现笔记
├── docs/
│   └── KIVY_ANDROID_BUILD_GUIDE.md  # Android 构建指南
├── assets/
│   └── default_placeholder.png      # 默认占位图
└── .github/
    └── workflows/
        └── build-android.yml        # GitHub Actions 工作流
```

## 🎨 图像增强算法

应用使用四级滤镜管道自动增强图像：

1. **对比度增强**: 1.2x
2. **亮度调整**: 1.1x
3. **色彩增强**: 1.15x
4. **锐度增强**: 1.3x

## 🔧 配置说明

### buildozer.spec 关键配置

```ini
# 应用信息
title = 美化神器
package.name = image_enhancer
package.domain = org.mydemo
version = 0.1

# 依赖
requirements = python3,kivy,pillow,plyer

# Android 权限（Android 13+ 兼容）
android.permissions = READ_MEDIA_IMAGES

# 私有存储
android.private_storage = True

# 支持的架构
android.archs = arm64-v8a,armeabi-v7a
```

## 📱 Android 构建指南

详细的 Android 构建故障排查和配置指南，请参考：
- [Kivy/Android 构建指南](docs/KIVY_ANDROID_BUILD_GUIDE.md)

## 🐛 故障排查

### 常见问题

1. **构建失败**：参考 [构建指南](docs/KIVY_ANDROID_BUILD_GUIDE.md)
2. **权限错误**：确保使用 Android 13+ 兼容的权限配置
3. **字体显示问题**：应用会自动选择合适的系统字体

### 调试

```bash
# 查看构建日志
buildozer -v android debug

# Android 设备日志
buildozer android logcat
```

## 📊 构建统计

- **首次构建**: ~20 分钟（下载 SDK/NDK）
- **后续构建**: ~5-8 分钟（使用缓存）
- **APK 大小**: ~38MB
- **支持架构**: arm64-v8a, armeabi-v7a

## 🔄 CI/CD

项目使用 GitHub Actions 自动构建 Android APK：

- **触发条件**: 推送到 main 分支
- **构建时间**: ~20 分钟（首次）
- **产物保留**: 90 天
- **缓存策略**: 三级缓存（buildozer、应用、SDK）

## 📝 开发日志

- [实现完成笔记](IMPLEMENTATION_COMPLETE.md)
- [Android 构建问题总结](docs/KIVY_ANDROID_BUILD_GUIDE.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证。

## 🙏 致谢

- [Kivy](https://kivy.org/) - 跨平台 Python GUI 框架
- [Buildozer](https://buildozer.readthedocs.io/) - Kivy 应用打包工具
- [Pillow](https://pillow.readthedocs.io/) - Python 图像处理库
- [Plyer](https://plyer.readthedocs.io/) - 跨平台 API 包装器

---

**项目地址**: https://github.com/shaohaiyang/kivy_mobile_image

**作者**: shaohaiyang

**最后更新**: 2026-04-03