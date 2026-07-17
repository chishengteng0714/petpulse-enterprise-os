import json
from pathlib import Path
from typing import Any

from modules.evidence_center.domain import EvidenceItem


DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "evidence.json"
)


def get_mock_evidence_items() -> list[EvidenceItem]:
    """
    Evidence Center 資料入口。

    執行原則：
    1. 優先讀取 data/evidence.json 的真實資料。
    2. 資料檔不存在、格式錯誤或內容為空時，回傳空清單。
    3. 不再提供 example-post 類型的示範來源網址。
    """

    return load_evidence_items()


def load_evidence_items() -> list[EvidenceItem]:
    """
    從 JSON 資料檔載入 EvidenceItem。
    """

    if not DATA_FILE.exists():
        return []

    try:
        raw_content = DATA_FILE.read_text(encoding="utf-8-sig")
        payload = json.loads(raw_content)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return []

    records = _extract_records(payload)
    evidence_items: list[EvidenceItem] = []

    for record in records:
        item = _build_evidence_item(record)

        if item is not None:
            evidence_items.append(item)

    return evidence_items


def _extract_records(payload: Any) -> list[dict]:
    """
    支援以下兩種 JSON 格式：

    1. 直接陣列
       [
           {...},
           {...}
       ]

    2. evidence_items 容器
       {
           "evidence_items": [
               {...},
               {...}
           ]
       }
    """

    if isinstance(payload, list):
        return [
            record
            for record in payload
            if isinstance(record, dict)
        ]

    if isinstance(payload, dict):
        records = payload.get("evidence_items", [])

        if isinstance(records, list):
            return [
                record
                for record in records
                if isinstance(record, dict)
            ]

    return []


def _build_evidence_item(
    record: dict,
) -> EvidenceItem | None:
    """
    將 JSON 紀錄轉換為 EvidenceItem。

    缺少必要欄位或網址不是正式 HTTP/HTTPS 網址時，
    該筆資料會被略過，避免 Evidence Center 出現失效來源。
    """

    evidence_id = _clean_text(record.get("evidence_id"))
    content = _clean_text(record.get("content"))
    original_url = _clean_text(record.get("original_url"))

    if not evidence_id:
        return None

    if not content:
        return None

    if not _is_valid_source_url(original_url):
        return None

    platform = _normalize_platform(record.get("platform"))
    sentiment = _normalize_sentiment(record.get("sentiment"))

    try:
        engagement = max(
            0,
            int(record.get("engagement", 0)),
        )
    except (TypeError, ValueError):
        engagement = 0

    return EvidenceItem(
        evidence_id=evidence_id,
        platform=platform,
        author=_clean_text(record.get("author")) or "未知來源",
        content=content,
        ai_summary=(
            _clean_text(record.get("ai_summary"))
            or content
        ),
        topic=_clean_text(record.get("topic")) or "未分類",
        sentiment=sentiment,
        published_time=(
            _clean_text(record.get("published_time"))
            or ""
        ),
        engagement=engagement,
        original_url=original_url,
    )


def _clean_text(value: Any) -> str:
    """
    將欄位轉為乾淨字串。
    """

    if value is None:
        return ""

    return str(value).strip()


def _is_valid_source_url(url: str) -> bool:
    """
    只允許正式 HTTP 或 HTTPS 來源網址，
    並排除舊版 example 示範網址。
    """

    normalized = url.lower()

    if not normalized.startswith(
        ("https://", "http://")
    ):
        return False

    blocked_patterns = (
        "example-post",
        "example-thread",
        "example-review",
        "example.com",
    )

    return not any(
        pattern in normalized
        for pattern in blocked_patterns
    )


def _normalize_platform(value: Any) -> str:
    """
    將來源平台限制在 EvidencePlatform 支援範圍。
    """

    platform = _clean_text(value)

    allowed_platforms = {
        "Facebook",
        "Instagram",
        "Threads",
        "PTT",
        "Dcard",
        "Forum",
        "Google Review",
        "News",
        "Blog",
    }

    if platform in allowed_platforms:
        return platform

    return "News"


def _normalize_sentiment(value: Any) -> str:
    """
    將情緒值限制在 EvidenceSentiment 支援範圍。
    """

    sentiment = _clean_text(value)

    allowed_sentiments = {
        "Positive",
        "Neutral",
        "Negative",
        "Mixed",
        "Unknown",
    }

    if sentiment in allowed_sentiments:
        return sentiment

    return "Unknown"