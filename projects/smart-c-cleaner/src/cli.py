from __future__ import annotations

import argparse
import sys

from cleaner.categories import CleanTier, build_categories, categories_by_tier
from cleaner.clean_engine import clean_categories, deep_categories_need_confirm
from cleaner.scanner import scan_categories
from cleaner.utils import format_size, is_admin, relaunch_as_admin


def _selected_categories(args: argparse.Namespace):
    all_categories = build_categories()
    if args.only:
        wanted = set(args.only)
        return [item for item in all_categories if item.id in wanted]
    if args.deep:
        return all_categories
    return categories_by_tier(CleanTier.SAFE)


def _print_scan_results(results) -> int:
    total = 0
    print("\n扫描结果：")
    print("-" * 72)
    for result in results:
        tier = "深度" if result.category.tier == CleanTier.DEEP else "安全"
        if not result.accessible:
            size_text = "需管理员"
        elif result.category.special == "recycle_bin":
            size_text = "待清空"
        else:
            size_text = format_size(result.total_size)
            total += result.total_size
        print(
            f"[{tier}] {result.category.name:<18} "
            f"{size_text:>12}  ({result.file_count} 项)  {result.note}"
        )
    print("-" * 72)
    print(f"预计可释放（不含回收站）: {format_size(total)}\n")
    return total


def cmd_scan(args: argparse.Namespace) -> int:
    categories = _selected_categories(args)
    results = scan_categories(categories)
    _print_scan_results(results)
    return 0


def cmd_clean(args: argparse.Namespace) -> int:
    categories = _selected_categories(args)
    deep_items = deep_categories_need_confirm(categories)

    if deep_items and not args.yes:
        print("\n以下深度清理项将被执行，请确认：")
        for item in deep_items:
            print(f"  - {item.name}: {item.description}")
        answer = input("\n确认执行深度清理? 输入 yes 继续: ").strip().lower()
        if answer not in {"yes", "y"}:
            print("已取消。")
            return 1

    if any(item.requires_admin for item in categories) and not is_admin():
        print("部分项目需要管理员权限。")
        if args.admin:
            relaunch_as_admin()
        print("请使用 --admin 以管理员身份重新运行，或右键「以管理员身份运行」。")
        return 1

    scan_results = {item.category.id: item for item in scan_categories(categories)}
    _print_scan_results(scan_results.values())

    if not args.yes:
        answer = input("确认开始清理? 输入 yes 继续: ").strip().lower()
        if answer not in {"yes", "y"}:
            print("已取消。")
            return 1

    summary = clean_categories(categories, scan_results)
    print("\n清理完成：")
    print("-" * 72)
    for result in summary.results:
        status = "成功" if result.success else "失败"
        freed = format_size(result.freed_bytes) if result.freed_bytes else "-"
        print(f"[{status}] {result.category_name:<18} 释放: {freed:>10}  {result.message}")
    print("-" * 72)
    print(f"共释放空间: {format_size(summary.total_freed)}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    print("\n可用清理项：")
    for item in build_categories():
        tier = "深度" if item.tier == CleanTier.DEEP else "安全"
        admin = " [需管理员]" if item.requires_admin else ""
        print(f"  {item.id:<22} [{tier}]{admin} {item.name} - {item.description}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smart-c-cleaner",
        description="智能清理 C 盘 - 安全清理 + 可选深度清理",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    scan_parser = sub.add_parser("scan", help="扫描可清理空间")
    scan_parser.add_argument("--deep", action="store_true", help="包含深度清理项")
    scan_parser.add_argument("--only", nargs="+", help="仅扫描指定类别 ID")
    scan_parser.set_defaults(func=cmd_scan)

    clean_parser = sub.add_parser("clean", help="执行清理")
    clean_parser.add_argument("--deep", action="store_true", help="包含深度清理项")
    clean_parser.add_argument("--only", nargs="+", help="仅清理指定类别 ID")
    clean_parser.add_argument("-y", "--yes", action="store_true", help="跳过确认")
    clean_parser.add_argument("--admin", action="store_true", help="请求管理员权限")
    clean_parser.set_defaults(func=cmd_clean)

    list_parser = sub.add_parser("list", help="列出所有清理项")
    list_parser.set_defaults(func=cmd_list)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
