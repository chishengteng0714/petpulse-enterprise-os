from modules.platform.specification.models import (
    AISpec,
    EnterpriseProductSpec,
    HeroSpec,
    InteractionSpec,
    NavigationItemSpec,
    SectionSpec,
    WorkspaceSpec,
)


def build_enterprise_product_spec() -> EnterpriseProductSpec:
    """
    Enterprise Product Specification Golden Master

    定義 PetPulse Enterprise OS 的產品規格、資訊架構、
    工作區導覽與 AI 原生體驗原則。

    GM-07 Final Product Audit：
    - 統一產品語言
    - 保留既有 Specification Structure
    - 不新增 Runtime / Engine / Layer / Domain / Registry / API
    - 不改變 Runtime Behavior
    """

    return EnterpriseProductSpec(
        name="PetPulse Enterprise OS",
        version="1.0",
        product_principles=[
            "主管決策體驗優先",
            "AI 原生體驗",
            "證據驅動",
            "決策導向",
            "企業作業系統思維",
            "元件優先",
            "Runtime 整合",
        ],
        design_principles=[
            "資訊層級優先於視覺裝飾",
            "每個頁面都必須回答今日最重要的事",
            "每個洞察都必須能回到證據",
            "每個建議都必須指向下一步行動",
            "每個工作區都必須支援持續作業",
        ],
        navigation=[
            NavigationItemSpec(
                key="enterprise_home",
                label="今日企業首頁",
                description="主管快速掌握今日重點、風險、機會與下一步行動。",
                icon="🏠",
                target="enterprise_home",
            ),
            NavigationItemSpec(
                key="executive_workspace",
                label="企業工作區",
                description="檢視企業健康度、待決策事項與管理優先順序。",
                icon="📊",
                target="executive_workspace",
                status="planned",
            ),
            NavigationItemSpec(
                key="evidence_center",
                label="證據中心",
                description="集中管理市場、品牌與消費者證據，作為決策依據來源。",
                icon="📄",
                target="evidence_center",
            ),
            NavigationItemSpec(
                key="investigation_studio",
                label="深入調查室",
                description="針對重要議題進行結構化調查與決策準備。",
                icon="🕸️",
                target="investigation_studio",
                status="planned",
            ),
            NavigationItemSpec(
                key="enterprise_observability",
                label="營運觀察室",
                description="觀察 Runtime、API、Contract、效能與平台健康狀態。",
                icon="🩺",
                target="enterprise_observability",
            ),
        ],
        workspaces=[
            _build_enterprise_home_spec(),
            _build_executive_workspace_spec(),
            _build_evidence_center_spec(),
            _build_investigation_studio_spec(),
            _build_enterprise_observability_spec(),
        ],
    )


def _build_enterprise_home_spec() -> WorkspaceSpec:
    return WorkspaceSpec(
        key="enterprise_home",
        name="Enterprise Home",
        purpose="Daily operating entry point for the Enterprise OS.",
        user_goal="Understand what matters today and decide where to continue working.",
        hero=HeroSpec(
            greeting="Good Morning",
            title="Your Enterprise Intelligence Briefing is ready.",
            summary="A daily executive briefing that highlights priorities, risks, opportunities and recommended next actions.",
            primary_action="Continue Investigation",
            secondary_action="Review Evidence",
        ),
        sections=[
            SectionSpec(
                key="today_focus",
                title="Today's Focus",
                description="The most important operating context for today.",
                priority=1,
            ),
            SectionSpec(
                key="decision_feed",
                title="Decision Feed",
                description="A prioritized stream of risks, opportunities, evidence and AI recommendations.",
                priority=2,
            ),
            SectionSpec(
                key="timeline",
                title="Market Timeline",
                description="A time-based view of important signals and operating events.",
                priority=3,
            ),
            SectionSpec(
                key="workspace_launcher",
                title="Workspace Launcher",
                description="Continue working or open a recommended workspace.",
                priority=4,
            ),
        ],
        interactions=[
            InteractionSpec(
                trigger="Click priority signal",
                behavior="Open quick preview with evidence and recommended action.",
                result="User can continue into Evidence Center or Investigation Studio.",
            ),
            InteractionSpec(
                trigger="Click continue investigation",
                behavior="Resume the most recent active investigation.",
                result="User enters the relevant operating workspace.",
            ),
        ],
        ai=AISpec(
            role="Executive Copilot",
            description="Summarizes daily operating context and recommends the next best action.",
            capabilities=[
                "Summarize enterprise signals",
                "Prioritize risks and opportunities",
                "Explain recommendation rationale",
                "Suggest next workspace",
            ],
        ),
    )


