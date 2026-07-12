from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EnterpriseIntelligenceDomain(str, Enum):
    EXECUTIVE_BRIEFING = "Executive Briefing"
    STRATEGY_PLANNING = "Strategy Planning"
    ENTERPRISE_AI = "Enterprise AI"
    RISK_ANALYSIS = "Risk Analysis"
    OPPORTUNITY_DISCOVERY = "Opportunity Discovery"
    CROSS_WORKSPACE = "Cross Workspace Intelligence"
    AGENT_RUNTIME = "Enterprise Agent Runtime"


@dataclass
class EnterpriseIntelligenceSignal:
    signal_id: str
    title: str
    description: str
    domain: EnterpriseIntelligenceDomain
    priority: str = "Medium"
    source: str = "Enterprise Intelligence Hub"
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EnterpriseIntelligenceSummary:
    title: str
    narrative: str
    key_points: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)


@dataclass
class EnterpriseIntelligenceHubState:
    status: str
    layer_name: str
    description: str
    domains: list[EnterpriseIntelligenceDomain]
    signals: list[EnterpriseIntelligenceSignal]
    summary: EnterpriseIntelligenceSummary
    runtime_context: dict[str, Any] = field(default_factory=dict)