from typing import TYPE_CHECKING

from modules.evidence_center.query_engine import EvidenceQueryEngine
from modules.evidence_center.repository import EvidenceRepository

if TYPE_CHECKING:
    from modules.evidence_center.investigation_state import InvestigationState


class EvidenceService:
    """
    Evidence Service

    證據中心的資料查詢入口。

    GM-07 Final Product Audit：
    - 不新增功能
    - 不改變 Architecture
    - 保留既有 Service 責任
    - 對齊 EvidenceItem schema
    - 強化查詢流程可讀性
    """

    def __init__(self):
        self.repository = EvidenceRepository()
        self.query_engine = EvidenceQueryEngine()

    def get_all_evidence(self):
        """
        取得所有證據。
        """

        return self.repository.list_all()

    def query_evidence(
        self,
        platform=None,
        topic=None,
        sentiment=None,
        keyword=None,
        sort_by="最新優先",
    ):
        """
        依照查詢條件取得證據。
        """

        items = self.repository.list_all()

        results = self.query_engine.filter_by_platform(items, platform)
        results = self.query_engine.filter_by_topic(results, topic)
        results = self.query_engine.filter_by_sentiment(results, sentiment)
        results = self.query_engine.filter_by_keyword(results, keyword)
        results = self.query_engine.sort(results, sort_by)

        return results

    def query_by_state(self, state: "InvestigationState"):
        """
        依照畫面目前的查詢條件取得證據。
        """

        return self.query_evidence(
            platform=_normalize_platform(state.platform),
            topic=_normalize_topic(state.topic),
            sentiment=_normalize_sentiment(state.sentiment),
            keyword=_normalize_keyword(state.keyword),
            sort_by=_normalize_sort_by(state.sort_by),
        )

    def get_recent_evidence(self, limit=5):
        """
        取得近期證據。
        """

        items = self.repository.list_all()

        return sorted(
            items,
            key=lambda item: item.published_time,
            reverse=True,
        )[:limit]

    def get_negative_evidence(self):
        """
        取得負向證據。
        """

        return self.query_evidence(sentiment="Negative")

    def get_positive_evidence(self):
        """
        取得正向證據。
        """

        return self.query_evidence(sentiment="Positive")

    def get_platform_summary(self):
        """
        取得各來源範圍的證據數量摘要。
        """

        return self._count_by_field("platform")

    def get_sentiment_summary(self):
        """
        取得各情緒狀態的證據數量摘要。
        """

        return self._count_by_field("sentiment")

    def get_topic_summary(self):
        """
        取得各議題範圍的證據數量摘要。
        """

        return self._count_by_field("topic")

    def _count_by_field(self, field_name):
        """
        依指定欄位統計證據數量。
        """

        summary = {}

        for item in self.repository.list_all():
            value = getattr(item, field_name, None)
            summary[value] = summary.get(value, 0) + 1

        return summary


def _normalize_platform(value):
    """
    正規化來源範圍查詢條件。
    """

    if value in [None, "", "All", "全部"]:
        return None

    return value


def _normalize_topic(value):
    """
    正規化議題範圍查詢條件。
    """

    if value in [None, "", "All", "全部"]:
        return None

    return value


def _normalize_sentiment(value):
    """
    正規化情緒狀態查詢條件。
    """

    sentiment_map = {
        None: None,
        "": None,
        "All": None,
        "全部": None,
        "Positive": "Positive",
        "正向": "Positive",
        "Neutral": "Neutral",
        "中立": "Neutral",
        "Negative": "Negative",
        "負向": "Negative",
        "Mixed": "Mixed",
        "Unknown": "Unknown",
    }

    return sentiment_map.get(value, value)


def _normalize_keyword(value):
    """
    正規化關鍵字查詢條件。
    """

    if value is None:
        return None

    keyword = str(value).strip()

    if not keyword:
        return None

    return keyword


def _normalize_sort_by(value):
    """
    正規化排序條件。
    """

    sort_map = {
        None: "最新優先",
        "": "最新優先",
        "Recent": "最新優先",
        "最新時間": "最新優先",
        "Engagement": "互動高到低",
        "互動數": "互動高到低",
    }

    return sort_map.get(value, value)