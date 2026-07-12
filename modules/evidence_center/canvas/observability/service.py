"""
Observability Service

Enterprise Observability Platform 的應用服務層。

此 Service 負責統一提供：

- Health Summary
- Technical Debt Registry
- Enterprise Observability Snapshot

Panel 不直接組裝底層資料，而是透過 Service 取得觀測結果。
"""

from modules.evidence_center.canvas.observability.health_summary import (
    build_observability_health_summary,
)
from modules.evidence_center.canvas.observability.models import (
    HealthStatus,
)
from modules.evidence_center.canvas.observability.technical_debt import (
    build_technical_debt_registry,
)


class ObservabilityService:
    """
    Canvas Observability Application Service

    職責：
    - 統一 Observability 資料入口
    - 隔離 Panel 與底層 Builder
    - 提供可測試、可擴充的 Enterprise Snapshot
    - 提供安全 fallback，避免 Observability 本身造成畫面崩潰
    """

    def __init__(self, runtime=None):
        self.runtime = runtime

    def get_health_summary(self):
        """
        取得 Canvas Runtime 健康摘要。
        """

        try:
            return build_observability_health_summary(self.runtime)
        except Exception as error:
            return self._build_health_summary_fallback(error)

    def get_technical_debt_registry(self):
        """
        取得 Observability Technical Debt Registry。
        """

        try:
            return build_technical_debt_registry(self.runtime)
        except Exception as error:
            return self._build_technical_debt_fallback(error)

    def get_enterprise_snapshot(self):
        """
        取得 Enterprise Observability Snapshot。

        給 Overview Panel、未來 Executive Briefing、
        Strategy Center 或 Agent Runtime 使用。
        """

        health_summary = self.get_health_summary()
        technical_debt = self.get_technical_debt_registry()

        return {
            "health_summary": health_summary,
            "technical_debt": technical_debt,
            "overall_status": health_summary.get(
                "overall_status",
                HealthStatus.UNKNOWN.value,
            ),
            "technical_debt_total": technical_debt.get("total", 0),
            "requires_attention": self.requires_attention(
                health_summary=health_summary,
                technical_debt=technical_debt,
            ),
            "service_status": self._resolve_service_status(
                health_summary=health_summary,
                technical_debt=technical_debt,
            ),
        }

    def requires_attention(self, health_summary=None, technical_debt=None):
        """
        判斷目前 Observability 是否需要處理。
        """

        health_summary = health_summary or self.get_health_summary()
        technical_debt = technical_debt or self.get_technical_debt_registry()

        overall_status = health_summary.get(
            "overall_status",
            HealthStatus.UNKNOWN.value,
        )

        if overall_status in [
            HealthStatus.CRITICAL.value,
            HealthStatus.FAILED.value,
            HealthStatus.ERROR.value,
            HealthStatus.UNAVAILABLE.value,
        ]:
            return True

        if technical_debt.get("critical", 0) > 0:
            return True

        if technical_debt.get("high", 0) > 0:
            return True

        return False

    def _resolve_service_status(self, health_summary, technical_debt):
        """
        判斷 Observability Service 自身狀態。
        """

        if health_summary.get("service_error"):
            return HealthStatus.ERROR.value

        if technical_debt.get("service_error"):
            return HealthStatus.ERROR.value

        return HealthStatus.HEALTHY.value

    def _build_health_summary_fallback(self, error):
        """
        Health Summary 失敗時的安全回傳。
        """

        return {
            "overall_status": HealthStatus.CRITICAL.value,
            "runtime_status": HealthStatus.UNKNOWN.value,
            "api_status": HealthStatus.UNKNOWN.value,
            "contract_status": HealthStatus.UNKNOWN.value,
            "performance_status": HealthStatus.UNKNOWN.value,
            "summary": "Observability health summary failed to build.",
            "metrics": {
                "nodes": 0,
                "edges": 0,
                "actions": 0,
                "flows": 0,
                "events": 0,
            },
            "details": {},
            "service_error": str(error),
        }

    def _build_technical_debt_fallback(self, error):
        """
        Technical Debt Registry 失敗時的安全回傳。
        """

        return {
            "total": 1,
            "critical": 1,
            "high": 0,
            "medium": 0,
            "low": 0,
            "items": [
                {
                    "category": "Observability Service",
                    "title": "Technical Debt Registry failed to build",
                    "severity": "Critical",
                    "description": "Observability Service 無法建立 Technical Debt Registry。",
                    "recommendation": "檢查 technical_debt.py、health_summary.py 與 Runtime 狀態。",
                    "error": str(error),
                }
            ],
            "service_error": str(error),
        }


def create_observability_service(runtime=None):
    """
    建立 ObservabilityService。
    """

    return ObservabilityService(runtime=runtime)