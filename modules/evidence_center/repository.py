from modules.evidence_center.domain import EvidenceItem
from modules.evidence_center.store import get_mock_evidence_items


class EvidenceRepository:
    """
    Evidence Repository

    統一管理證據資料的取得方式。

    Store 僅負責提供資料來源，
    Repository 對外提供一致的證據查詢介面。

    GM-07 Final Product Audit：
    - 不新增功能
    - 不改變 Architecture
    - 保留既有 Repository 職責
    - 強化文件說明與可讀性
    """

    def __init__(self):
        self._items = get_mock_evidence_items()

    def list_all(self) -> list[EvidenceItem]:
        """
        取得所有證據。

        回傳資料副本，避免外部直接修改 Repository 內部狀態。
        """

        return list(self._items)

    def get_by_id(self, evidence_id: str) -> EvidenceItem | None:
        """
        依照證據編號取得單筆證據。
        """

        for item in self._items:
            if item.evidence_id == evidence_id:
                return item

        return None

    def get_by_platform(self, platform: str) -> list[EvidenceItem]:
        """
        依照資料來源取得證據。
        """

        return [
            item
            for item in self._items
            if item.platform == platform
        ]

    def get_by_topic(self, topic: str) -> list[EvidenceItem]:
        """
        依照討論議題取得證據。
        """

        return [
            item
            for item in self._items
            if item.topic == topic
        ]

    def get_by_sentiment(self, sentiment: str) -> list[EvidenceItem]:
        """
        依照情緒傾向取得證據。
        """

        return [
            item
            for item in self._items
            if item.sentiment == sentiment
        ]

    def get_recent(self, limit: int = 10) -> list[EvidenceItem]:
        """
        取得最新證據。

        依發佈時間由新到舊排序，回傳指定筆數。
        """

        return sorted(
            self._items,
            key=lambda item: item.published_time,
            reverse=True,
        )[:limit]