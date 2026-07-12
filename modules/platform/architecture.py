PLATFORM_ARCHITECTURE = {
    "layer": "Platform Layer",
    "sprint": "Sprint D",
    "step": "Platform Refactor Step 2",
    "status": "Foundation Ready",
    "purpose": (
        "Create the highest-level Platform Layer for PetPulse Enterprise OS v1.0. "
        "The Platform Layer owns shell, routing, workspace registry, and platform runtime."
    ),
    "principles": [
        "Platform First",
        "Runtime First",
        "Workspace Registry",
        "No Duplicate Entry Points",
        "Composable Workspaces",
        "Enterprise OS Ready",
    ],
    "modules": {
        "__init__.py": "Public exports for Platform Layer.",
        "architecture.py": "Platform architecture metadata.",
        "runtime.py": "Platform runtime state and session bridge.",
        "workspace_registry.py": "Central registry for all platform workspaces.",
        "router.py": "Workspace routing and active workspace resolution.",
        "shell.py": "Top-level platform shell renderer.",
    },
    "future_structure": [
        "platform/shell",
        "platform/runtime",
        "platform/navigation",
        "platform/layout",
        "platform/context",
        "platform/settings",
    ],
    "target_app_entry": "render_platform()",
}


def get_platform_architecture():
    return PLATFORM_ARCHITECTURE