"""
小红书轻量发布脚本 - 基于 Playwright MCP
连接已登录的 Chrome 浏览器，复用登录态发布内容
"""
import asyncio
import random
import sys
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright, Page, Browser, Playwright

# Windows 控制台编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class XHSPublisher:
    """小红书发布器 - 连接已登录浏览器"""
    
    def __init__(self, debug_port: int = 9222):
        self.debug_port = debug_port
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self._playwright: Optional[Playwright] = None
    
    async def connect(self) -> bool:
        """连接到已登录的 Chrome 浏览器"""
        try:
            self._playwright = await async_playwright().start()
            # 使用 IPv6 地址 [::1] 连接 Chrome
            # 优先尝试 IPv4，失败则尝试 IPv6
            try:
                self.browser = await self._playwright.chromium.connect_over_cdp(
                    f"http://127.0.0.1:{self.debug_port}"
                )
            except Exception:
                self.browser = await self._playwright.chromium.connect_over_cdp(
                    f"http://[::1]:{self.debug_port}"
                )
            context = self.browser.contexts[0]
            self.page = context.pages[0] if context.pages else await context.new_page()
            self.page.set_default_timeout(30000)
            print("[OK] 已连接到浏览器")
            return True
        except Exception as e:
            print(f"[FAIL] 连接失败: {e}")
            print(f"   请确保 Chrome 以调试模式启动:")
            print(f"   chrome --remote-debugging-port={self.debug_port}")
            return False
    
    async def check_login(self) -> bool:
        """检查是否已登录小红书"""
        if not self.page:
            return False
        try:
            print(f"[INFO] 正在检查登录状态...")
            # 如果不在发布页，则前往
            if "creator.xiaohongshu.com/publish/publish" not in self.page.url:
                await self.page.goto("https://creator.xiaohongshu.com/publish/publish")
            
            # 等待关键元素出现，而不是等待网络空闲
            try:
                # 尝试查找侧边栏头像或退出按钮，或者直接查找发布页的元素
                await self.page.wait_for_selector('.upload-input, input[type="file"]', timeout=10000)
                print("[OK] 已检测到登录状态")
                return True
            except:
                # 检查是否在登录页
                if "login" in self.page.url:
                    print("[FAIL] 未登录，请先在浏览器中手动登录小红书")
                    return False
                
                # 再次检查是否有登录后的特征
                content = await self.page.content()
                if "退出" in content or "发布笔记" in content:
                    print("[OK] 已通过内容特征检测到登录状态")
                    return True
            
            print("[FAIL] 无法确认登录状态")
            return False
        except Exception as e:
            print(f"[FAIL] 登录检查失败: {e}")
            await self._screenshot("login_check_fail.png")
            return False
    
    async def upload_images(self, image_paths: list[str]) -> bool:
        """上传图片"""
        if not self.page:
            return False
        try:
            # 确保切换到 "上传图文" 标签
            print("[INFO] 切换到图文发布模式...")
            
            # 尝试调整窗口大小，避免视口问题
            try:
                viewport = self.page.viewport_size
                if not viewport or viewport['width'] < 1000:
                    await self.page.set_viewport_size({"width": 1280, "height": 800})
            except:
                pass

            # 使用 JS 点击来绕过视口检测
            image_tab = self.page.get_by_text("上传图文").first
            if await image_tab.count() > 0:
                await image_tab.evaluate("element => element.click()")
                await asyncio.sleep(1)
            
            # 等待上传区域 (允许隐藏状态)
            await self.page.wait_for_selector('input[type="file"]', state="attached", timeout=10000)
            file_input = self.page.locator('input[type="file"]').first
            
            # 验证图片路径
            valid_paths = []
            for p in image_paths:
                path = Path(p)
                if path.exists():
                    valid_paths.append(str(path.absolute()))
                else:
                    print(f"[WARN] 图片不存在: {p}")
            
            if not valid_paths:
                print("[FAIL] 没有有效的图片")
                return False
            
            await file_input.set_input_files(valid_paths)
            print(f"[OK] 已上传 {len(valid_paths)} 张图片")
            
            # 等待图片处理完成 (可以等一些特定的预览图出现)
            await asyncio.sleep(3)
            return True
        except Exception as e:
            print(f"[FAIL] 图片上传失败: {e}")
            await self._screenshot("error_upload.png")
            return False
    
    async def fill_content(self, title: str, content: str) -> bool:
        """填写标题和正文"""
        if not self.page:
            return False
        try:
            # 等待页面跳转到编辑页
            await self.page.wait_for_selector('input[placeholder*="标题"]', timeout=15000)
            
            # 填写标题
            title_input = self.page.locator('input[placeholder*="标题"]')
            await title_input.fill(title[:20])  # 小红书标题限制20字
            print(f"[OK] 已填写标题: {title[:20]}")
            
            # 填写正文 - 使用多种选择器策略
            content_selectors = [
                '#post-textarea',
                'div[contenteditable="true"]',
                '[data-placeholder*="正文"]',
                '.ql-editor',
            ]
            
            editor = None
            for selector in content_selectors:
                try:
                    editor = self.page.locator(selector).first
                    if await editor.count() > 0:
                        break
                except:
                    continue
            
            if editor and await editor.count() > 0:
                await editor.click()
                await self.page.keyboard.type(content, delay=10)
                print("[OK] 已填写正文")
            else:
                print("[WARN] 未找到正文编辑器，尝试备用方法")
                await self.page.keyboard.press("Tab")
                await self.page.keyboard.type(content, delay=10)
            
            await asyncio.sleep(1)
            return True
        except Exception as e:
            print(f"[FAIL] 填写内容失败: {e}")
            await self._screenshot("error_content.png")
            return False
    
    async def publish(self, dry_run: bool = False) -> bool:
        """点击发布按钮"""
        if not self.page:
            return False
        try:
            # 多种发布按钮选择器
            publish_selectors = [
                'button:has-text("发布")',
                'button:has-text("发 布")',
                '.publishBtn',
                '[class*="publish"]',
            ]
            
            for selector in publish_selectors:
                try:
                    btn = self.page.locator(selector).first
                    if await btn.count() > 0 and await btn.is_visible():
                        if dry_run:
                            print("[INFO] Dry-run 模式，跳过发布")
                            return True
                        
                        await btn.click()
                        print("[OK] 已点击发布按钮")
                        
                        # 等待发布结果
                        await asyncio.sleep(3)
                        
                        # 检查是否成功
                        if "success" in self.page.url or "publish" not in self.page.url:
                            print("[DONE] 发布成功！")
                            return True
                        return True
                except:
                    continue
            
            print("[FAIL] 未找到发布按钮")
            await self._screenshot("error_publish.png")
            return False
        except Exception as e:
            print(f"[FAIL] 发布失败: {e}")
            await self._screenshot("error_publish.png")
            return False
    
    async def run(self, title: str, content: str, images: list[str], dry_run: bool = False) -> bool:
        """执行完整发布流程"""
        if not await self.connect():
            return False
        
        if not await self.check_login():
            return False
        
        steps = [
            ("上传图片", lambda: self.upload_images(images)),
            ("填写内容", lambda: self.fill_content(title, content)),
            ("发布", lambda: self.publish(dry_run)),
        ]
        
        for name, step in steps:
            print(f"\n[STEP] {name}...")
            if not await step():
                print(f"[FAIL] 流程中断于: {name}")
                return False
            await asyncio.sleep(random.uniform(0.5, 1.5))
        
        return True
    
    async def _screenshot(self, filename: str):
        """保存截图用于调试"""
        if not self.page:
            return
        try:
            path = Path("logs") / filename
            path.parent.mkdir(exist_ok=True)
            await self.page.screenshot(path=str(path))
            print(f"[SCREENSHOT] 截图已保存: {path}")
        except:
            pass
    
    async def disconnect(self):
        """断开浏览器连接"""
        # 注意：不要关闭 browser，因为我们只是连接到已有浏览器
        # 直接关闭 playwright 即可释放资源
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None


async def publish(title: str, content: str, images: list[str], dry_run: bool = False) -> bool:
    """便捷发布函数"""
    publisher = XHSPublisher()
    try:
        return await publisher.run(title, content, images, dry_run)
    finally:
        await publisher.disconnect()


# 命令行入口
if __name__ == "__main__":
    import sys
    
    # 示例用法
    asyncio.run(publish(
        title="测试标题",
        content="这是测试内容 #测试 #自动化",
        images=["test.jpg"],
        dry_run=True  # 设为 False 真正发布
    ))
