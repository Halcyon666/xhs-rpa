import os
import time
import shutil
import asyncio
import aiohttp
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# 确保 src 目录在 python path 中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入发布器类
from src.publisher import XHSPublisher

app = FastAPI(title="XHS RPA API")

# 全局锁，防止同时操作浏览器冲突
browser_lock = asyncio.Lock()

# 请求数据模型
class PublishRequest(BaseModel):
    title: Optional[str] = None
    content: str
    images: List[str]  # 支持 URL 或 本地路径
    tags: Optional[str] = None
    dry_run: bool = False

async def download_image(url: str, save_dir: Path) -> str:
    """下载网络图片到本地"""
    if not url.startswith("http"):
        # 如果是本地路径，检查是否存在
        if os.path.exists(url):
            return url
        # 也许是相对路径
        abs_path = os.path.abspath(url)
        if os.path.exists(abs_path):
            return abs_path
        print(f"[WARN] Local file not found: {url}")
        return url
    
    # 生成文件名
    filename = f"{int(time.time())}_{os.path.basename(url).split('?')[0]}"
    # 确保有扩展名
    if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
        filename += ".jpg"
        
    save_path = save_dir / filename
    
    print(f"[INFO] Downloading: {url} -> {save_path}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                if response.status != 200:
                    raise Exception(f"Download failed with status {response.status}")
                content = await response.read()
                with open(save_path, "wb") as f:
                    f.write(content)
        return str(save_path.absolute())
    except Exception as e:
        print(f"[ERROR] Failed to download image: {e}")
        raise

@app.post("/publish")
async def api_publish(req: PublishRequest):
    """
    发布接口
    """
    # 1. 自动提取标题（如果未提供）
    title = req.title
    if not title:
        # 取第一行，去掉特殊符号，截取前20字
        lines = req.content.strip().split('\n')
        # 过滤掉空行
        lines = [l for l in lines if l.strip()]
        if lines:
            # 移除常见的Markdown标记
            first_line = lines[0].replace("#", "").replace("*", "").strip()
            title = first_line[:20]
        else:
            title = "分享笔记"

    # 1.5 拼接 Tags 到内容末尾
    final_content = req.content
    if req.tags:
        final_content = f"{final_content.strip()}\n\n{req.tags.strip()}"

    # 2. 准备临时目录
    temp_dir = Path("temp_images")
    temp_dir.mkdir(exist_ok=True)
    
    local_image_paths = []
    
    # 3. 获取锁
    if browser_lock.locked():
        # 这里可以选择等待或者直接返回忙碌
        pass

    async with browser_lock:
        print(f"========== New Publish Request: {title} ==========")
        publisher = XHSPublisher()
        try:
            # 下载所有图片
            valid_images = []
            for url in req.images:
                try:
                    local_path = await download_image(url, temp_dir)
                    valid_images.append(local_path)
                except Exception as e:
                    print(f"[WARN] Skip image {url}: {e}")
            
            if not valid_images:
                raise HTTPException(status_code=400, detail="No valid images provided or download failed")

            print(f"[API] Starting publish task...")
            
            # 执行发布
            success = await publisher.run(
                title=title,
                content=final_content,
                images=valid_images,
                dry_run=req.dry_run
            )
            
            if success:
                print(f"[API] Publish Success!")
                return {"status": "success", "message": "Published successfully", "title": title}
            else:
                print(f"[API] Publish Failed!")
                raise HTTPException(status_code=500, detail="Publish failed internally (check logs)")
                
        except HTTPException:
            raise
        except Exception as e:
            print(f"[API] Unexpected Error: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
            
        finally:
            # 清理
            await publisher.disconnect()
            # 可选：清理临时文件
            # shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    import uvicorn
    print("启动 API 服务: http://0.0.0.0:8000")
    print("请确保已运行 '启动浏览器.bat' 并已登录小红书")
    uvicorn.run(app, host="0.0.0.0", port=8000)
