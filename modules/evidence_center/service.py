import inspect
import json
from pathlib import Path
from typing import TYPE_CHECKING

from modules.evidence_center.domain import EvidenceItem
from modules.evidence_center.query_engine import EvidenceQueryEngine
from modules.evidence_center.repository import EvidenceRepository

if TYPE_CHECKING:
    from modules.evidence_center.investigation_state import InvestigationState


ANALYSIS_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "analysis.json"
)


class EvidenceService:
    """
    Evidence Service

    GM26 Executive Evidence Intelligence：
    - Evidence Center 唯一資料來源改為 analysis.json。
    - 只載入 Analyzer 驗證後的 evidence_items。
    - 不再直接讀取 Crawler 原始資料。
    - 保留既有 Service、Query Engine 與 EvidenceItem 架構。
    - 支援 Brand Confidence、可信度等級與高風險標記。
    """

    def __init__(self):
        # 保留既有 Repository 依賴，避免破壞 Architecture。
        # GM25 的讀取入口改由 Service 載入 Analyzer 結果。
        self.repository = EvidenceRepository()
        self.query_engine = EvidenceQueryEngine()

    def get_all_evidence(self):
        """
        取得 Analyzer 驗證後的所有品牌證據。

        GM25 預設順序：
        1. 高風險與負向訊號置頂。
        2. Brand Confidence 由高到低。
        3. 發布時間由新到舊。
        """
        items = self._load_analyzed_evidence()

        return self._sort_gm25_default(
            items
        )

    def query_evidence(
        self,
        platform=None,
        topic=None,
        sentiment=None,
        keyword=None,
        sort_by="GM25 智慧排序",
        confidence_level=None,
        brand_only=False,
        high_risk_only=False,
    ):
        """
        依照查詢條件取得 Analyzer 驗證後證據。

        既有查詢參數維持不變，並增加 GM25 條件：
        - confidence_level
        - brand_only
        - high_risk_only
        """
        items = self._load_analyzed_evidence()

        results = self.query_engine.filter_by_platform(
            items,
            platform,
        )
        results = self.query_engine.filter_by_topic(
            results,
            topic,
        )
        results = self.query_engine.filter_by_sentiment(
            results,
            sentiment,
        )
        results = self.query_engine.filter_by_keyword(
            results,
            keyword,
        )

        results = self._filter_by_confidence_level(
            results,
            confidence_level,
        )

        if brand_only:
            results = [
                item
                for item in results
                if bool(
                    getattr(
                        item,
                        "is_brand_signal",
                        True,
                    )
                )
            ]

        if high_risk_only:
            results = [
                item
                for item in results
                if bool(
                    getattr(
                        item,
                        "is_high_risk",
                        False,
                    )
                )
            ]

        return self._sort_results(
            results,
            sort_by,
        )

    def query_by_state(
        self,
        state: "InvestigationState",
    ):
        """
        依照畫面目前的查詢條件取得證據。
        """
        return self.query_evidence(
            platform=_normalize_platform(
                state.platform
            ),
            topic=_normalize_topic(
                state.topic
            ),
            sentiment=_normalize_sentiment(
                state.sentiment
            ),
            keyword=_normalize_keyword(
                state.keyword
            ),
            sort_by=_normalize_sort_by(
                state.sort_by
            ),
        )

    def get_recent_evidence(
        self,
        limit=5,
    ):
        """
        取得近期 Analyzer 品牌證據。
        """
        items = self._load_analyzed_evidence()

        return sorted(
            items,
            key=lambda item: _published_value(
                item
            ),
            reverse=True,
        )[:limit]

    def get_negative_evidence(self):
        """
        取得負向品牌證據。
        """
        return self.query_evidence(
            sentiment="Negative"
        )

    def get_positive_evidence(self):
        """
        取得正向品牌證據。
        """
        return self.query_evidence(
            sentiment="Positive"
        )

    def get_high_risk_evidence(self):
        """
        取得 Analyzer 標記的高風險品牌證據。
        """
        return self.query_evidence(
            high_risk_only=True
        )

    def get_confidence_evidence(
        self,
        confidence_level,
    ):
        """
        依可信度等級取得品牌證據。
        """
        return self.query_evidence(
            confidence_level=(
                confidence_level
            )
        )

    def get_platform_summary(self):
        """
        取得各來源範圍的證據數量摘要。
        """
        return self._count_by_field(
            "platform"
        )

    def get_sentiment_summary(self):
        """
        取得各情緒狀態的證據數量摘要。
        """
        return self._count_by_field(
            "sentiment"
        )

    def get_topic_summary(self):
        """
        取得各議題範圍的證據數量摘要。
        """
        return self._count_by_field(
            "topic"
        )

    def get_confidence_summary(self):
        """
        取得各可信度等級的證據數量摘要。
        """
        return self._count_by_field(
            "confidence_level"
        )

    def get_kpi_summary(self):
        """
        直接讀取 analysis.json 的 GM25 KPI。

        Evidence Center 與 Executive Home 使用同一份來源，
        避免再次出現首頁 127、Evidence 406 的落差。
        """
        analysis = self._load_analysis()

        evidence_items = analysis.get(
            "evidence_items",
            [],
        )

        if not isinstance(
            evidence_items,
            list,
        ):
            evidence_items = []

        return {
            "brand_health": _safe_int(
                analysis.get(
                    "brand_health",
                    0,
                )
            ),
            "brand_signal_count": (
                _safe_int(
                    analysis.get(
                        "brand_signal_count",
                        len(evidence_items),
                    )
                )
            ),
            "evidence_count": len(
                evidence_items
            ),
            "high_risk_count": (
                _safe_int(
                    analysis.get(
                        "high_risk_count",
                        0,
                    )
                )
            ),
            "brand_confidence_average": (
                _safe_float(
                    analysis.get(
                        "brand_confidence_average",
                        0,
                    )
                )
            ),
            "data_quality": str(
                analysis.get(
                    "data_quality",
                    "資料不足",
                )
            ).strip(),
            "positive": _safe_int(
                analysis.get(
                    "positive",
                    0,
                )
            ),
            "neutral": _safe_int(
                analysis.get(
                    "neutral",
                    0,
                )
            ),
            "negative": _safe_int(
                analysis.get(
                    "negative",
                    0,
                )
            ),
        }

    def _count_by_field(
        self,
        field_name,
    ):
        """
        依指定欄位統計 Analyzer 證據數量。
        """
        summary = {}

        for item in self._load_analyzed_evidence():
            value = getattr(
                item,
                field_name,
                None,
            )

            if hasattr(
                value,
                "value",
            ):
                value = value.value

            summary[value] = (
                summary.get(
                    value,
                    0,
                )
                + 1
            )

        return summary

    def _load_analysis(self):
        """
        安全讀取 analysis.json。

        找不到、格式錯誤或內容不是 JSON 物件時，
        回傳空字典，不回退到 Crawler。
        """
        if not ANALYSIS_PATH.exists():
            return {}

        try:
            with open(
                ANALYSIS_PATH,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(
                    file
                )
        except (
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError,
        ):
            return {}

        if not isinstance(
            data,
            dict,
        ):
            return {}

        return data

    def _load_analyzed_evidence(self):
        """
        將 analysis.json 的 evidence_items
        轉為既有 EvidenceItem 物件。
        """
        analysis = self._load_analysis()

        raw_items = analysis.get(
            "evidence_items",
            [],
        )

        if not isinstance(
            raw_items,
            list,
        ):
            return []

        items = []

        for raw_item in raw_items:
            if not isinstance(
                raw_item,
                dict,
            ):
                continue

            item = self._build_evidence_item(
                raw_item
            )

            if item is not None:
                items.append(
                    item
                )

        return items

    def _build_evidence_item(
        self,
        raw_item,
    ):
        """
        依現有 EvidenceItem 真實建構參數建立物件。

        GM25 不修改 Domain Schema。
        額外情報欄位以相容屬性附加，
        供新版 Evidence Table 使用。
        """
        normalized = {
            "evidence_id": str(
                raw_item.get(
                    "evidence_id",
                    "",
                )
            ).strip(),
            "platform": str(
                raw_item.get(
                    "platform",
                    raw_item.get(
                        "source",
                        "News",
                    ),
                )
            ).strip(),
            "author": str(
                raw_item.get(
                    "author",
                    raw_item.get(
                        "publisher",
                        "",
                    ),
                )
            ).strip(),
            "content": str(
                raw_item.get(
                    "content",
                    raw_item.get(
                        "snippet",
                        raw_item.get(
                            "title",
                            "",
                        ),
                    ),
                )
            ).strip(),
            "ai_summary": str(
                raw_item.get(
                    "ai_summary",
                    raw_item.get(
                        "snippet",
                        raw_item.get(
                            "title",
                            "",
                        ),
                    ),
                )
            ).strip(),
            "topic": str(
                raw_item.get(
                    "topic",
                    "品牌情報",
                )
            ).strip(),
            "sentiment": (
                _normalize_item_sentiment(
                    raw_item.get(
                        "sentiment",
                        "neutral",
                    )
                )
            ),
            "published_time": str(
                raw_item.get(
                    "published_time",
                    raw_item.get(
                        "published_at",
                        "",
                    ),
                )
            ).strip(),
            "engagement": _safe_int(
                raw_item.get(
                    "engagement",
                    0,
                )
            ),
            "original_url": str(
                raw_item.get(
                    "original_url",
                    raw_item.get(
                        "url",
                        "",
                    ),
                )
            ).strip(),
        }

        try:
            signature = inspect.signature(
                EvidenceItem
            )

            accepted_fields = {
                name
                for name in signature.parameters
                if name != "self"
            }

            constructor_values = {
                key: value
                for key, value
                in normalized.items()
                if key in accepted_fields
            }

            item = EvidenceItem(
                **constructor_values
            )
        except (
            TypeError,
            ValueError,
        ):
            return None

        extra_values = {
            "title": str(
                raw_item.get(
                    "title",
                    "",
                )
            ).strip(),
            "snippet": str(
                raw_item.get(
                    "snippet",
                    "",
                )
            ).strip(),
            "publisher": str(
                raw_item.get(
                    "publisher",
                    normalized["author"],
                )
            ).strip(),
            "source": str(
                raw_item.get(
                    "source",
                    normalized["platform"],
                )
            ).strip(),
            "published_at": str(
                raw_item.get(
                    "published_at",
                    normalized[
                        "published_time"
                    ],
                )
            ).strip(),
            "collected_at": str(
                raw_item.get(
                    "collected_at",
                    "",
                )
            ).strip(),
            "brand_confidence": (
                _safe_int(
                    raw_item.get(
                        "brand_confidence",
                        0,
                    )
                )
            ),
            "raw_brand_confidence": (
                _safe_int(
                    raw_item.get(
                        "raw_brand_confidence",
                        raw_item.get(
                            "brand_confidence",
                            0,
                        ),
                    )
                )
            ),
            "confidence_level": str(
                raw_item.get(
                    "confidence_level",
                    "一般",
                )
            ).strip(),
            "executive_summary": str(
                raw_item.get(
                    "executive_summary",
                    raw_item.get(
                        "ai_summary",
                        raw_item.get(
                            "snippet",
                            raw_item.get(
                                "title",
                                "",
                            ),
                        ),
                    ),
                )
            ).strip(),
            "impact_level": str(
                raw_item.get(
                    "impact_level",
                    "一般",
                )
            ).strip(),
            "recommended_action": str(
                raw_item.get(
                    "recommended_action",
                    "持續監測後續討論量與情緒變化。",
                )
            ).strip(),
            "is_brand_signal": bool(
                raw_item.get(
                    "is_brand_signal",
                    True,
                )
            ),
            "is_high_risk": bool(
                raw_item.get(
                    "is_high_risk",
                    False,
                )
            ),
            "is_negative": bool(
                raw_item.get(
                    "is_negative",
                    (
                        normalized[
                            "sentiment"
                        ]
                        == "Negative"
                    ),
                )
            ),
            "result_type": str(
                raw_item.get(
                    "result_type",
                    "brand",
                )
            ).strip(),
        }

        for key, value in (
            extra_values.items()
        ):
            try:
                setattr(
                    item,
                    key,
                    value,
                )
            except (
                AttributeError,
                TypeError,
            ):
                try:
                    object.__setattr__(
                        item,
                        key,
                        value,
                    )
                except (
                    AttributeError,
                    TypeError,
                ):
                    pass

        return item

    def _filter_by_confidence_level(
        self,
        items,
        confidence_level,
    ):
        """
        依 GM25 可信度等級篩選。
        """
        normalized_level = (
            _normalize_confidence_level(
                confidence_level
            )
        )

        if normalized_level is None:
            return items

        return [
            item
            for item in items
            if str(
                getattr(
                    item,
                    "confidence_level",
                    "",
                )
            ).strip()
            == normalized_level
        ]

    def _sort_results(
        self,
        items,
        sort_by,
    ):
        """
        保留既有排序選項，增加 GM25 智慧排序。
        """
        normalized_sort = (
            _normalize_sort_by(
                sort_by
            )
        )

        if normalized_sort == (
            "GM25 智慧排序"
        ):
            return self._sort_gm25_default(
                items
            )

        if normalized_sort == (
            "可信度高到低"
        ):
            return sorted(
                items,
                key=lambda item: (
                    _confidence_value(
                        item
                    ),
                    _published_value(
                        item
                    ),
                ),
                reverse=True,
            )

        if normalized_sort == (
            "負向優先"
        ):
            return sorted(
                items,
                key=lambda item: (
                    _negative_value(
                        item
                    ),
                    _risk_value(
                        item
                    ),
                    _confidence_value(
                        item
                    ),
                    _published_value(
                        item
                    ),
                ),
                reverse=True,
            )

        return self.query_engine.sort(
            items,
            normalized_sort,
        )

    def _sort_gm25_default(
        self,
        items,
    ):
        """
        GM25 主管決策排序。

        負向與高風險固定置頂，再比較可信度與發布時間。
        """
        return sorted(
            items,
            key=lambda item: (
                _risk_value(
                    item
                ),
                _negative_value(
                    item
                ),
                _confidence_value(
                    item
                ),
                _published_value(
                    item
                ),
            ),
            reverse=True,
        )


def _normalize_platform(value):
    """
    正規化來源範圍查詢條件。
    """
    if value in [
        None,
        "",
        "All",
        "全部",
    ]:
        return None

    return value


def _normalize_topic(value):
    """
    正規化議題範圍查詢條件。
    """
    if value in [
        None,
        "",
        "All",
        "全部",
    ]:
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
        "positive": "Positive",
        "正向": "Positive",
        "Neutral": "Neutral",
        "neutral": "Neutral",
        "中立": "Neutral",
        "Negative": "Negative",
        "negative": "Negative",
        "負向": "Negative",
        "Mixed": "Mixed",
        "mixed": "Mixed",
        "Unknown": "Unknown",
        "unknown": "Unknown",
    }

    return sentiment_map.get(
        value,
        value,
    )


