class InvestigationBrain:
    """
    Investigation Brain v1
    開始具備「推論能力」
    """

    def generate_hypothesis(self, evidences: list) -> list:
        """
        從多筆 evidence 推論可能假設
        """

        if not evidences:
            return ["資料不足，無法生成假設"]

        hypotheses = []

        platforms = {e.get("platform") for e in evidences}

        if len(platforms) > 1:
            hypotheses.append("不同平台出現相似議題，可能是跨平台擴散事件")

        total_engagement = sum(e.get("engagement", 0) for e in evidences)

        if total_engagement > 1000:
            hypotheses.append("整體互動量偏高，可能存在 viral 傳播現象")

        if any("負面" in e.get("content", "") for e in evidences):
            hypotheses.append("可能存在負面情緒集中擴散")

        return hypotheses

    def detect_contradictions(self, e1, e2) -> list:
        """
        矛盾偵測
        """

        contradictions = []

        if not e1 or not e2:
            return ["資料不足"]

        if e1.get("sentiment") != e2.get("sentiment"):
            contradictions.append("情緒判斷不同，可能存在輿論分裂")

        if e1.get("platform") != e2.get("platform"):
            contradictions.append("來源平台不同，資訊視角可能不一致")

        if e1.get("engagement", 0) > e2.get("engagement", 0) * 2:
            contradictions.append("A 的擴散速度顯著高於 B")

        return contradictions