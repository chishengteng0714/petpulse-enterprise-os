from modules.platform.specification.enterprise_product_spec import (
    build_enterprise_product_spec,
)


class EnterpriseSpecificationService:
    """
    Enterprise Specification Service Golden Master

    提供 PetPulse Enterprise OS 產品規格的統一讀取入口。

    負責提供：
    - Product Information
    - Product Principles
    - Navigation
    - Workspace Specification

    GM-07 Final Product Audit：
    - 不改變 Runtime Behavior
    - 不新增 Architecture
    - 僅整理 Docstring、命名與可讀性
    """

    def __init__(self):
        self.spec = build_enterprise_product_spec()

    def get_product_spec(self):
        """
        取得完整產品規格。
        """

        return self.spec

    def get_product_name(self):
        """
        取得產品名稱。
        """

        return self.spec.name

    def get_product_version(self):
        """
        取得產品版本。
        """

        return self.spec.version

    def get_product_principles(self):
        """
        取得產品原則。
        """

        return self.spec.product_principles

    def get_design_principles(self):
        """
        取得設計原則。
        """

        return self.spec.design_principles

    def get_navigation(self):
        """
        取得產品導覽設定。
        """

        return self.spec.navigation

    def get_workspaces(self):
        """
        取得所有 Workspace 規格。
        """

        return self.spec.workspaces

    def get_workspace(self, workspace_key):
        """
        依照 Workspace Key 取得單一 Workspace 規格。
        """

        for workspace in self.spec.workspaces:
            if workspace.key == workspace_key:
                return workspace

        return None

    def get_workspace_sections(self, workspace_key):
        """
        取得 Workspace Sections，依 Priority 排序。
        """

        workspace = self.get_workspace(workspace_key)

        if workspace is None:
            return []

        return sorted(
            workspace.sections,
            key=lambda section: section.priority,
        )

    def get_workspace_ai_spec(self, workspace_key):
        """
        取得 Workspace AI Specification。
        """

        workspace = self.get_workspace(workspace_key)

        if workspace is None:
            return None

        return workspace.ai