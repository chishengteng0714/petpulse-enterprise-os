from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class WorkspaceState:
    """
    Workspace State

    管理 Evidence Workspace 的畫面狀態。

    GM-07 Final Product Audit：
    - 不新增功能
    - 不改變 Architecture
    - 保留既有 State 結構
    - 強化文件說明與可讀性
    """

    investigation_state: Any = None

    # Master / Detail
    selected_evidence: Optional[Any] = None
    selected_evidence_2: Optional[Any] = None

    # Compare Mode
    compare_mode: bool = False

    # Workspace Memory
    selection_history: List[Any] = None
    compare_history: List[Any] = None

    def __post_init__(self):
        """
        初始化 Workspace Memory。
        """

        if self.selection_history is None:
            self.selection_history = []

        if self.compare_history is None:
            self.compare_history = []