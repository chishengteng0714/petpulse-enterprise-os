"""
Observability Technical Debt Registry

集中整理 Canvas Observability 發現的技術債：

- Missing API
- Degraded Contracts
- Slow Runtime API
- Empty Runtime Data
- Runtime Errors

此模組只負責資料整理，不負責 Streamlit UI。
"""

from modules.evidence_center.canvas.observability.health_summary import (
    build_observability_health_summary,
)
from modules.evidence_center.canvas.observability.models import (
    DebtSeverity,
    HealthStatus,
    TechnicalDebtItem,
    build_technical_debt_registry_from_items,
)


def build_technical_debt_registry(runtime):
    """
    建立 Observability Technical Debt Registry。
    """

    health_summary = build_observability_health_summary(runtime)

    debts = []

    debts.extend(_collect_runtime_debts(health_summary))
    debts.extend(_collect_api_debts(health_summary))
    debts.extend(_collect_contract_debts(health_summary))
    debts.extend(_collect_performance_debts(health_summary))

    return build_technical_debt_registry_from_items(debts).to_dict()


def _collect_runtime_debts(health_summary):
    debts = []

    runtime_detail = health_summary.get("details", {}).get("runtime", {})
    metrics = runtime_detail.get("metrics", {})

    if metrics.get("nodes", 0) == 0:
        debts.append(
            _build_debt(
                category="Runtime Data",
                title="Runtime nodes are empty",
                severity=DebtSeverity.HIGH.value,
                description="Canvas Runtime 目前沒有 Nodes，Graph / Canvas Layer 可能無法呈現有效內容。",
                recommendation="檢查 EvidenceAdapter、Graph Engine 與 Runtime 初始化流程。",
            )
        )

    if metrics.get("edges", 0) == 0:
        debts.append(
            _build_debt(
                category="Runtime Data",
                title="Runtime edges are empty",
                severity=DebtSeverity.MEDIUM.value,
                description="Canvas Runtime 目前沒有 Edges，Relationship / Graph Context 可能不完整。",
                recommendation="檢查 Graph Engine 是否正確產生 Evidence 關聯。",
            )
        )

    if metrics.get("actions", 0) == 0:
        debts.append(
            _build_debt(
                category="Runtime Data",
                title="Runtime actions are empty",
                severity=DebtSeverity.MEDIUM.value,
                description="Canvas Runtime 目前沒有 Actions，Action Queue 或 Decision Layer 可能缺少可執行建議。",
                recommendation="檢查 Action Engine 與 Runtime API get_actions()。",
            )
        )

    if metrics.get("flows", 0) == 0:
        debts.append(
            _build_debt(
                category="Runtime Data",
                title="Runtime flows are empty",
                severity=DebtSeverity.LOW.value,
                description="Canvas Runtime 目前沒有 Flows，Flow Engine 可能尚未提供可觀測資料。",
                recommendation="檢查 Flow Engine 是否已有輸出，或確認目前 Sprint 是否尚未啟用 Flow。",
            )
        )

    return debts


def _collect_api_debts(health_summary):
    debts = []

    api_detail = health_summary.get("details", {}).get("api", {})
    missing = api_detail.get("missing", [])

    for method_name in missing:
        debts.append(
            _build_debt(
                category="Runtime API",
                title=f"Missing Runtime API：{method_name}",
                severity=DebtSeverity.HIGH.value,
                description=f"Canvas Runtime 缺少必要 API：{method_name}。",
                recommendation="補齊 Runtime API，或調整 API Contract 定義。",
            )
        )

    return debts


def _collect_contract_debts(health_summary):
    debts = []

    contract_detail = health_summary.get("details", {}).get("contract", {})
    missing = contract_detail.get("missing", [])

    for method_name in missing:
        debts.append(
            _build_debt(
                category="Runtime Contract",
                title=f"Contract method missing：{method_name}",
                severity=DebtSeverity.MEDIUM.value,
                description=f"Enterprise Runtime Contract 尚未涵蓋或尚未實作：{method_name}。",
                recommendation="確認此方法是否為正式 Contract；若是，請在 Runtime 中補上。",
            )
        )

    return debts


def _collect_performance_debts(health_summary):
    debts = []

    performance_detail = health_summary.get("details", {}).get("performance", {})
    results = performance_detail.get("results", [])

    for result in results:
        method_name = result.get("method")
        status = result.get("status")
        latency_ms = result.get("latency_ms")

        if status == HealthStatus.ERROR.value:
            debts.append(
                _build_debt(
                    category="Performance",
                    title=f"Runtime API error：{method_name}",
                    severity=DebtSeverity.CRITICAL.value,
                    description=f"Runtime API {method_name} 執行時發生錯誤。",
                    recommendation="檢查該 API 的例外處理與 Runtime 狀態依賴。",
                )
            )

        elif status == HealthStatus.UNAVAILABLE.value:
            debts.append(
                _build_debt(
                    category="Performance",
                    title=f"Runtime API unavailable：{method_name}",
                    severity=DebtSeverity.HIGH.value,
                    description=f"Runtime API {method_name} 不存在或不可呼叫。",
                    recommendation="補齊 API 或從 Performance Check 移除此方法。",
                )
            )

        elif isinstance(latency_ms, (int, float)) and latency_ms >= 200:
            debts.append(
                _build_debt(
                    category="Performance",
                    title=f"Slow Runtime API：{method_name}",
                    severity=DebtSeverity.MEDIUM.value,
                    description=f"Runtime API {method_name} 耗時 {latency_ms} ms，可能影響 Debug Center 體感速度。",
                    recommendation="檢查資料量、重複計算、Presenter 或 Engine 是否需要快取。",
                )
            )

    return debts


def _build_debt(category, title, severity, description, recommendation):
    return TechnicalDebtItem(
        category=category,
        title=title,
        severity=severity,
        description=description,
        recommendation=recommendation,
    )