def _normalize_item_sentiment(value):
    """
    將 analysis.json 的小寫情緒轉為既有 Evidence 格式。
    """
    normalized = _normalize_sentiment(
        value
    )

    if normalized is None:
        return "Neutral"

    return normalized


def _normalize_confidence_level(value):
    """
    正規化可信度篩選條件。
    """
    if value in [
        None,
        "",
        "All",
        "全部",
    ]:
        return None

    level_map = {
        "極高": "極高",
        "高": "高",
        "中": "中",
        "一般": "一般",
    }

    return level_map.get(
        str(value).strip(),
        str(value).strip(),
    )


def _normalize_keyword(value):
    """
    正規化關鍵字查詢條件。
    """
    if value is None:
        return None

    keyword = str(
        value
    ).strip()

    if not keyword:
        return None

    return keyword


def _normalize_sort_by(value):
    """
    正規化排序條件。
    """
    sort_map = {
        None: "GM25 智慧排序",
        "": "GM25 智慧排序",
        "GM25": "GM25 智慧排序",
        "智慧排序": "GM25 智慧排序",
        "主管決策排序": "GM25 智慧排序",
        "Recent": "最新優先",
        "最新時間": "最新優先",
        "Engagement": "互動高到低",
        "互動數": "互動高到低",
        "Brand Confidence": (
            "可信度高到低"
        ),
        "可信度": "可信度高到低",
        "Negative": "負向優先",
        "負向": "負向優先",
    }

    return sort_map.get(
        value,
        value,
    )


