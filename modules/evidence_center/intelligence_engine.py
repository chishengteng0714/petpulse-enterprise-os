# modules/evidence_center/intelligence_engine.py

class EvidenceIntelligenceEngine:
    """
    Evidence Intelligence Layer

    將 Evidence 轉成初步洞察。

    GM-06 Final Schema Consistency Audit：
    - 使用 content 作為 Evidence 主要內容
    - 使用 ai_summary 作為摘要補充
    """

    def summarize(self, evidence: dict) -> str:
        if not evidence:
            return ""

        content = evidence.get("content", "")
        ai_summary = evidence.get("ai_summary", "")

        focus_text = ai_summary or content

        return f"此證據的核心內容集中在：{focus_text[:80]}..."

    def compare(self, e1: dict, e2: dict) -> dict:
        """
        產生比較結果。
        """

        if not e1 or not e2:
            return {"insight": "資料不足"}

        insight = []

        eng1 = e1.get("engagement", 0)
        eng2 = e2.get("engagement", 0)

        if eng1 > eng2:
            insight.append("A 的互動量高於 B，代表影響力較強")
        elif eng2 > eng1:
            insight.append("B 的互動量高於 A，代表擴散更強")
        else:
            insight.append("A 與 B 影響力相近")

        if e1.get("platform") != e2.get("platform"):
            insight.append("來源平台不同，可能代表不同族群")

        return {
            "insight": insight,
            "summary_a": self.summarize(e1),
            "summary_b": self.summarize(e2),
        }