# XHS RPA

<p align="right">
  <b>🇺🇸 English</b> | 
  <a href="./README_CN.md">🇨🇳 简体中文</a>
</p>

Xiaohongshu (Little Red Book) Automated Publishing System with AI Content Generation.

## ⚠️ Disclaimer

**This project is for educational and research purposes only. Commercial or illegal use is strictly prohibited. Users bear all consequences arising from the use of this project.**

---

## Project Structure

```
xhs-rpa/
├── src/
│   ├── publisher.py          # Core publishing logic (browser automation)
│   └── server.py             # FastAPI service
├── config/
│   └── settings.yaml         # Configuration file
├── chrome-profile/           # Chrome user data directory (auto-created)
├── logs/                     # Error screenshots and debug logs
├── launch-browser.bat        # Start Chrome in debug mode
├── run_api.bat              # Start API server (Method 1)
├── publish.py               # CLI publishing tool (Method 2)
├── requirements.txt         # Python dependencies
├── README.md                # Language selector
├── README_EN.md             # This file (English)
└── README_CN.md             # Chinese documentation
```

### File Descriptions

| File | Purpose |
|------|---------|
| `src/publisher.py` | **Core Module**: Encapsulates all automation operations including browser connection, login check, image upload, content filling, and publish button clicking |
| `src/server.py` | **API Service**: FastAPI-based HTTP interface supporting remote publish calls |
| `launch-browser.bat` | **Launch Browser**: Automatically finds Chrome and starts it in debug mode with isolated user data directory |
| `run_api.bat` | **Start API**: One-click environment check, dependency installation, and API server startup (recommended for integration) |
| `publish.py` | **CLI Tool**: Execute publish commands directly in terminal with parameter support (suitable for scripting) |
| `config/settings.yaml` | **Configuration**: Optional settings for account and default tags |
| `chrome-profile/` | **Browser Data**: Stores login state and cookies to avoid re-login |
| `logs/` | **Debug Info**: Page screenshots when publishing fails, useful for troubleshooting |

---

## 🛠️ 1. Environment Setup (First Time)

Before use, ensure you have Python and Chrome browser installed.

### 1.1 Create and Activate Virtual Environment (Recommended)

To avoid polluting your global Python environment, using a virtual environment is strongly recommended.

**Windows:**
Open terminal (CMD or PowerShell) in the project root directory and run:

```bash
python -m venv venv
.\venv\Scripts\activate
```

*(You should see `(venv)` appear at the beginning of the command line when activated)*

**Mac / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 1.2 Install Dependencies

With the virtual environment activated, run the following commands to install required libraries:

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 🚀 2. Launch Browser (Critical Step)

This tool needs to connect to a Chrome browser running in **debug mode**. Please follow these steps carefully:

### Step 1: Completely Close Chrome

Ensure no Chrome processes are running in the taskbar or background.

*   **Windows**: Right-click Chrome icon in taskbar -> Close window. If necessary, open Task Manager to end all `chrome.exe` processes.
*   **Mac**: Right-click Chrome icon in Dock -> Quit.

### Step 2: Start Chrome in Debug Mode

**Easy Method (Recommended):**

Simply double-click **`launch-browser.bat`**

The script will automatically:
1. Find Chrome installation path from registry
2. Start Chrome in debug mode (port 9222)
3. Create isolated user data directory `chrome-profile/`

**Manual Method (Backup):**

If the script cannot find Chrome, you can manually run:

```cmd
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="E:\gemini-lifesync\xhs-rpa\chrome-profile"
```

### Step 3: Login to Xiaohongshu

After the browser starts:

1.  Enter `https://creator.xiaohongshu.com/` in the address bar
2.  **Complete login manually** (scan QR code or phone verification)
3.  Keep this browser window **open** after successful login

---

## ▶️ 3. Run Publishing Script

There are two ways to publish content:

### Method 1: API Service (Recommended for System Integration)

Suitable for scenarios requiring integration with other systems (such as CMS, content management platforms).

**Start Service:**

```bash
# Double-click or run in terminal
run_api.bat
```

The service will listen on `http://127.0.0.1:8000`

**Call API:**

```bash
curl -X POST http://127.0.0.1:8000/publish \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Title",
    "content": "This is the content #test",
    "images": ["test.jpg"],
    "tags": "#tag1 #tag2",
    "dry_run": true
  }'
```

