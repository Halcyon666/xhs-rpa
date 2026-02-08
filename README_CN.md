# XHS RPA

<p align="right">
  <a href="./README_EN.md">🇺🇸 English</a> | 
  <b>🇨🇳 简体中文</b>
</p>

小红书 (Xiaohongshu) 自动化发布系统，集成 AI 内容生成。

## ⚠️ 免责声明

**本项目仅供学习研究使用，严禁用于任何商业或非法用途。使用本项目造成的任何后果由使用者自行承担，与项目作者无关。**

---

## 项目结构

```
xhs-rpa/
├── src/
│   ├── publisher.py     # 核心发布逻辑（浏览器操作）
│   └── server.py        # FastAPI 接口服务
├── config/
│   └── settings.yaml    # 配置文件
├── chrome-profile/      # Chrome 浏览器数据目录（自动创建）
├── logs/                # 错误截图和调试日志
├── launch-browser.bat   # 启动 Chrome 调试模式
├── run_api.bat          # 启动 API 服务（方式一）
├── publish.py           # 命令行发布工具（方式二）
├── requirements.txt     # Python 依赖列表
└── README.md            # 项目说明文档
```

### 文件说明

| 文件 | 作用 |
|------|------|
| `src/publisher.py` | **核心模块**：封装了浏览器连接、登录检查、图片上传、内容填写、发布按钮点击等所有自动化操作 |
| `src/server.py` | **API 服务**：基于 FastAPI 提供 HTTP 接口，支持远程调用发布功能 |
| `launch-browser.bat` | **启动浏览器**：自动查找 Chrome 并以调试模式启动，创建独立的用户数据目录 |
| `run_api.bat` | **启动 API**：一键检查环境、安装依赖、启动 API 服务（推荐用于集成） |
| `publish.py` | **命令行工具**：直接在终端执行发布命令，支持参数传入（适合脚本调用） |
| `config/settings.yaml` | **配置项**：可配置小红书账号、默认标签等（可选） |
| `chrome-profile/` | **浏览器数据**：保存登录状态、Cookie，避免每次重新登录 |
| `logs/` | **调试信息**：发布失败时的页面截图，用于排查问题 |

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

本工具需要连接到一个**开启了调试模式**的 Chrome 浏览器。

### 第一步：彻底关闭 Chrome

请确保任务栏和后台没有运行任何 Chrome 进程。

*   **Windows**: 右键任务栏 Chrome 图标 -> 关闭窗口。如有必要，打开任务管理器结束所有 `chrome.exe` 进程。
*   **Mac**: 右键 Dock 栏 Chrome 图标 -> 退出。

### 第二步：以调试模式启动 Chrome

**简单方法（推荐）：**

直接双击运行 **`launch-browser.bat`**

脚本会自动：
1. 从注册表查找 Chrome 安装路径
2. 以调试模式启动 Chrome（端口 9222）
3. 创建独立的用户数据目录 `chrome-profile/`

**手动方法（备用）：**

如果脚本无法找到 Chrome，可以手动运行：

```cmd
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="E:\gemini-lifesync\xhs-rpa\chrome-profile"
```

### 第三步：登录小红书

浏览器启动后：

1.  在地址栏输入 `https://creator.xiaohongshu.com/`
2.  **手动完成登录**（扫码或手机号验证码）
3.  登录成功后，保持这个浏览器窗口**不要关闭**

---

## ▶️ 3. 运行发布脚本

有两种方式可以发布内容：

### 方式一：API 服务（推荐用于系统集成）

适合需要与其他系统（如 CMS、内容管理平台）对接的场景。

**启动服务：**

```bash
# 双击运行或在终端执行
run_api.bat
```

服务启动后会监听 `http://127.0.0.1:8000`

**调用接口：**

```bash
curl -X POST http://127.0.0.1:8000/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试标题",
    "content": "这是正文内容 #测试",
    "images": ["test.jpg"],
    "tags": "#标签1 #标签2",
    "dry_run": true
  }'
```

参数说明：
- `title`: 标题（可选，不填则自动提取正文第一行）
- `content`: 正文内容（必填）
- `images`: 图片路径或 URL 数组（必填）
- `tags`: 标签字符串（可选，会自动添加到正文末尾）
- `dry_run`: 测试模式（`true` 只填写不发布，`false` 真正发布）

### 方式二：命令行工具（推荐用于手动发布）

适合临时发布或脚本批量处理。

**命令格式：**

```bash
python publish.py -t "标题" -c "正文内容" -i "图片路径" [-d]
```

**示例：**

```bash
# 测试模式（不真正发布）
python publish.py -t "测试笔记" -c "这是正文 #标签" -i "test.jpg" -d

# 正式发布（去掉 -d）
python publish.py -t "正式笔记" -c "正文内容" -i "image1.jpg,image2.jpg"
```

参数说明：
- `-t, --title`: 标题
- `-c, --content`: 正文内容
- `-i, --images`: 图片路径，多个用逗号分隔
- `-d, --dry-run`: 测试模式（可选）

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

## 🔧 集成到您的系统

### Python 代码调用

```python
import asyncio
from src.publisher import publish

async def main():
    success = await publish(
        title="自动发布测试",
        content="这是通过代码调用的内容。\n\n#自动化 #Python",
        images=["E:\\photos\\image1.jpg"],
        dry_run=False  # False 为正式发布
    )
    
    if success:
        print("✅ 发布成功")
    else:
        print("❌ 发布失败")

if __name__ == "__main__":
    asyncio.run(main())
```

### 工作流建议

1. **首次使用**：运行 `launch-browser.bat` → 登录小红书 → 保持浏览器开启
2. **日常发布**：
   - API 方式：启动 `run_api.bat` → 调用 HTTP 接口
   - 脚本方式：直接运行 `python publish.py [参数]`
3. **批量处理**：使用 `publish.py` 配合循环或定时任务

---

<p align="center">
  <a href="./README.md">⬆️ 返回语言选择</a> | 
  <a href="./README_EN.md">🇺🇸 Switch to English</a>
</p>
