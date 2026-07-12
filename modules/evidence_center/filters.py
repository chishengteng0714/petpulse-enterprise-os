"""
Compatibility Layer for Platform Filter

正式 UI Component 已移至：

modules.evidence_center.components.platform_filter

此檔案暫時保留，避免舊 import 失效。
未來確認所有呼叫端都完成 migration 後，可以安全移除。
"""

from modules.evidence_center.components.platform_filter import (
    render_platform_filter,
)


__all__ = [
    "render_platform_filter",
]