from dataclasses import dataclass
from typing import Literal


EvidencePlatform = Literal[
    "Facebook",
    "Instagram",
    "Threads",
    "PTT",
    "Dcard",
    "Forum",
    "Google Review",
    "News",
    "Blog",
]


EvidenceSentiment = Literal[
    "Positive",
    "Neutral",
    "Negative",
    "Mixed",
    "Unknown",
]


@dataclass
class EvidenceItem:
    """
    Evidence Item

    Evidence Center 的核心資料模型。

    每一筆 Evidence 都代表一個可追溯、可查核、可引用的公開來源訊號。

    GM-06 Final Product Audit：
    - 不新增欄位
    - 不改變資料結構
    - 保留既有 EvidenceItem schema
    - 強化命名語意與 Docstring 可讀性
    """

    evidence_id: str
    platform: EvidencePlatform
    author: str
    content: str
    ai_summary: str
    topic: str
    sentiment: EvidenceSentiment
    published_time: str
    engagement: int
    original_url: str