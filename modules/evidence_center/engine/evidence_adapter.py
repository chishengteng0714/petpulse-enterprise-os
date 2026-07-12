# modules/evidence_center/engine/evidence_adapter.py

from typing import Any

from modules.evidence_center.engine.models import EngineEvidence


class EvidenceAdapter:
    """
    Evidence Adapter

    將 EvidenceService / Repository 回傳的資料，
    轉成 Engine 層唯一使用的 EngineEvidence。

    GM-06 Final Schema Consistency Audit：
    - 使用 Golden Master Evidence Schema
    - content 作為 Evidence 主要內容
    - ai_summary 作為摘要補充
    - original_url 作為原始來源連結
    """

    def adapt_many(self, evidence_items: list[Any]) -> list[EngineEvidence]:
        return [
            self.adapt(item, index)
            for index, item in enumerate(evidence_items)
        ]

    def adapt(self, item: Any, index: int = 0) -> EngineEvidence:
        evidence_id = self._safe_get(item, "evidence_id", None)

        if evidence_id is None:
            evidence_id = self._safe_get(item, "id", None)

        if evidence_id is None:
            evidence_id = f"evidence_{index + 1}"

        content = self._safe_get(item, "content", f"Evidence {index + 1}")
        ai_summary = self._safe_get(item, "ai_summary", "")

        platform = self._format_value(
            self._safe_get(item, "platform", "Unknown")
        )
        topic = self._format_value(
            self._safe_get(item, "topic", "Unknown")
        )
        sentiment = self._format_value(
            self._safe_get(item, "sentiment", "Unknown")
        )

        engagement = self._safe_number(
            self._safe_get(item, "engagement", 0)
        )

        original_url = self._safe_get(item, "original_url", "")
        published_time = self._safe_get(item, "published_time", "")

        metadata = {
            "raw_index": index,
            "raw_type": type(item).__name__,
            "ai_summary": ai_summary,
            "original_url": original_url,
        }

        raw_metadata = self._safe_get(item, "metadata", None)

        if isinstance(raw_metadata, dict):
            metadata.update(raw_metadata)

        return EngineEvidence(
            evidence_id=str(evidence_id),
            title=str(content),
            content=str(content),
            platform=platform,
            topic=topic,
            sentiment=sentiment,
            engagement=engagement,
            source_url=str(original_url or ""),
            created_time=str(published_time or ""),
            metadata=metadata,
        )

    def _safe_get(self, item: Any, key: str, default: Any = None) -> Any:
        if isinstance(item, dict):
            return item.get(key, default)

        return getattr(item, key, default)

    def _safe_number(self, value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def _format_value(self, value: Any) -> str:
        if value is None:
            return "Unknown"

        if hasattr(value, "value"):
            return str(value.value)

        return str(value)