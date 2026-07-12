"""
Evidence Table Compatibility Layer

正式 UI Component 已移至：

modules.evidence_center.components.evidence_table

此檔案僅保留舊版匯入相容性，避免既有程式碼失效。

GM-07 Final Product Audit：
- 不新增功能
- 不改變 Architecture
- 保留 Backward Compatibility
- 不改變 Runtime Behavior
- 統一文件說明
"""

from modules.evidence_center.components.evidence_table import (
    render_evidence_table,
)

__all__ = [
    "render_evidence_table",
]