def _build_executive_workspace_spec() -> WorkspaceSpec:
    return WorkspaceSpec(
        key="executive_workspace",
        name="Executive Workspace",
        purpose="High-level decision workspace for leadership review.",
        user_goal="Review business health, priorities and decisions requiring attention.",
        hero=HeroSpec(
            greeting="Executive Mode",
            title="Review today's operating priorities.",
            summary="A leadership workspace for business health, decision queues and executive recommendations.",
            primary_action="Open Decision Queue",
            secondary_action="Review Market Snapshot",
        ),
        sections=[
            SectionSpec("business_health", "Business Health", "Current enterprise operating health.", 1),
            SectionSpec("decision_queue", "Decision Queue", "Open decisions requiring executive attention.", 2),
            SectionSpec("executive_recommendations", "Executive Recommendations", "AI-supported recommendations.", 3),
            SectionSpec("recent_decisions", "Recent Decisions", "Recently reviewed or completed decisions.", 4),
        ],
        interactions=[
            InteractionSpec(
                trigger="Open decision",
                behavior="Show decision detail, evidence and options.",
                result="Executive can approve, reject or request investigation.",
            ),
        ],
        ai=AISpec(
            role="Executive Decision Advisor",
            description="Supports leadership decisions with summarized evidence and recommendation logic.",
            capabilities=[
                "Explain decision context",
                "Compare options",
                "Identify missing evidence",
                "Recommend next decision step",
            ],
        ),
    )


def _build_evidence_center_spec() -> WorkspaceSpec:
    return WorkspaceSpec(
        key="evidence_center",
        name="Evidence Center",
        purpose="Single Source of Truth for all evidence.",
        user_goal="Find, inspect and validate the original sources behind insights.",
        hero=HeroSpec(
            greeting="Evidence Mode",
            title="Trace every insight back to original evidence.",
            summary="Review source signals, evidence details, relationships and investigation context.",
            primary_action="Explore Evidence",
            secondary_action="Open Relationship Map",
        ),
        sections=[
            SectionSpec("evidence_explorer", "Evidence Explorer", "Browse and filter evidence.", 1),
            SectionSpec("evidence_detail", "Evidence Detail", "Inspect selected evidence.", 2),
            SectionSpec("relationship_map", "Relationship Map", "Understand relationships between signals.", 3),
            SectionSpec("evidence_timeline", "Evidence Timeline", "View evidence progression over time.", 4),
        ],
        interactions=[
            InteractionSpec(
                trigger="Select evidence",
                behavior="Update detail, relationship and recommendation panels.",
                result="User sees evidence context and possible next action.",
            ),
        ],
        ai=AISpec(
            role="Evidence Analyst",
            description="Explains evidence and connects it to risks, opportunities and investigations.",
            capabilities=[
                "Explain source meaning",
                "Detect related signals",
                "Summarize evidence clusters",
                "Recommend investigation paths",
            ],
        ),
    )


def _build_investigation_studio_spec() -> WorkspaceSpec:
    return WorkspaceSpec(
        key="investigation_studio",
        name="Investigation Studio",
        purpose="Structured workspace for investigation and decision preparation.",
        user_goal="Turn signals into investigation flows and actionable recommendations.",
        hero=HeroSpec(
            greeting="Investigation Mode",
            title="Build a structured investigation from market signals.",
            summary="Organize evidence, relationships, timelines, actions and decision flows.",
            primary_action="Start Investigation",
            secondary_action="Review Active Flows",
        ),
        sections=[
            SectionSpec("active_cases", "Active Cases", "Current investigations in progress.", 1),
            SectionSpec("investigation_canvas", "Investigation Canvas", "Graph and flow-based investigation workspace.", 2),
            SectionSpec("action_plan", "Action Plan", "Recommended actions and next steps.", 3),
            SectionSpec("decision_package", "Decision Package", "Prepared decision-ready summary.", 4),
        ],
        interactions=[
            InteractionSpec(
                trigger="Create investigation",
                behavior="Initialize investigation flow from selected evidence.",
                result="User can organize evidence into a structured case.",
            ),
        ],
        ai=AISpec(
            role="Investigation Copilot",
            description="Guides investigation structure, missing evidence checks and next action planning.",
            capabilities=[
                "Suggest investigation structure",
                "Find missing evidence",
                "Generate action plan",
                "Prepare decision package",
            ],
        ),
    )


def _build_enterprise_observability_spec() -> WorkspaceSpec:
    return WorkspaceSpec(
        key="enterprise_observability",
        name="Enterprise Observability",
        purpose="Monitor technical and architectural health of the Enterprise OS.",
        user_goal="Ensure runtime, API, contract, session and performance health remain stable.",
        hero=HeroSpec(
            greeting="Operations Mode",
            title="Monitor Enterprise OS health.",
            summary="Inspect runtime diagnostics, contract health, session snapshots and technical debt.",
            primary_action="Open Runtime Debug Center",
            secondary_action="Review Technical Debt",
        ),
        sections=[
            SectionSpec("runtime_health", "Runtime Health", "Runtime status and diagnostics.", 1),
            SectionSpec("api_health", "API Health", "Runtime API contract status.", 2),
            SectionSpec("performance_health", "Performance Health", "Performance and rendering signals.", 3),
            SectionSpec("technical_debt", "Technical Debt Registry", "Known maintainability risks.", 4),
        ],
        interactions=[
            InteractionSpec(
                trigger="Open health signal",
                behavior="Show diagnostic detail and recommended remediation.",
                result="User can identify runtime or architecture issues.",
            ),
        ],
        ai=AISpec(
            role="Observability Analyst",
            description="Explains platform health and suggests remediation priorities.",
            capabilities=[
                "Explain runtime issue",
                "Identify technical debt",
                "Summarize health status",
                "Recommend remediation priority",
            ],
        ),
    )