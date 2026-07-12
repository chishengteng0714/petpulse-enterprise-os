from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class HeroSpec:
    """
    Specification for the hero area of a workspace.
    """

    greeting: str
    title: str
    summary: str
    primary_action: Optional[str] = None
    secondary_action: Optional[str] = None


@dataclass
class SectionSpec:
    """
    Specification for a workspace content section.
    """

    key: str
    title: str
    description: str
    priority: int = 100


@dataclass
class NavigationItemSpec:
    """
    Specification for a platform navigation item.
    """

    key: str
    label: str
    description: str
    icon: str
    target: str
    status: str = "available"


@dataclass
class InteractionSpec:
    """
    Specification for a workspace interaction pattern.
    """

    trigger: str
    behavior: str
    result: str


@dataclass
class AISpec:
    """
    Specification for the AI role and capabilities of a workspace.
    """

    role: str
    description: str
    capabilities: List[str] = field(default_factory=list)


@dataclass
class WorkspaceSpec:
    """
    Product specification for a single workspace.
    """

    key: str
    name: str
    purpose: str
    user_goal: str
    hero: HeroSpec
    sections: List[SectionSpec]
    interactions: List[InteractionSpec] = field(default_factory=list)
    ai: Optional[AISpec] = None


@dataclass
class EnterpriseProductSpec:
    """
    Product specification for the enterprise platform.
    """

    name: str
    version: str
    product_principles: List[str]
    design_principles: List[str]
    navigation: List[NavigationItemSpec]
    workspaces: List[WorkspaceSpec]