from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Smart C Cleaner - 智能 C 盘清理工具")
    parser.add_argument(
        "--gui",
        action="store_true",
        help="启动图形界面（默认）",
    )
    parser.add_argument(
        "cli_args",
        nargs="*",
        help="命令行参数，例如: scan --deep / clean --deep -y",
    )

    args, unknown = parser.parse_known_args()
    cli_args = args.cli_args + unknown

    if cli_args and cli_args[0] in {"scan", "clean", "list"}:
        from cli import main as cli_main

        return cli_main(cli_args)

    if cli_args and not args.gui:
        from cli import main as cli_main

        return cli_main(cli_args)

    from gui import main as gui_main

    gui_main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