Parameter Description:
- `title`: Title (optional, auto-extracted from first line of content if not provided)
- `content`: Content body (required)
- `images`: Array of image paths or URLs (required)
- `tags`: Tag string (optional, automatically appended to content end)
- `dry_run`: Test mode (`true` = fill only, don't publish; `false` = actual publish)

### Method 2: CLI Tool (Recommended for Manual Publishing)

Suitable for temporary publishing or batch script processing.

**Command Format:**

```bash
python publish.py -t "Title" -c "Content" -i "Image Path" [-d]
```

**Examples:**

```bash
# Test mode (doesn't actually publish)
python publish.py -t "Test Note" -c "This is content #tag" -i "test.jpg" -d

# Actual publish (remove -d)
python publish.py -t "Real Note" -c "Content here" -i "image1.jpg,image2.jpg"
```

Parameter Description:
- `-t, --title`: Title
- `-c, --content`: Content body
- `-i, --images`: Image paths, comma-separated for multiple
- `-d, --dry-run`: Test mode (optional)

---

## 🔌 4. Integration into Your Code

If you want to call the publish function in other Python scripts, you can reference it like this:

```python
import asyncio
from src.publisher import publish

async def main():
    # Use absolute paths or paths relative to execution directory
    images = [r"E:\photos\image1.jpg", r"E:\photos\image2.jpg"]
    
    success = await publish(
        title="Automated Publishing",
        content="This content is automatically published by script.\n\n#automation #python",
        images=images,
        dry_run=False  # Set to False for actual publishing
    )
    
    if success:
        print("✅ Publish successful")
    else:
        print("❌ Publish failed, check logs")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ❓ FAQ (Frequently Asked Questions)

### Q1: Script shows "Connection failed: BrowserType.connect_over_cdp: connect ECONNREFUSED ::1:9222"

**Cause**: Chrome is not started in debug mode, or the port number is incorrect.

**Solution**:
1. Completely close all Chrome windows.
2. Restart Chrome following [Step 2](#2-launch-browser-critical-step).
3. Ensure the startup command includes `--remote-debugging-port=9222`.

### Q2: Script shows "[FAIL] Not logged in"

**Cause**: Browser is not logged into Xiaohongshu, or login session has expired.

**Solution**: In the Chrome window with debug port enabled, manually refresh the Xiaohongshu creator center page to ensure logged-in status.

### Q3: Error "Element is outside of the viewport" or clicks not responding

**Cause**: Browser window too small, or page elements are obscured.

**Solution**: The script will automatically try to adjust window size. You can also manually enlarge the Chrome window and keep it in foreground.

### Q4: Image upload failed

**Cause**: Incorrect image path, or file is in use.

**Solution**: Check the `images` list in your code, preferably use **absolute paths** (e.g., `E:\data\img.jpg`) and ensure image files actually exist.

### Q5: Why open this browser every time?

**Cause**: We use an isolated browser environment (`chrome-profile`) to isolate automation operations, avoiding interference with your regular browser usage and providing better safety against account bans.

### Q6: Why need to login the first time?

**Cause**: Because this isolated environment is brand new. Once you log in, data is automatically saved in the `chrome-profile` folder, so you don't need to log in again next time (unless cookies expire).

---

## 🔧 Integration Workflow

### Python Code Call

```python
import asyncio
from src.publisher import publish

async def main():
    success = await publish(
        title="Automated Test",
        content="This content is called via code.\n\n#automation #python",
        images=["E:\\photos\\image1.jpg"],
        dry_run=False  # False for actual publish
    )
    
    if success:
        print("✅ Publish successful")
    else:
        print("❌ Publish failed")

if __name__ == "__main__":
    asyncio.run(main())
```

### Workflow Recommendations

1. **First Use**: Run `launch-browser.bat` → Login to Xiaohongshu → Keep browser open
2. **Daily Publishing**:
   - API Method: Start `run_api.bat` → Call HTTP API
   - Script Method: Directly run `python publish.py [parameters]`
3. **Batch Processing**: Use `publish.py` with loops or scheduled tasks

---

<p align="center">
  <a href="./README.md">⬆️ Back to Language Selection</a> | 
  <a href="./README_CN.md">🇨🇳 切换到中文</a>
</p>
