<div align="center">

[![English](https://img.shields.io/badge/LANG-🇬🇧%20English-lightgrey)](README.md)
[![Русский](https://img.shields.io/badge/LANG-🇷🇺%20Русский-lightgrey)](README_ru.md)
[![中文](https://img.shields.io/badge/LANG-🇨🇳%20中文-red)](README_zh.md)

</div>

# EDM Data Base // SECRET FILES
**一个完全离线、支持自托管的机密文件保险箱，拥有黑客风格 (Brutalist/Hacker) 的 UI。**
License: MIT

Python 3.8+

Flask

</div>
<div align="center">
</div>
## 🪐 关于项目
**EDM Data Base** 是一个轻量级、前端零依赖的机密文件服务器和保险箱。它允许你在本地（如通过 Termux 在 Android 设备上、树莓派或任何 PC）托管文件，并通过时尚且可定制的 Web UI 安全地访问它们。
所有的设置、账户和服务器操作都可以通过集成在你终端中的 **CLI 管理控制台** 来进行管理。
### ✨ 特性
 * **完全离线的前端:** 没有外部 CDN，没有 Google 字体或外部资产，一切都内置。
 * **集成的 CLI 控制台:** 直接从制作精美的终端 UI 启动服务器、管理账户和监控统计数据。
 * **自适应的 Web UI:** Brutalist/Hacker 设计风格，支持主题（明亮、黑暗、矩阵）、可自定义形状、颜色和触觉反馈。
 * **多媒体支持:** 浏览器内内置图片查看器、视频播放器和文本/代码编辑器。
 * **隐藏/取消隐藏保险箱:** 即刻在保险箱文件夹前添加一个点 (.)，以在系统文件管理器中隐藏它（通过 UI 或 CLI 控制）。
 * **移动端优先:** 非常适合在 Termux (Android) 上运行，并通过手机浏览器访问。
<div align="center">
</div>
## 🚀 入门指南 (安装)
### 先决条件
 * 系统已安装 **Python 3.8+**。
 * （可选）如果在 Android 上运行，需要 **Termux**。
### 1. 克隆仓库
打开你的终端并运行以下命令：
```bash
git clone [https://github.com/你的用户名/edm-database.git](https://github.com/你的用户名/edm-database.git)
cd edm-database

```
### 2. 安装依赖
安装所需的 Python 包（仅需要 Flask）：
```bash
pip install -r requirements.txt

```
*（如果你没有 requirements.txt，只需运行：pip install flask）*
### 3. 运行服务器 / 管理控制台
启动集成的管理控制台：
```bash
python server.py

```
在终端菜单中，你可以：
 1. 创建一个安全的保险箱路径。
 2. 设置你的登录 ID 和 KEY。
 3. 按 [ 1 ] 启动 Flask 服务器。
 4. 在你的浏览器中打开提供的本地 IP（例如：http://192.168.1.X:5000）。
## 🛠️ 使用方法
 * **上传:** 拖放文件，或者使用 + FILE / UPLOAD 按钮。
 * **上下文菜单:** 点击 ⋮ 图标或长按任何文件夹卡片，即可重命名、添加标签或删除文件。
 * **设置:** 访问设置面板可更改主题（黑暗/明亮/黑客）、切换自动保存或调整边框圆角。
## 🤝 参与贡献
欢迎提出建议、反馈问题和提交代码！
欢迎查看 issues 页面。
## 📝 许可证
本项目采用 MIT 许可证。
