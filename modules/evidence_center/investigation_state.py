from dataclasses import dataclass


@dataclass
class InvestigationState:
    """
    Investigation State

    負責保存 Evidence Center 目前的查詢條件。

    GM-06 Final Product Audit：
    - 不新增功能
    - 不改變 Architecture
    - 保留既有 State 欄位
    - 強化命名一致性與可讀性
    """

    platform: str = "全部"
    topic: str = "全部"
    sentiment: str = "全部"
    keyword: str = ""
    sort_by: str = "最新優先"

    def reset(self):
        """
        重設查詢條件。
        """

        self.platform = "全部"
        self.topic = "全部"
        self.sentiment = "全部"
        self.keyword = ""
        self.sort_by = "最新優先"