# XHS RPA

小红书 (Xiaohongshu) 自动化发布系统，集成 AI 内容生成。

## ⚠️ 免责声明

**本项目仅供学习研究使用，严禁用于任何商业或非法用途。使用本项目造成的任何后果由使用者自行承担，与项目作者无关。**

---

## 项目结构

```
xhs-rpa/
├── src/publisher.py     # 核心发布脚本
├── chrome-profile/      # 专用浏览器数据目录
├── logs/                # 错误日志和截图
├── 启动浏览器.bat       # 1. 先运行这个，登录账号
├── start.bat            # 2. 再运行这个，执行发布
└── requirements.txt     # Python 依赖
```

---

## 🛠️ 1. 环境准备 (首次使用)

在使用之前，请确保你的电脑上安装了 Python 和 Chrome 浏览器。

### 1.1 创建并激活虚拟环境 (推荐)

为了避免污染全局 Python 环境，强烈建议使用虚拟环境。

**Windows:**
在项目根目录下打开终端 (CMD 或 PowerShell)，运行：

```bash
python -m venv venv
.\venv\Scripts\activate
```

*(激活成功后，命令行前面会出现 `(venv)` 字样)*

**Mac / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 1.2 安装依赖库

在激活了虚拟环境的终端中，运行以下命令安装必要的库：

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 🚀 2. 启动浏览器 (关键步骤)

本工具需要连接到一个**开启了调试模式**的 Chrome 浏览器。请务必按照以下步骤操作：

### 第一步：彻底关闭 Chrome

请确保任务栏和后台没有运行任何 Chrome 进程。

*   **Windows**: 右键任务栏 Chrome 图标 -> 关闭窗口。如有必要，打开任务管理器结束所有 `chrome.exe` 进程。
*   **Mac**: 右键 Dock 栏 Chrome 图标 -> 退出。

### 第二步：以调试模式启动 Chrome

**Windows 用户:**

1.  按下 `Win + R` 键，打开"运行"窗口。
2.  输入 `cmd` 并回车，打开黑色的命令提示符窗口。
3.  复制并粘贴以下命令（包含 `--user-data-dir` 参数以避免冲突），然后回车：

```cmd
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="E:\gemini-lifesync\xhs-rpa\chrome-profile"
```

*(注意：请确保路径正确，或改为你电脑上存在的路径)*

**Mac 用户:**
在终端中运行：

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

### 第三步：登录小红书

浏览器启动后，会自动打开一个新窗口。

1.  在地址栏输入 `https://creator.xiaohongshu.com/`
2.  **手动完成登录**（扫码或手机号验证码）。
3.  登录成功后，保持这个浏览器窗口**不要关闭**。

---

## ▶️ 3. 运行发布脚本

### 3.1 快速测试 (Dry-run)

默认情况下，脚本处于演示模式 (`dry_run=True`)。它会帮你上传图片、填写标题和内容，但**不会**点击最后的发布按钮。

在项目根目录下运行：

```bash
.\venv\Scripts\activate
python src/publisher.py
```

或者直接双击运行目录下的 `start.bat` 文件。

如果看到终端输出 `[DONE] 发布成功！` (Dry-run模式下显示)，说明一切正常。

### 3.2 真正发布

确认测试没问题后，你可以通过修改代码来真正发布。

打开 `src/publisher.py`，找到文件末尾的 `if __name__ == "__main__":` 部分：

```python
    # 示例用法
    asyncio.run(publish(
        title="测试标题",
        content="这是测试内容 #测试 #自动化",
        images=["test.jpg"],
        dry_run=False  # <--- 将 True 改为 False 即可真正发布
    ))
```

---

## 🔌 4. 集成到你的代码

如果你想在其他 Python 脚本中调用发布功能，可以这样引用：

```python
import asyncio
from src.publisher import publish

async def main():
    # 图片请使用绝对路径，或者相对于运行目录的路径
    images = [r"E:\photos\image1.jpg", r"E:\photos\image2.jpg"]
    
    success = await publish(
        title="Python自动发布",
        content="这是通过脚本自动发布的内容。\n\n#自动化 #Python",
        images=images,
        dry_run=False # 设置为 False 以执行发布
    )
    
    if success:
        print("发布成功")
    else:
        print("发布失败，请检查日志")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ❓ 常见问题 (FAQ)

### Q1: 运行脚本提示 "连接失败: BrowserType.connect_over_cdp: connect ECONNREFUSED ::1:9222"

**原因**: Chrome 没有以调试模式启动，或者端口号不对。

**解决**: 
1. 彻底关闭所有 Chrome 窗口。
2. 按照 [第2步](#2-启动浏览器-关键步骤) 的命令重新启动 Chrome。
3. 确保启动命令中包含 `--remote-debugging-port=9222`。

### Q2: 脚本提示 "[FAIL] 未登录"

**原因**: 浏览器没有登录小红书，或者登录状态失效。

**解决**: 在那个开启了调试端口的 Chrome 窗口中，手动刷新一下小红书创作中心页面，确保是登录状态。

### Q3: 报错 "Element is outside of the viewport" 或点击没反应

**原因**: 浏览器窗口太小，或者页面元素被遮挡。

**解决**: 脚本会自动尝试调整窗口大小。你也可以手动把 Chrome 窗口拉大一点，保持前台显示。

### Q4: 图片上传失败

**原因**: 图片路径不对，或者文件被占用。

**解决**: 检查代码中的 `images` 列表，尽量使用**绝对路径** (例如 `E:\data\img.jpg`)，确保图片文件真实存在。

### Q5: 为什么每次都要打开这个浏览器？

**原因**: 因为我们使用了一个独立的浏览器环境 (`chrome-profile`) 来隔离自动化操作，避免干扰你平时使用的浏览器，也更安全防封号。

### Q6: 为什么第一次需要登录？

**原因**: 因为这个独立环境是全新的。只要你登录一次，数据就会自动保存在 `chrome-profile` 文件夹里，下次启动就不用再登录了（除非 Cookie 过期）。

---

## 📂 目录结构说明

*   `src/publisher.py`: 核心发布脚本。
*   `chrome-profile/`: Chrome 浏览器用户数据目录，保存登录状态。
*   `logs/`: 存放运行过程中的错误截图，方便调试。
*   `requirements.txt`: 项目依赖列表。
*   `start.bat`: Windows 下的一键启动脚本 (测试用)。
*   `启动浏览器.bat`: 启动 Chrome 调试模式的脚本。
