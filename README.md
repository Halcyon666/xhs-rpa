# XHS RPA

小红书 (Xiaohongshu) Automated Publishing System with AI Content Generation.

---

<p align="center">
  <b>Language / 语言</b><br>
  <a href="./README_EN.md">🇺🇸 English</a> | 
  <a href="./README_CN.md">🇨🇳 简体中文</a>
</p>

---

## ⚠️ Disclaimer

**This project is for educational and research purposes only. Commercial or illegal use is strictly prohibited. Users bear all consequences arising from the use of this project.**

## ⚠️ 免责声明

**本项目仅供学习研究使用，严禁用于任何商业或非法用途。使用本项目造成的任何后果由使用者自行承担。**

---

## Quick Start / 快速开始

Choose your preferred language to view the full documentation:

- **[English Documentation](./README_EN.md)** - For international users
- **[中文文档](./README_CN.md)** - 面向中文用户

## Repository Structure / 项目结构

```
xhs-rpa/
├── src/
│   ├── publisher.py          # Core publishing logic
│   └── server.py             # FastAPI service
├── config/
│   └── settings.yaml         # Configuration file
├── chrome-profile/           # Chrome user data (auto-created)
├── logs/                     # Debug logs & screenshots
├── launch-browser.bat        # Start Chrome in debug mode
├── run_api.bat              # Start API server (Method 1)
├── publish.py               # CLI tool (Method 2)
├── requirements.txt         # Python dependencies
├── README.md                # This file (Language selector)
├── README_EN.md             # English documentation
└── README_CN.md             # Chinese documentation
```

## Features / 功能特性

- 🚀 **API Service** - HTTP interface for system integration
- 🖥️ **Command Line Tool** - Direct terminal publishing
- 🌐 **Remote Control** - Connect to existing Chrome browser
- 📸 **Image Support** - Local files & URLs
- 🏷️ **Auto Tags** - Automatic tag appending
- 🧪 **Dry Run Mode** - Test without actual publishing

## License / 许可证

MIT License - See individual README files for details.

---

<p align="center">
  Made with ❤️ for automation enthusiasts
</p>
