from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from cleaner.categories import CleanCategory, CleanTier
from cleaner.scanner import CategoryScanResult, scan_category
from cleaner.utils import empty_recycle_bin, is_admin


@dataclass
class CleanActionResult:
    category_id: str
    category_name: str
    freed_bytes: int = 0
    deleted_count: int = 0
    success: bool = True
    message: str = ""


@dataclass
class CleanSummary:
    results: list[CleanActionResult] = field(default_factory=list)

    @property
    def total_freed(self) -> int:
        return sum(item.freed_bytes for item in self.results if item.success)

    @property
    def success_count(self) -> int:
        return sum(1 for item in self.results if item.success)


def _delete_path(path: Path) -> tuple[bool, int]:
    try:
        if not path.exists():
            return True, 0
        if path.is_file() or path.is_symlink():
            size = path.stat().st_size
            path.unlink(missing_ok=True)
            return True, size
        size = _directory_size(path)
        shutil.rmtree(path, ignore_errors=False)
        return True, size
    except OSError:
        return False, 0


def _directory_size(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0
    if path.is_file():
        try:
            return path.stat().st_size
        except OSError:
            return 0
    for child in path.rglob("*"):
        if child.is_file():
            try:
                total += child.stat().st_size
            except OSError:
                continue
    return total


def _clean_directory_contents(path: Path, scan_result: CategoryScanResult) -> tuple[int, int, str]:
    freed = 0
    deleted = 0
    errors: list[str] = []

    if scan_result.items:
        for item in scan_result.items:
            ok, size = _delete_path(item.path)
            if ok:
                freed += size
                deleted += 1
            else:
                errors.append(str(item.path))
        if errors:
            return freed, deleted, f"部分文件删除失败: {len(errors)} 个"
        return freed, deleted, f"已删除 {deleted} 个文件"

    if not path.exists():
        return 0, 0, "目录不存在"

    try:
        if path.is_file():
            size = path.stat().st_size
            path.unlink(missing_ok=True)
            return size, 1, "已删除文件"
        freed = _directory_size(path)
        for child in path.iterdir():
            if child.is_dir():
                shutil.rmtree(child, ignore_errors=True)
            else:
                child.unlink(missing_ok=True)
        deleted = scan_result.file_count or 1
        return freed, deleted, "已清空目录内容"
    except OSError as exc:
        return freed, deleted, f"清理失败: {exc}"


def clean_category(category: CleanCategory, scan_result: CategoryScanResult | None = None) -> CleanActionResult:
    if category.requires_admin and not is_admin():
        return CleanActionResult(
            category_id=category.id,
            category_name=category.name,
            success=False,
            message="需要管理员权限，请以管理员身份运行",
        )

    if scan_result is None:
        scan_result = scan_category(category)

    if category.special == "recycle_bin":
        ok, message = empty_recycle_bin()
        return CleanActionResult(
            category_id=category.id,
            category_name=category.name,
            success=ok,
            message=message,
        )

    if not scan_result.accessible:
        return CleanActionResult(
            category_id=category.id,
            category_name=category.name,
            success=False,
            message=scan_result.note or "无法访问",
        )

    total_freed = 0
    total_deleted = 0
    messages: list[str] = []

    if category.id == "large_downloads":
        for item in scan_result.items:
            ok, size = _delete_path(item.path)
            if ok:
                total_freed += size
                total_deleted += 1
        return CleanActionResult(
            category_id=category.id,
            category_name=category.name,
            freed_bytes=total_freed,
            deleted_count=total_deleted,
            success=True,
            message=f"已删除 {total_deleted} 个大文件",
        )

    for path in category.paths:
        freed, deleted, message = _clean_directory_contents(path, scan_result)
        total_freed += freed
        total_deleted += deleted
        if message:
            messages.append(message)

    if category.id in {"windows_old", "upgrade_temp"}:
        for path in category.paths:
            if path.exists() and path.is_dir():
                try:
                    size = _directory_size(path)
                    shutil.rmtree(path, ignore_errors=False)
                    total_freed += size
                    total_deleted += 1
                    messages.append(f"已删除 {path.name}")
                except OSError as exc:
                    return CleanActionResult(
                        category_id=category.id,
                        category_name=category.name,
                        freed_bytes=total_freed,
                        deleted_count=total_deleted,
                        success=False,
                        message=f"删除 {path} 失败: {exc}",
                    )

    if total_freed == 0 and total_deleted == 0:
        return CleanActionResult(
            category_id=category.id,
            category_name=category.name,
            success=True,
            message="没有需要清理的内容",
        )

    return CleanActionResult(
        category_id=category.id,
        category_name=category.name,
        freed_bytes=total_freed,
        deleted_count=total_deleted,
        success=True,
        message="; ".join(messages) if messages else "清理完成",
    )


def clean_categories(
    categories: list[CleanCategory],
    scan_results: dict[str, CategoryScanResult] | None = None,
) -> CleanSummary:
    summary = CleanSummary()
    for category in categories:
        scan_result = (scan_results or {}).get(category.id)
        summary.results.append(clean_category(category, scan_result))
    return summary


def deep_categories_need_confirm(categories: list[CleanCategory]) -> list[CleanCategory]:
    return [item for item in categories if item.tier == CleanTier.DEEP]
