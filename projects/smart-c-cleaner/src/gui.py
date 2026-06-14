from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk

from cleaner.categories import CleanCategory, CleanTier, build_categories
from cleaner.clean_engine import clean_categories
from cleaner.scanner import CategoryScanResult, scan_categories
from cleaner.utils import format_size, is_admin, relaunch_as_admin

try:
    import psutil
except ImportError:
    psutil = None


class SmartCCleanerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Smart C Cleaner - 智能 C 盘清理")
        self.root.geometry("860x620")
        self.root.minsize(760, 540)

        self.categories = build_categories()
        self.scan_results: dict[str, CategoryScanResult] = {}
        self.check_vars: dict[str, tk.BooleanVar] = {}
        self.size_labels: dict[str, ttk.Label] = {}

        self.status_var = tk.StringVar(value="就绪")
        self.summary_var = tk.StringVar(value="尚未扫描")
        self.disk_var = tk.StringVar(value="正在读取磁盘信息...")
        self.progress_var = tk.DoubleVar(value=0.0)

        self._build_ui()
        self._refresh_disk_info()

    def _build_ui(self) -> None:
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")

        ttk.Label(header, text="Smart C Cleaner", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(header, text="安全清理 + 深度清理（深度项会二次确认）").pack(anchor="w")
        ttk.Label(header, textvariable=self.disk_var).pack(anchor="w", pady=(6, 0))

        admin_text = "管理员模式" if is_admin() else "普通用户（部分项目需管理员权限）"
        ttk.Label(header, text=admin_text, foreground="#555").pack(anchor="w")

        body = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        body.pack(fill="both", expand=True)

        columns = ("name", "tier", "size", "count", "note")
        self.tree = ttk.Treeview(body, columns=columns, show="headings", height=16)
        self.tree.heading("name", text="清理项")
        self.tree.heading("tier", text="类型")
        self.tree.heading("size", text="大小")
        self.tree.heading("count", text="文件数")
        self.tree.heading("note", text="说明")

        self.tree.column("name", width=220, anchor="w")
        self.tree.column("tier", width=60, anchor="center")
        self.tree.column("size", width=100, anchor="e")
        self.tree.column("count", width=70, anchor="e")
        self.tree.column("note", width=360, anchor="w")

        scroll = ttk.Scrollbar(body, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for category in self.categories:
            var = tk.BooleanVar(value=category.default_selected)
            self.check_vars[category.id] = var
            tier = "深度" if category.tier == CleanTier.DEEP else "安全"
            note = category.description
            if category.requires_admin:
                note += " [需管理员]"
            self.tree.insert(
                "",
                "end",
                iid=category.id,
                values=(category.name, tier, "-", "-", note),
            )
            self._refresh_row_check(category.id)

        self.tree.bind("<Button-1>", self._toggle_checkbox)

        footer = ttk.Frame(self.root, padding=12)
        footer.pack(fill="x")

        btn_row = ttk.Frame(footer)
        btn_row.pack(fill="x")

        ttk.Button(btn_row, text="全选安全项", command=self._select_safe).pack(side="left")
        ttk.Button(btn_row, text="全选", command=self._select_all).pack(side="left", padx=6)
        ttk.Button(btn_row, text="全不选", command=self._select_none).pack(side="left")
        ttk.Button(btn_row, text="扫描", command=self._start_scan).pack(side="right")
        ttk.Button(btn_row, text="清理选中项", command=self._start_clean).pack(side="right", padx=6)

        if not is_admin():
            ttk.Button(btn_row, text="管理员运行", command=relaunch_as_admin).pack(side="right", padx=6)

        ttk.Label(footer, textvariable=self.summary_var).pack(anchor="w", pady=(8, 4))
        ttk.Progressbar(footer, variable=self.progress_var, maximum=100).pack(fill="x")
        ttk.Label(footer, textvariable=self.status_var).pack(anchor="w", pady=(4, 0))

    def _refresh_disk_info(self) -> None:
        if psutil is None:
            self.disk_var.set("C: 盘信息需要安装 psutil（pip install psutil）")
            return
        try:
            usage = psutil.disk_usage("C:\\")
            self.disk_var.set(
                f"C: 总容量 {format_size(usage.total)} | "
                f"已用 {format_size(usage.used)} | "
                f"可用 {format_size(usage.free)} ({100 - usage.percent:.1f}% 可用)"
            )
        except Exception as exc:
            self.disk_var.set(f"无法读取 C: 盘信息: {exc}")

    def _toggle_checkbox(self, event) -> None:
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        if self.tree.identify_column(event.x) != "#1":
            return
        var = self.check_vars.get(row_id)
        if var is None:
            return
        var.set(not var.get())
        self._refresh_row_check(row_id)

    def _refresh_row_check(self, category_id: str) -> None:
        category = next(item for item in self.categories if item.id == category_id)
        selected = self.check_vars[category_id].get()
        prefix = "[x]" if selected else "[ ]"
        values = list(self.tree.item(category_id, "values"))
        values[0] = f"{prefix} {category.name}"
        self.tree.item(category_id, values=values)

    def _select_safe(self) -> None:
        for category in self.categories:
            self.check_vars[category.id].set(category.tier == CleanTier.SAFE)
            self._refresh_row_check(category.id)

    def _select_all(self) -> None:
        for category in self.categories:
            self.check_vars[category.id].set(True)
            self._refresh_row_check(category.id)

    def _select_none(self) -> None:
        for category in self.categories:
            self.check_vars[category.id].set(False)
            self._refresh_row_check(category.id)

    def _selected_categories(self) -> list[CleanCategory]:
        return [item for item in self.categories if self.check_vars[item.id].get()]

    def _update_scan_row(self, result: CategoryScanResult) -> None:
        category = result.category
        if not result.accessible:
            size_text = "需管理员"
        elif category.special == "recycle_bin":
            size_text = "待清空"
        else:
            size_text = format_size(result.total_size)
        values = list(self.tree.item(category.id, "values"))
        values[2] = size_text
        values[3] = str(result.file_count)
        values[4] = result.note or category.description
        self.tree.item(category.id, values=values)

    def _start_scan(self) -> None:
        selected = self._selected_categories()
        if not selected:
            messagebox.showwarning("提示", "请至少选择一项清理内容。")
            return
        self.status_var.set("正在扫描...")
        self.progress_var.set(5)
        threading.Thread(target=self._scan_worker, args=(selected,), daemon=True).start()

    def _scan_worker(self, categories: list[CleanCategory]) -> None:
        results = scan_categories(categories)
        total = 0
        for index, result in enumerate(results, start=1):
            self.scan_results[result.category.id] = result
            if result.accessible and result.category.special != "recycle_bin":
                total += result.total_size
            progress = index / len(results) * 100
            self.root.after(0, self._update_scan_row, result)
            self.root.after(0, self.progress_var.set, progress)
        self.root.after(
            0,
            self.summary_var.set,
            f"扫描完成，选中项预计可释放 {format_size(total)}（不含回收站）",
        )
        self.root.after(0, self.status_var.set, "扫描完成")

    def _start_clean(self) -> None:
        selected = self._selected_categories()
        if not selected:
            messagebox.showwarning("提示", "请至少选择一项清理内容。")
            return

        deep_items = [item for item in selected if item.tier == CleanTier.DEEP]
        if deep_items:
            names = "\n".join(f"- {item.name}" for item in deep_items)
            ok = messagebox.askyesno(
                "深度清理确认",
                f"你选择了以下深度清理项，可能无法恢复：\n\n{names}\n\n确定继续吗？",
            )
            if not ok:
                return

        need_admin = [item for item in selected if item.requires_admin]
        if need_admin and not is_admin():
            messagebox.showerror(
                "需要管理员权限",
                "选中项包含需要管理员权限的内容。\n请点击「管理员运行」后重试。",
            )
            return

        if not messagebox.askyesno("确认清理", "确定开始清理选中的项目吗？"):
            return

        self.status_var.set("正在清理...")
        self.progress_var.set(5)
        threading.Thread(target=self._clean_worker, args=(selected,), daemon=True).start()

    def _clean_worker(self, categories: list[CleanCategory]) -> None:
        scan_map = {
            item.id: self.scan_results[item.id]
            for item in categories
            if item.id in self.scan_results
        }
        summary = clean_categories(categories, scan_map)
        freed = summary.total_freed
        self.root.after(0, self._refresh_disk_info)
        self.root.after(0, self.progress_var.set, 100)
        self.root.after(
            0,
            self.summary_var.set,
            f"清理完成，共释放 {format_size(freed)}",
        )
        self.root.after(0, self.status_var.set, "清理完成")
        lines = [
            f"{'成功' if item.success else '失败'} - {item.category_name}: {item.message}"
            for item in summary.results
        ]
        self.root.after(0, messagebox.showinfo, "清理结果", "\n".join(lines))


def main() -> None:
    root = tk.Tk()
    style = ttk.Style()
    if "vista" in style.theme_names():
        style.theme_use("vista")
    SmartCCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
