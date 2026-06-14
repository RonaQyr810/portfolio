from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from cleaner.categories import CleanCategory
from cleaner.utils import is_admin


@dataclass
class ScanItem:
    path: Path
    size: int
    category_id: str


@dataclass
class CategoryScanResult:
    category: CleanCategory
    total_size: int = 0
    file_count: int = 0
    items: list[ScanItem] = field(default_factory=list)
    accessible: bool = True
    note: str = ""


def _file_age_days(path: Path) -> float:
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return 0
    return (time.time() - mtime) / 86400


def _matches_filters(path: Path, category: CleanCategory) -> bool:
    if category.glob_patterns:
        if not any(path.match(pattern) for pattern in category.glob_patterns):
            return False
    if category.min_age_days is not None:
        if _file_age_days(path) < category.min_age_days:
            return False
    if category.min_size_mb is not None:
        try:
            if path.stat().st_size < category.min_size_mb * 1024 * 1024:
                return False
        except OSError:
            return False
    return True


def _scan_file(path: Path, category: CleanCategory) -> ScanItem | None:
    if not path.is_file():
        return None
    if not _matches_filters(path, category):
        return None
    try:
        size = path.stat().st_size
    except OSError:
        return None
    return ScanItem(path=path, size=size, category_id=category.id)


def _scan_directory(path: Path, category: CleanCategory) -> tuple[int, int, list[ScanItem]]:
    total = 0
    count = 0
    items: list[ScanItem] = []

    if not path.exists():
        return 0, 0, items

    if category.glob_patterns and path.is_dir():
        for pattern in category.glob_patterns:
            for match in path.glob(pattern):
                item = _scan_file(match, category)
                if item:
                    total += item.size
                    count += 1
                    items.append(item)
        return total, count, items

    if path.is_file():
        item = _scan_file(path, category)
        if item:
            return item.size, 1, [item]
        return 0, 0, items

    try:
        for root, _, files in os.walk(path, topdown=True, onerror=lambda _: None):
            root_path = Path(root)
            for name in files:
                file_path = root_path / name
                item = _scan_file(file_path, category)
                if item:
                    total += item.size
                    count += 1
                    items.append(item)
    except OSError:
        pass

    return total, count, items


def scan_category(category: CleanCategory) -> CategoryScanResult:
    if category.special == "recycle_bin":
        return CategoryScanResult(
            category=category,
            total_size=0,
            file_count=0,
            note="回收站大小无法精确统计，清理时将直接清空",
        )

    if category.requires_admin and not is_admin():
        return CategoryScanResult(
            category=category,
            accessible=False,
            note="需要管理员权限",
        )

    total = 0
    count = 0
    items: list[ScanItem] = []

    for path in category.paths:
        size, file_count, found = _scan_directory(path, category)
        total += size
        count += file_count
        items.extend(found)

    note = ""
    if total == 0 and count == 0:
        note = "未发现可清理内容"

    return CategoryScanResult(
        category=category,
        total_size=total,
        file_count=count,
        items=items,
        note=note,
    )


def scan_categories(categories: list[CleanCategory]) -> list[CategoryScanResult]:
    return [scan_category(category) for category in categories]
