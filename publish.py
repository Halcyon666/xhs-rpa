import asyncio
import sys
import argparse
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))
from publisher import publish


async def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='小红书自动发布脚本')
    parser.add_argument('--title', '-t', required=True, help='帖子标题')
    parser.add_argument('--content', '-c', required=True, help='帖子正文内容')
    parser.add_argument('--images', '-i', required=True, help='图片路径，多个用逗号分隔')
    parser.add_argument('--dry-run', '-d', action='store_true', help='测试模式（不真正发布）')
    
    args = parser.parse_args()
    
    # 解析图片路径
    image_list = [p.strip() for p in args.images.split(',')]
    
    print(f"\n{'='*50}")
    print(f"标题: {args.title}")
    print(f"内容: {args.content[:50]}...")
    print(f"图片: {image_list}")
    print(f"模式: {'测试' if args.dry_run else '正式发布'}")
    print(f"{'='*50}\n")
    
    # 执行发布
    success = await publish(
        title=args.title,
        content=args.content,
        images=image_list,
        dry_run=args.dry_run
    )
    
    print(f"\n{'='*50}")
    print("✅ 发布成功！" if success else "❌ 发布失败！")
    print(f"{'='*50}")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
