from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

from cleaner.utils import expand_path, get_system_drive


class CleanTier(str, Enum):
    SAFE = "safe"
    DEEP = "deep"


@dataclass
class CleanCategory:
    id: str
    name: str
    description: str
    tier: CleanTier
    paths: list[Path] = field(default_factory=list)
    glob_patterns: list[str] = field(default_factory=list)
    requires_admin: bool = False
    default_selected: bool = False
    special: str | None = None
    min_age_days: int | None = None
    min_size_mb: int | None = None


def _user_profile() -> Path:
    return expand_path("%USERPROFILE%")


def _local_appdata() -> Path:
    return expand_path("%LOCALAPPDATA%")


def _program_data() -> Path:
    return expand_path("%PROGRAMDATA%")


def _system_root() -> Path:
    return expand_path("%SystemRoot%")


def build_categories() -> list[CleanCategory]:
    system = get_system_drive()
    user = _user_profile()
    local = _local_appdata()
    program_data = _program_data()
    win = _system_root()

    return [
        CleanCategory(
            id="user_temp",
            name="用户临时文件",
            description="当前用户的 TEMP 与 LocalAppData\\Temp 目录",
            tier=CleanTier.SAFE,
            paths=[
                expand_path("%TEMP%"),
                local / "Temp",
            ],
            default_selected=True,
        ),
        CleanCategory(
            id="windows_temp",
            name="Windows 临时文件",
            description="C:\\Windows\\Temp 系统临时目录",
            tier=CleanTier.SAFE,
            paths=[win / "Temp"],
            requires_admin=True,
            default_selected=True,
        ),
        CleanCategory(
            id="recycle_bin",
            name="回收站",
            description="清空所有驱动器的回收站",
            tier=CleanTier.SAFE,
            special="recycle_bin",
            default_selected=True,
        ),
        CleanCategory(
            id="thumbnail_cache",
            name="缩略图缓存",
            description="Explorer 缩略图与图标缓存",
            tier=CleanTier.SAFE,
            paths=[local / "Microsoft" / "Windows" / "Explorer"],
            glob_patterns=["thumbcache_*.db", "iconcache_*.db"],
            default_selected=True,
        ),
        CleanCategory(
            id="directx_cache",
            name="DirectX 着色器缓存",
            description="D3D 着色器编译缓存",
            tier=CleanTier.SAFE,
            paths=[local / "D3DSCache"],
            default_selected=True,
        ),
        CleanCategory(
            id="edge_cache",
            name="Microsoft Edge 缓存",
            description="Edge 浏览器缓存与 Code Cache",
            tier=CleanTier.SAFE,
            paths=[
                local / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache",
                local / "Microsoft" / "Edge" / "User Data" / "Default" / "Code Cache",
                local / "Microsoft" / "Edge" / "User Data" / "Default" / "GPUCache",
            ],
            default_selected=False,
        ),
        CleanCategory(
            id="chrome_cache",
            name="Google Chrome 缓存",
            description="Chrome 浏览器缓存（如已安装）",
            tier=CleanTier.SAFE,
            paths=[
                local / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
                local / "Google" / "Chrome" / "User Data" / "Default" / "Code Cache",
                local / "Google" / "Chrome" / "User Data" / "Default" / "GPUCache",
            ],
            default_selected=False,
        ),
        CleanCategory(
            id="delivery_optimization",
            name="传递优化缓存",
            description="Windows 更新传递优化下载缓存",
            tier=CleanTier.SAFE,
            paths=[
                program_data / "Microsoft" / "Windows" / "DeliveryOptimization" / "Cache",
            ],
            requires_admin=True,
            default_selected=True,
        ),
        CleanCategory(
            id="error_reports",
            name="Windows 错误报告",
            description="WER 本地错误报告与队列文件",
            tier=CleanTier.SAFE,
            paths=[
                program_data / "Microsoft" / "Windows" / "WER",
                local / "Microsoft" / "Windows" / "WER",
            ],
            default_selected=True,
        ),
        CleanCategory(
            id="windows_logs",
            name="旧系统日志",
            description="CBS、DISM 等超过 30 天的日志文件",
            tier=CleanTier.SAFE,
            paths=[
                win / "Logs" / "CBS",
                win / "Logs" / "DISM",
                win / "Logs" / "WindowsUpdate",
            ],
            glob_patterns=["*.log", "*.etl"],
            min_age_days=30,
            requires_admin=True,
            default_selected=False,
        ),
        CleanCategory(
            id="update_download_cache",
            name="Windows 更新下载缓存",
            description="SoftwareDistribution\\Download 已下载更新包",
            tier=CleanTier.DEEP,
            paths=[win / "SoftwareDistribution" / "Download"],
            requires_admin=True,
            default_selected=False,
        ),
        CleanCategory(
            id="windows_old",
            name="旧 Windows 安装 (Windows.old)",
            description="系统升级后保留的旧系统文件夹，删除后无法回退",
            tier=CleanTier.DEEP,
            paths=[win / "Windows.old"],
            requires_admin=True,
            default_selected=False,
        ),
        CleanCategory(
            id="upgrade_temp",
            name="升级临时文件夹",
            description="$Windows.~BT / $Windows.~WS 等升级残留",
            tier=CleanTier.DEEP,
            paths=[
                system / "$Windows.~BT",
                system / "$Windows.~WS",
                system / "$GetCurrent",
            ],
            requires_admin=True,
            default_selected=False,
        ),
        CleanCategory(
            id="prefetch",
            name="Prefetch 预读取",
            description="系统预读取文件，清理后短期内可能略慢",
            tier=CleanTier.DEEP,
            paths=[win / "Prefetch"],
            glob_patterns=["*.pf"],
            requires_admin=True,
            default_selected=False,
        ),
        CleanCategory(
            id="large_downloads",
            name="下载文件夹大文件",
            description="Downloads 中超过 500MB 的文件（需逐项确认）",
            tier=CleanTier.DEEP,
            paths=[user / "Downloads"],
            min_size_mb=500,
            default_selected=False,
        ),
        CleanCategory(
            id="installer_leftovers",
            name="安装程序残留",
            description="用户目录下常见 .msi / .exe 安装包缓存",
            tier=CleanTier.DEEP,
            paths=[
                local / "Downloaded Installations",
                user / "AppData" / "Local" / "Temp",
            ],
            glob_patterns=["*.msi", "*.exe"],
            min_age_days=7,
            default_selected=False,
        ),
    ]


def categories_by_tier(tier: CleanTier | None = None) -> list[CleanCategory]:
    items = build_categories()
    if tier is None:
        return items
    return [item for item in items if item.tier == tier]
