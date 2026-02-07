# XHS RPA

小红书 (Xiaohongshu) 自动化发布系统，集成 AI 内容生成。

## ⚠️ 免责声明

**本项目仅供学习研究使用，严禁用于任何商业或非法用途。使用本项目造成的任何后果由使用者自行承担，与项目作者无关。**

## 项目结构

```
xhs-rpa/
├── src/publisher.py     # 核心发布脚本
├── chrome-profile/      # 专用浏览器数据目录
├── 启动浏览器.bat       # 1. 先运行这个，登录账号
├── start.bat            # 2. 再运行这个，执行发布
└── requirements.txt     # Python 依赖
```

## 快速上手

1. **首次配置**
   - 运行 `python -m venv venv` 创建虚拟环境
   - 运行 `venv\Scripts\activate` 激活
   - 运行 `pip install -r requirements.txt` 安装依赖
   - 运行 `playwright install chromium` 安装浏览器核心

2. **日常使用**
   - **第一步**：双击 `启动浏览器.bat`
     - 在打开的 Chrome 窗口中，**手动登录**你的小红书账号。
     - **注意**：登录后不要关闭这个窗口！保持开启状态。
   - **第二步**：双击 `start.bat`
     - 脚本会自动连接浏览器，帮你发布内容。

## 常见问题

**Q: 为什么每次都要打开这个浏览器？**
A: 因为我们使用了一个独立的浏览器环境 (`chrome-profile`) 来隔离自动化操作，避免干扰你平时使用的浏览器，也更安全防封号。

**Q: 为什么第一次需要登录？**
A: 因为这个独立环境是全新的。只要你登录一次，数据就会自动保存在 `chrome-profile` 文件夹里，下次启动就不用再登录了（除非 Cookie 过期）。
