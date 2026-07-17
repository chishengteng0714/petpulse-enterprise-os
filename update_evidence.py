from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "evidence.json"

GOOGLE_NEWS_RSS_URL = "https://news.google.com/rss/search"

SEARCH_QUERY = '"寵物公園" OR "PetPark"'

MAX_ITEMS = 30

EXCLUDED_KEYWORDS = {
    "狗公園",
    "犬隻活動區",
    "遛狗",
    "毛孩放電",
    "親水設施",
    "公所",
    "市府",
    "議員",
    "工程",
    "啟用",
    "動土",
    "維護",
    "寵物友善公園",
    "寵物運動公園",
    "寵物活動公園",
}

POSITIVE_KEYWORDS = {
    "成長",
    "提升",
    "推出",
    "合作",
    "優惠",
    "獲獎",
    "創新",
    "開幕",
    "好評",
    "推薦",
    "人氣",
    "擴展",
}

NEGATIVE_KEYWORDS = {
    "爭議",
    "投訴",
    "下架",
    "違規",
    "缺貨",
    "負評",
    "風險",
    "虧損",
    "道歉",
    "召回",
    "問題",
    "糾紛",
}


def main() -> None:
    """
    擷取 Google News RSS，整理為 Evidence Center 可讀取的 JSON。
    """

    print("開始擷取 Google News RSS...")

    rss_xml = _download_google_news_rss()
    records = _parse_rss_items(rss_xml)
    evidence_items = _build_evidence_items(records)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Google News RSS",
        "query": SEARCH_QUERY,
        "evidence_items": evidence_items,
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"更新完成，共寫入 {len(evidence_items)} 筆新聞資料。")
    print(f"資料檔案：{OUTPUT_FILE}")


def _download_google_news_rss() -> bytes:
    """
    下載 Google News RSS。
    """

    params = urllib.parse.urlencode(
        {
            "q": SEARCH_QUERY,
            "hl": "zh-TW",
            "gl": "TW",
            "ceid": "TW:zh-Hant",
        }
    )

    url = f"{GOOGLE_NEWS_RSS_URL}?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/150.0 Safari/537.36"
            )
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=30,
        ) as response:
            return response.read()

    except Exception as exc:
        raise RuntimeError(
            f"Google News RSS 下載失敗：{exc}"
        ) from exc


def _parse_rss_items(
    rss_xml: bytes,
) -> list[dict[str, str]]:
    """
    解析 RSS item。
    """

    try:
        root = ET.fromstring(rss_xml)

    except ET.ParseError as exc:
        raise RuntimeError(
            f"RSS XML 解析失敗：{exc}"
        ) from exc

    records: list[dict[str, str]] = []

    for item in root.findall(".//item"):
        title = _element_text(item, "title")
        link = _element_text(item, "link")
        description = _element_text(item, "description")
        published_time = _element_text(item, "pubDate")

        source_element = item.find("source")
        source_name = ""

        if source_element is not None and source_element.text:
            source_name = source_element.text.strip()

        records.append(
            {
                "title": title,
                "link": link,
                "description": description,
                "published_time": published_time,
                "source_name": source_name,
            }
        )

    return records


