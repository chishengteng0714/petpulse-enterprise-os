from modules.evidence_center.domain import EvidenceItem


def get_mock_evidence_items() -> list[EvidenceItem]:
    """
    Evidence Center Mock Store

    提供 Evidence Center Golden Master 展示用資料。

    GM-06 Final Product Audit：
    - 不新增功能
    - 不改變 Architecture
    - 保留既有 Mock Store 責任
    - 對齊 EvidenceItem schema
    - 清除 GM-05 Demo Audit 殘留說明
    """

    return [
        EvidenceItem(
            evidence_id="ev_fb_001",
            platform="Facebook",
            author="寵物社團使用者",
            content="最近很多人討論狗狗腸胃敏感，尤其換飼料後軟便的狀況變多。",
            ai_summary="Facebook 社團出現飼料轉換與腸胃敏感相關討論。",
            topic="腸胃敏感",
            sentiment="Negative",
            published_time="2026-07-03 09:20",
            engagement=128,
            original_url="https://facebook.com/example-post",
        ),
        EvidenceItem(
            evidence_id="ev_ig_001",
            platform="Instagram",
            author="pet_lifestyle_tw",
            content="分享一款外出攜帶方便的寵物保健品，很多飼主留言詢問成分。",
            ai_summary="Instagram 內容顯示保健品攜帶便利性受到關注。",
            topic="寵物保健品",
            sentiment="Positive",
            published_time="2026-07-03 10:45",
            engagement=356,
            original_url="https://instagram.com/example-post",
        ),
        EvidenceItem(
            evidence_id="ev_threads_001",
            platform="Threads",
            author="毛孩生活觀察",
            content="最近看到不少人分享毛孩保健品日常，大家比較在意成分透明跟吃起來方不方便。",
            ai_summary="Threads 討論顯示成分透明與使用便利性是保健品關注重點。",
            topic="成分透明",
            sentiment="Positive",
            published_time="2026-07-03 12:05",
            engagement=214,
            original_url="https://threads.net/example-post",
        ),
        EvidenceItem(
            evidence_id="ev_dcard_001",
            platform="Dcard",
            author="寵物版使用者",
            content="家裡老狗最近開始吃關節保健，想問有沒有比較不會踩雷、價格也合理的品牌。",
            ai_summary="Dcard 使用者對高齡犬關節保健品有價格與品牌信任需求。",
            topic="高齡犬照護",
            sentiment="Neutral",
            published_time="2026-07-03 13:30",
            engagement=87,
            original_url="https://dcard.tw/example-post",
        ),
        EvidenceItem(
            evidence_id="ev_forum_001",
            platform="Forum",
            author="寵物用品討論使用者",
            content="這次比較幾款寵物營養補充品，大家最常問的是成分來源與適口性。",
            ai_summary="論壇討論顯示成分來源與適口性是高互動討論重點。",
            topic="產品開箱",
            sentiment="Positive",
            published_time="2026-07-03 14:10",
            engagement=492,
            original_url="https://forum.example.com/example-thread",
        ),
        EvidenceItem(
            evidence_id="ev_forum_002",
            platform="Forum",
            author="討論區使用者",
            content="想找寵物保健品長期吃的心得，有沒有品牌穩定、價格不要太高的選擇？",
            ai_summary="論壇討論顯示消費者重視長期使用心得、品牌穩定度與價格合理性。",
            topic="品牌信任",
            sentiment="Neutral",
            published_time="2026-07-03 15:25",
            engagement=63,
            original_url="https://forum.example.com/example-review",
        ),
        EvidenceItem(
            evidence_id="ev_ptt_001",
            platform="PTT",
            author="匿名使用者",
            content="有沒有推薦比較適合高齡犬的關節保健品牌？價格不要太誇張。",
            ai_summary="PTT 使用者對高齡犬關節保健品有明確需求。",
            topic="高齡犬照護",
            sentiment="Neutral",
            published_time="2026-07-03 11:10",
            engagement=42,
            original_url="https://ptt.cc/example-post",
        ),
        EvidenceItem(
            evidence_id="ev_review_001",
            platform="Google Review",
            author="門市顧客",
            content="店員很親切，也會提醒不同年齡狗狗適合的營養補充品。",
            ai_summary="Google Review 顯示門市服務與營養建議形成正面體驗。",
            topic="門市服務",
            sentiment="Positive",
            published_time="2026-07-02 18:30",
            engagement=5,
            original_url="https://google.com/maps/example-review",
        ),
    ]