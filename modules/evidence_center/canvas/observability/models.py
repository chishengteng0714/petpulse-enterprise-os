from dataclasses import asdict, dataclass, field
from enum import Enum


class HealthStatus(str, Enum):
    HEALTHY = "Healthy"
    DEGRADED = "Degraded"
    PARTIAL = "Partial"
    FAILED = "Failed"
    ERROR = "Error"
    CRITICAL = "Critical"
    UNAVAILABLE = "Unavailable"
    UNKNOWN = "Unknown"


class DebtSeverity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class RuntimeMetrics:
    nodes: int = 0
    edges: int = 0
    actions: int = 0
    flows: int = 0
    events: int = 0

    def to_dict(self):
        return asdict(self)


@dataclass
class HealthDetail:
    status: str = HealthStatus.UNKNOWN.value
    message: str = ""
    metrics: dict = field(default_factory=dict)
    available: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    coverage: int | None = None
    average_latency_ms: float | None = None
    results: list[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


@dataclass
class HealthSummary:
    overall_status: str = HealthStatus.UNKNOWN.value
    runtime_status: str = HealthStatus.UNKNOWN.value
    api_status: str = HealthStatus.UNKNOWN.value
    contract_status: str = HealthStatus.UNKNOWN.value
    performance_status: str = HealthStatus.UNKNOWN.value
    summary: str = ""
    metrics: dict = field(default_factory=dict)
    details: dict = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


@dataclass
class PerformanceCheckResult:
    method: str
    status: str
    latency_ms: float | None = None

    def to_dict(self):
        return asdict(self)


@dataclass
class TechnicalDebtItem:
    category: str
    title: str
    severity: str
    description: str
    recommendation: str

    def to_dict(self):
        return asdict(self)


@dataclass
class TechnicalDebtRegistry:
    total: int = 0
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    items: list[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


def build_technical_debt_registry_from_items(items):
    normalized_items = [
        item.to_dict() if hasattr(item, "to_dict") else item
        for item in items
    ]

    return TechnicalDebtRegistry(
        total=len(normalized_items),
        critical=len(
            [item for item in normalized_items if item.get("severity") == DebtSeverity.CRITICAL.value]
        ),
        high=len(
            [item for item in normalized_items if item.get("severity") == DebtSeverity.HIGH.value]
        ),
        medium=len(
            [item for item in normalized_items if item.get("severity") == DebtSeverity.MEDIUM.value]
        ),
        low=len(
            [item for item in normalized_items if item.get("severity") == DebtSeverity.LOW.value]
        ),
        items=normalized_items,
    )