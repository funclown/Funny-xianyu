"""
基础功能测试脚本
测试爬虫的基本导入和配置是否正常
"""
import sys


def test_imports():
    """测试模块导入"""
    print("="*60)
    print("测试 1: 模块导入")
    print("="*60)

    try:
        from src import config
        print("[OK] config.py 导入成功")

        from src import utils
        print("[OK] utils.py 导入成功")

        from src import parsers
        print("[OK] parsers.py 导入成功")

        from src import scraper
        print("[OK] scraper.py 导入成功")

        print("\n所有模块导入成功！\n")
        return True
    except Exception as e:
        print(f"\n[ERROR] 模块导入失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """测试配置"""
    print("="*60)
    print("测试 2: 配置检查")
    print("="*60)

    try:
        from src.config import (
            STATE_FILE,
            JSONL_OUTPUT_DIR,
            LOG_DIR,
            API_URL_PATTERN,
            DETAIL_API_URL_PATTERN,
            RUN_HEADLESS,
            LOGIN_IS_EDGE,
            DEBUG_MODE
        )

        print(f"STATE_FILE: {STATE_FILE}")
        print(f"JSONL_OUTPUT_DIR: {JSONL_OUTPUT_DIR}")
        print(f"LOG_DIR: {LOG_DIR}")
        print(f"API_URL_PATTERN: {API_URL_PATTERN}")
        print(f"DETAIL_API_URL_PATTERN: {DETAIL_API_URL_PATTERN}")
        print(f"RUN_HEADLESS: {RUN_HEADLESS}")
        print(f"LOGIN_IS_EDGE: {LOGIN_IS_EDGE}")
        print(f"DEBUG_MODE: {DEBUG_MODE}")

        print("\n配置加载成功！\n")
        return True
    except Exception as e:
        print(f"\n✗ 配置加载失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_utils():
    """测试工具函数"""
    print("="*60)
    print("测试 3: 工具函数")
    print("="*60)

    try:
        from src.utils import (
            get_link_unique_key,
            format_registration_days,
            log_time
        )

        # 测试 get_link_unique_key
        test_link = "https://www.goofish.com/item?id=123456&spm=xxx"
        unique_key = get_link_unique_key(test_link)
        assert unique_key == "https://www.goofish.com/item?id=123456"
        print(f"[OK] get_link_unique_key: {unique_key}")

        # 测试 format_registration_days
        days_365 = format_registration_days(365)
        print(f"[OK] format_registration_days(365天): {days_365}")

        days_100 = format_registration_days(100)
        print(f"[OK] format_registration_days(100天): {days_100}")

        # 测试 log_time
        log_time("测试日志输出")
        print("[OK] log_time 函数正常")

        print("\n工具函数测试通过！\n")
        return True
    except Exception as e:
        print(f"\n[ERROR] 工具函数测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_check_login_state():
    """检查登录状态文件"""
    print("="*60)
    print("测试 4: 登录状态文件检查")
    print("="*60)

    import os
    from src.config import STATE_FILE

    if os.path.exists(STATE_FILE):
        print(f"[OK] 登录状态文件存在: {STATE_FILE}")
        import json
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[OK] 登录状态文件格式正确")
            print(f"\n提示: 登录状态文件已就绪，可以开始爬取")
            return True
        except Exception as e:
            print(f"[WARN] 登录状态文件可能损坏: {e}")
            print("  提示: 请重新生成登录状态文件")
            return False
    else:
        print(f"[INFO] 登录状态文件不存在: {STATE_FILE}")
        print("  提示: 登录状态文件是可选的，但建议准备以获得更完整的数据")
        print("  参考 README.md 了解如何准备登录状态文件")
        # 登录状态文件不是必需的，所以返回 True
        return True


def test_check_playwright():
    """检查 Playwright 是否安装"""
    print("="*60)
    print("测试 5: Playwright 安装检查")
    print("="*60)

    try:
        from playwright.sync_api import sync_playwright
        print("[OK] Playwright Python 包已安装")
        print("[OK] Playwright 模块加载完整")
        print("\n提示: 如果尚未安装浏览器，请运行:")
        print("  playwright install chromium")
        return True
    except ImportError:
        print("[ERROR] Playwright 未安装")
        print("  提示: 运行 'pip install playwright'")
        return False


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("闲鱼爬虫 - 基础功能测试")
    print("="*60 + "\n")

    results = []

    # 运行测试
    results.append(("模块导入", test_imports()))
    results.append(("配置检查", test_config()))
    results.append(("工具函数", test_utils()))
    results.append(("登录状态", test_check_login_state()))
    results.append(("Playwright", test_check_playwright()))

    # 输出测试结果
    print("="*60)
    print("测试结果汇总")
    print("="*60)

    for name, passed in results:
        status = "[OK] 通过" if passed else "[FAIL] 失败"
        print(f"{name}: {status}")

    all_passed = all(r[1] for r in results)

    print("="*60)
    if all_passed:
        print("[OK] 所有测试通过！项目已准备就绪。")
    else:
        print("[WARN] 部分测试未通过，请根据提示进行修复。")
    print("="*60)

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