def _build_evidence_items(
    records: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """
    將 RSS 資料整理為 EvidenceItem schema。
    """

    evidence_items: list[dict[str, Any]] = []
    seen_urls: set[str] = set()

    for record in records:
        title = _clean_text(record.get("title"))
        link = _clean_text(record.get("link"))
        description = _clean_html(record.get("description"))
        source_name = _clean_text(record.get("source_name"))

        if not title or not link:
            continue

        if link in seen_urls:
            continue

        if _is_noise_record(title, description):
            continue

        seen_urls.add(link)

        content = description or title
        combined_text = f"{title} {content}"

        evidence_items.append(
            {
                "evidence_id": _build_evidence_id(link),
                "platform": "News",
                "author": source_name or "Google News",
                "content": title,
                "ai_summary": content,
                "topic": _detect_topic(combined_text),
                "sentiment": _detect_sentiment(combined_text),
                "published_time": _format_published_time(
                    record.get("published_time")
                ),
                "engagement": 0,
                "original_url": link,
            }
        )

        if len(evidence_items) >= MAX_ITEMS:
            break

    evidence_items.sort(
        key=lambda item: item["published_time"],
        reverse=True,
    )

    return evidence_items


def _is_noise_record(
    title: str,
    description: str,
) -> bool:
    """
    排除與品牌「寵物公園」無關的同名公園或公共設施新聞。
    """

    combined_text = f"{title} {description}"

    return any(
        keyword in combined_text
        for keyword in EXCLUDED_KEYWORDS
    )


def _detect_sentiment(text: str) -> str:
    """
    使用簡易關鍵字規則判斷情緒。
    """

    positive_score = sum(
        1
        for keyword in POSITIVE_KEYWORDS
        if keyword in text
    )

    negative_score = sum(
        1
        for keyword in NEGATIVE_KEYWORDS
        if keyword in text
    )

    if positive_score > negative_score:
        return "Positive"

    if negative_score > positive_score:
        return "Negative"

    if positive_score and negative_score:
        return "Mixed"

    return "Neutral"


def _detect_topic(text: str) -> str:
    """
    使用關鍵字規則判斷新聞主題。
    """

    topic_rules = [
        (
            "促銷與優惠",
            {
                "優惠",
                "折扣",
                "回饋",
                "刷卡",
                "滿額",
                "贈品",
                "LINE Pay",
            },
        ),
        (
            "門市與展店",
            {
                "門市",
                "開幕",
                "展店",
                "據點",
                "旗艦店",
                "分店",
            },
        ),
        (
            "品牌與行銷",
            {
                "品牌",
                "行銷",
                "代言",
                "活動",
                "聯名",
                "合作",
            },
        ),
        (
            "產品與服務",
            {
                "商品",
                "產品",
                "服務",
                "飼料",
                "用品",
                "美容",
                "醫療",
            },
        ),
        (
            "企業營運",
            {
                "營收",
                "成長",
                "投資",
                "併購",
                "策略",
                "市場",
            },
        ),
        (
            "風險與爭議",
            {
                "爭議",
                "投訴",
                "下架",
                "違規",
                "召回",
                "道歉",
                "糾紛",
            },
        ),
    ]

    for topic, keywords in topic_rules:
        if any(keyword in text for keyword in keywords):
            return topic

    return "品牌新聞"


def _format_published_time(value: Any) -> str:
    """
    將 RSS 發布時間轉換為 Evidence Center 使用格式。
    """

    raw_value = _clean_text(value)

    if not raw_value:
        return ""

    try:
        parsed = parsedate_to_datetime(raw_value)

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        local_time = parsed.astimezone()

        return local_time.strftime("%Y-%m-%d %H:%M")

    except (TypeError, ValueError, OverflowError):
        return raw_value


def _build_evidence_id(url: str) -> str:
    """
    使用新聞網址建立穩定且唯一的 evidence_id。
    """

    digest = hashlib.sha256(
        url.encode("utf-8")
    ).hexdigest()[:16]

    return f"news_{digest}"


def _clean_html(value: Any) -> str:
    """
    移除 RSS description 裡的 HTML 標籤。
    """

    text = _clean_text(value)

    if not text:
        return ""

    text = unescape(text)

    text = re.sub(
        r"<[^>]+>",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def _clean_text(value: Any) -> str:
    """
    將任意值轉成乾淨文字。
    """

    if value is None:
        return ""

    return str(value).strip()


def _element_text(
    parent: ET.Element,
    tag_name: str,
) -> str:
    """
    安全取得 XML 子元素文字。
    """

    element = parent.find(tag_name)

    if element is None or element.text is None:
        return ""

    return element.text.strip()


if __name__ == "__main__":
    main()