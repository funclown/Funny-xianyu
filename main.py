"""
闲鱼爬虫主程序
支持两种运行模式：
1. 交互式模式（直接运行）
2. 命令行参数模式（从Web界面调用）
"""
import asyncio
import sys
import json
import argparse
from src.scraper import scrape_xianyu
from src.utils import log_time
from src.config import TASKS_FILE, get_notification_config


def print_banner():
    """打印程序横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              闲鱼爬虫 - 简化版 v1.0                       ║
║                                                           ║
║              专注于数据爬取，不包含AI分析                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def load_task_by_id(task_id):
    """根据任务ID加载任务配置"""
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)

        for task in tasks:
            if task['id'] == task_id:
                return task

        print(f"错误: 未找到任务ID为 {task_id} 的任务")
        return None
    except Exception as e:
        print(f"错误: 加载任务文件失败 - {e}")
        return None


async def run_task_interactive():
    """交互式运行模式"""
    print_banner()

    # ==================== 获取用户输入 ====================
    print("\n请输入爬取参数：\n")

    keyword = input("1. 搜索关键词: ").strip()
    if not keyword:
        print("错误: 搜索关键词不能为空！")
        return

    max_pages_input = input("2. 爬取页数 (默认1): ").strip()
    max_pages = int(max_pages_input) if max_pages_input.isdigit() else 1

    personal_only_input = input("3. 是否只看个人闲置？(y/n，默认n): ").strip().lower()
    personal_only = personal_only_input == 'y'

    min_price = None
    max_price = None
    price_filter_input = input("4. 是否设置价格筛选？(y/n，默认n): ").strip().lower()
    if price_filter_input == 'y':
        min_price = input("   最低价格 (留空则不限制): ").strip() or None
        max_price = input("   最高价格 (留空则不限制): ").strip() or None

    debug_limit_input = input("5. 调试模式限制数量 (0=不限制，默认0): ").strip()
    debug_limit = int(debug_limit_input) if debug_limit_input.isdigit() else 0

    # ==================== 确认配置 ====================
    print("\n" + "="*60)
    print("爬取配置汇总：")
    print(f"  搜索关键词: {keyword}")
    print(f"  爬取页数: {max_pages}")
    print(f"  只看个人闲置: {'是' if personal_only else '否'}")
    if min_price or max_price:
        print(f"  价格范围: {min_price or '不限'} - {max_price or '不限'}")
    else:
        print(f"  价格范围: 不限")
    print(f"  调试限制: {'不限制' if debug_limit == 0 else debug_limit}")
    print("="*60)

    confirm = input("\n确认开始爬取？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消爬取。")
        return

    # ==================== 开始爬取 ====================
    await execute_scrape(keyword, max_pages, personal_only, min_price, max_price, debug_limit)


async def run_task_with_args(args):
    """使用命令行参数运行模式"""
    task_config = None

    # 如果指定了task-id，从文件加载任务配置
    if args.task_id:
        task_config = load_task_by_id(args.task_id)
        if not task_config:
            return
        keyword = task_config['keyword']
        max_pages = task_config.get('max_pages', 1)
        personal_only = task_config.get('personal_only', False)
        min_price = task_config.get('min_price')
        max_price = task_config.get('max_price')
        task_name = task_config.get('task_name', 'Unnamed Task')

        # 获取通知配置
        notify_config = get_notification_config()
    else:
        # 使用命令行参数
        if not args.keyword:
            print("错误: 必须指定 --keyword 或 --task-id")
            return
        keyword = args.keyword
        max_pages = args.pages
        personal_only = args.personal_only
        min_price = args.min_price
        max_price = args.max_price
        task_name = args.task_name or f"Task_{keyword}"

        # 获取通知配置
        notify_config = get_notification_config()

    # 打印任务信息
    print("\n" + "="*60)
    print(f"开始执行任务: {task_name if args.task_id else keyword}")
    print("="*60)
    print(f"  搜索关键词: {keyword}")
    print(f"  爬取页数: {max_pages}")
    print(f"  只看个人闲置: {'是' if personal_only else '否'}")
    if min_price or max_price:
        print(f"  价格范围: {min_price or '不限'} - {max_price or '不限'}")

    print("="*60 + "\n")

    # 执行爬取
    await execute_scrape(keyword, max_pages, personal_only, min_price, max_price, args.debug, notify_config)


async def execute_scrape(keyword, max_pages, personal_only, min_price, max_price, debug_limit, notify_config=None):
    """执行爬取任务的核心函数"""
    log_time("开始爬取任务...")

    try:
        processed_count = await scrape_xianyu(
            keyword=keyword,
            max_pages=max_pages,
            personal_only=personal_only,
            min_price=min_price,
            max_price=max_price,
            debug_limit=debug_limit,
            notify_config=notify_config
        )

        log_time(f"爬取任务完成！共处理 {processed_count} 个新商品。")
        print(f"\n数据已保存到: jsonl/{keyword}_full_data.jsonl")
        return processed_count

    except Exception as e:
        log_time(f"爬取过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 0


async def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='闲鱼爬虫程序')
    parser.add_argument('--task-id', type=str, help='从tasks.json加载指定ID的任务')
    parser.add_argument('--keyword', type=str, help='搜索关键词')
    parser.add_argument('--pages', type=int, default=1, help='爬取页数')
    parser.add_argument('--personal-only', action='store_true', help='只看个人闲置')
    parser.add_argument('--min-price', type=str, help='最低价格')
    parser.add_argument('--max-price', type=str, help='最高价格')
    parser.add_argument('--debug', type=int, default=0, help='调试模式限制数量')
    parser.add_argument('--task-name', type=str, help='任务名称')

    # 尝试解析参数
    try:
        args = parser.parse_args()
    except:
        # 如果解析失败，使用交互式模式
        args = None

    # 判断使用哪种模式
    if args and (args.task_id or args.keyword):
        # 命令行参数模式
        await run_task_with_args(args)
    elif len(sys.argv) == 1:
        # 没有参数，使用交互式模式
        await run_task_interactive()
    else:
        # 参数不完整
        parser.print_help()
        print("\n提示: 直接运行 'python main.py' 进入交互式模式")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n用户中断程序，正在退出...")
        sys.exit(0)
