from modules.evidence_center.domain import EvidenceItem


class EvidenceQueryEngine:
    """
    Evidence Query Engine

    負責處理證據清單的查詢、篩選與排序。

    GM-07 Final Product Audit：
    - 不新增功能
    - 不改變 Architecture
    - 保留既有查詢責任
    - 對齊 EvidenceItem schema
    - 強化可讀性與防呆
    """

    def filter_by_platform(
        self,
        evidence_items: list[EvidenceItem],
        platform: str | None,
    ) -> list[EvidenceItem]:
        """
        依照資料來源篩選證據。
        """

        if self._is_empty_filter(platform):
            return list(evidence_items)

        selected_platform = self._normalize_text(platform)

        return [
            item
            for item in evidence_items
            if self._normalize_text(item.platform) == selected_platform
        ]

    def filter_by_topic(
        self,
        evidence_items: list[EvidenceItem],
        topic: str | None,
    ) -> list[EvidenceItem]:
        """
        依照討論議題篩選證據。
        """

        if self._is_empty_filter(topic):
            return list(evidence_items)

        selected_topic = self._normalize_text(topic)

        return [
            item
            for item in evidence_items
            if self._normalize_text(item.topic) == selected_topic
        ]

    def filter_by_sentiment(
        self,
        evidence_items: list[EvidenceItem],
        sentiment: str | None,
    ) -> list[EvidenceItem]:
        """
        依照情緒狀態篩選證據。
        """

        if self._is_empty_filter(sentiment):
            return list(evidence_items)

        selected_sentiment = self._normalize_text(sentiment)

        return [
            item
            for item in evidence_items
            if self._normalize_text(item.sentiment) == selected_sentiment
        ]

    def filter_by_keyword(
        self,
        evidence_items: list[EvidenceItem],
        keyword: str | None,
    ) -> list[EvidenceItem]:
        """
        依照關鍵字搜尋證據。

        搜尋範圍：
        - content
        - ai_summary
        - topic
        - author
        - platform
        """

        if not keyword:
            return list(evidence_items)

        normalized_keyword = keyword.strip().lower()

        if not normalized_keyword:
            return list(evidence_items)

        return [
            item
            for item in evidence_items
            if normalized_keyword in self._build_search_text(item)
        ]

    def sort(
        self,
        evidence_items: list[EvidenceItem],
        sort_by: str | None,
    ) -> list[EvidenceItem]:
        """
        依照指定條件排序證據。
        """

        if self._is_empty_filter(sort_by):
            return list(evidence_items)

        normalized_sort = self._normalize_text(sort_by)

        if normalized_sort in [
            "最新優先",
            "newest",
            "newest first",
            "published_time_desc",
        ]:
            return sorted(
                evidence_items,
                key=lambda item: self._safe_sort_value(item.published_time),
                reverse=True,
            )

        if normalized_sort in [
            "最舊優先",
            "oldest",
            "oldest first",
            "published_time_asc",
        ]:
            return sorted(
                evidence_items,
                key=lambda item: self._safe_sort_value(item.published_time),
            )

        if normalized_sort in [
            "互動高到低",
            "highest engagement",
            "engagement_desc",
        ]:
            return sorted(
                evidence_items,
                key=lambda item: self._safe_number(item.engagement),
                reverse=True,
            )

        if normalized_sort in [
            "互動低到高",
            "lowest engagement",
            "engagement_asc",
        ]:
            return sorted(
                evidence_items,
                key=lambda item: self._safe_number(item.engagement),
            )

        return list(evidence_items)

    def query_by_state(
        self,
        evidence_items: list[EvidenceItem],
        state,
    ) -> list[EvidenceItem]:
        """
        依照畫面目前的查詢條件取得證據。

        Query Engine 只讀取條件並回傳查詢結果，
        不負責畫面呈現或狀態管理。
        """

        results = list(evidence_items)

        results = self.filter_by_platform(
            results,
            getattr(state, "platform", None),
        )
        results = self.filter_by_topic(
            results,
            getattr(state, "topic", None),
        )
        results = self.filter_by_sentiment(
            results,
            getattr(state, "sentiment", None),
        )
        results = self.filter_by_keyword(
            results,
            getattr(state, "keyword", None),
        )
        results = self.sort(
            results,
            getattr(state, "sort_by", None),
        )

        return results

    def _build_search_text(self, item: EvidenceItem) -> str:
        """
        建立證據的關鍵字搜尋文字。
        """

        searchable_values = [
            getattr(item, "content", ""),
            getattr(item, "ai_summary", ""),
            getattr(item, "topic", ""),
            getattr(item, "author", ""),
            getattr(item, "platform", ""),
        ]

        return " ".join(
            self._normalize_text(value)
            for value in searchable_values
        )

    def _is_empty_filter(self, value: str | None) -> bool:
        """
        判斷篩選條件是否代表「不篩選」。
        """

        if value is None:
            return True

        normalized_value = self._normalize_text(value)

        return normalized_value in [
            "",
            "all",
            "全部",
            "不限",
        ]

    def _normalize_text(self, value) -> str:
        """
        將 Enum、None 或一般值轉成可比對文字。
        """

        if value is None:
            return ""

        if hasattr(value, "value"):
            return str(value.value).strip().lower()

        return str(value).strip().lower()

    def _safe_number(self, value) -> int:
        """
        將數值安全轉為整數，避免排序時中斷。
        """

        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def _safe_sort_value(self, value) -> str:
        """
        將排序值安全轉成文字。
        """

        if value is None:
            return ""

        return str(value)