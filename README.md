# 图片一键美化 - 跨平台应用

一个使用 Kivy 和 Pillow 开发的简单跨平台图片美化应用，支持 macOS 和 Android。

## 功能特点

- **一键美化**：自动增强图片的对比度、亮度、色彩饱和度和锐度
- **平台适配**：
  - macOS: 标题显示"图片一键美化"
  - Android: 标题显示"美化神器"
- **简单易用**：选择图片 → 一键美化 → 保存图片

## 技术栈

- **Kivy** 2.3.0：跨平台 GUI 框架
- **Pillow** 10.0.0+：图像处理库
- **Plyer** 2.1.0：跨平台 API

## 本地开发 (macOS)

### 环境设置

1. 创建虚拟环境：
```bash
python3.12 -m venv venv
source venv/bin/activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
python main.py
```

## Android 打包

### GitHub Actions 自动打包

项目使用 GitHub Actions 自动构建 APK：

1. **推送到 GitHub**：
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/kivy_mobile_image.git
   git push -u origin main
   ```

2. **等待构建完成**（约 30-60 分钟）

3. **下载 APK**：
   - 进入 GitHub 仓库页面
   - 点击 "Actions" 标签
   - 选择最新的工作流运行
   - 在 "Artifacts" 部分下载 `android-apk`

### 本地手动打包（可选）

如果需要在本地打包 APK：

```bash
pip install buildozer
buildozer android debug
```

## 项目结构

```
kivy_mobile_image/
├── main.py                      # 应用主文件
├── requirements.txt             # Python 依赖
├── buildozer.spec              # Android 打包配置
├── .github/workflows/          # GitHub Actions 配置
│   └── build-android.yml
├── .gitignore                  # Git 忽略文件
└── README.md                   # 项目说明
```

## 图片增强算法

应用使用以下滤镜顺序进行图片增强：

1. **对比度增强**：1.2 倍
2. **亮度调整**：1.1 倍
3. **色彩增强**：1.15 倍
4. **锐化滤镜**：1.3 倍

## 使用说明

1. 点击"选择图片"按钮选择要美化的图片
2. 点击"一键美化"按钮应用增强效果
3. 点击"保存图片"按钮保存美化后的图片
4. macOS 保存到桌面，Android 保存到相册

## 许可证

MIT License