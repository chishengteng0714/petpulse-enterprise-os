ENTERPRISE_INTELLIGENCE_HUB_ARCHITECTURE = {
    "layer": "Enterprise Intelligence Hub",
    "sprint": "Sprint D",
    "step": "Step 1",
    "status": "Foundation Ready",
    "purpose": (
        "Create the shared Enterprise Intelligence Layer used by Executive Briefing, "
        "Strategy Planning, Enterprise AI, Risk Analysis, Opportunity Discovery, "
        "Cross Workspace Intelligence, and future Enterprise Agent Runtime."
    ),
    "position": [
        "Evidence Center",
        "Runtime Engine",
        "Canvas Runtime",
        "Canvas Intelligence",
        "Enterprise Observability",
        "Enterprise Intelligence Hub",
        "Enterprise Agent Runtime",
    ],
    "modules": {
        "__init__.py": "Public exports for the Enterprise Intelligence Layer.",
        "models.py": "Shared domain models and intelligence contracts.",
        "service.py": "Single service boundary for Enterprise Intelligence Hub.",
        "architecture.py": "Architecture map and Sprint D foundation metadata.",
    },
    "upstream_dependencies": [
        "Evidence Runtime",
        "Canvas Runtime",
        "Canvas Intelligence Runtime",
        "Enterprise Observability Service",
    ],
    "future_capabilities": [
        "Executive Briefing",
        "Strategy Planning",
        "Multi-Agent Runtime",
        "Enterprise Copilot",
        "AI Decision Center",
        "Risk Analysis",
        "Opportunity Discovery",
        "Cross Workspace Intelligence",
    ],
    "principles": [
        "Maintainability",
        "Observability",
        "Testability",
        "Scalability",
        "Single Intelligence Layer",
        "Runtime First",
        "Presenter Ready",
    ],
}


def get_enterprise_intelligence_architecture():
    return ENTERPRISE_INTELLIGENCE_HUB_ARCHITECTURE