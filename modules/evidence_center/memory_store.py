# modules/evidence_center/memory_store.py

class EvidenceMemoryStore:
    """
    Investigation Memory Layer

    記錄使用者在 Evidence Center 的選取與比較歷程。

    GM-06 Final Schema Consistency Audit：
    使用 Golden Master Evidence Schema。
    """

    def __init__(self):
        self.selected_history = []
        self.compare_history = []

    def add_selection(self, evidence):
        if not evidence:
            return

        self.selected_history.append(
            {
                "id": evidence.get("evidence_id") or evidence.get("id"),
                "content": evidence.get("content"),
                "timestamp": None,
            }
        )

    def add_compare(self, e1, e2):
        if not e1 or not e2:
            return

        self.compare_history.append(
            {
                "a": e1.get("evidence_id") or e1.get("id"),
                "b": e2.get("evidence_id") or e2.get("id"),
            }
        )

    def get_recent(self, limit=5):
        return self.selected_history[-limit:]