def _safe_int(value):
    """
    安全轉換整數。
    """
    try:
        return int(
            round(
                float(value)
            )
        )
    except (
        TypeError,
        ValueError,
    ):
        return 0


def _safe_float(value):
    """
    安全轉換浮點數。
    """
    try:
        return round(
            float(value),
            1,
        )
    except (
        TypeError,
        ValueError,
    ):
        return 0.0


def _confidence_value(item):
    """
    取得 Brand Confidence 排序值。
    """
    return _safe_int(
        getattr(
            item,
            "brand_confidence",
            0,
        )
    )


def _negative_value(item):
    """
    取得負向排序值。
    """
    sentiment = getattr(
        item,
        "sentiment",
        "",
    )

    if hasattr(
        sentiment,
        "value",
    ):
        sentiment = sentiment.value

    return int(
        str(
            sentiment
        ).strip().lower()
        == "negative"
    )


def _risk_value(item):
    """
    取得高風險排序值。
    """
    return int(
        bool(
            getattr(
                item,
                "is_high_risk",
                False,
            )
        )
    )


def _published_value(item):
    """
    取得發布時間排序值。
    """
    value = getattr(
        item,
        "published_at",
        None,
    )

    if value in [
        None,
        "",
    ]:
        value = getattr(
            item,
            "published_time",
            "",
        )

    return str(
        value
    ).strip()
