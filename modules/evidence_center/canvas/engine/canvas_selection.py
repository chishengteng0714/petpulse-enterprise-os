from dataclasses import dataclass
from typing import Any


@dataclass
class CanvasSelectedObject:
    """
    Canvas Unified Selected Object

    Canvas 層唯一選取物件格式。

    不再讓 UI 分別判斷：
    - selected_node
    - selected_action
    - selected_flow
    - selected_evidence

    統一回傳：
    {
        "type": "...",
        "object": ...
    }
    """

    type: str | None = None
    object: Any | None = None

    def to_dict(self):
        return {
            "type": self.type,
            "object": self.object,
        }


class CanvasSelection:
    """
    Canvas Selection State

    負責管理 Canvas 上目前選取的單一物件。
    """

    def __init__(self):
        self.selected_type: str | None = None
        self.selected_object: Any | None = None

    def select(self, object_type: str, selected_object: Any):
        """
        選取任一 Canvas 物件。
        """

        self.selected_type = object_type
        self.selected_object = selected_object

    def clear(self):
        """
        清除目前選取物件。
        """

        self.selected_type = None
        self.selected_object = None

    def get_selected_object(self):
        """
        Unified Selected Object API
        """

        return CanvasSelectedObject(
            type=self.selected_type,
            object=self.selected_object,
        ).to_dict()

    def has_selection(self):
        return self.selected_object is not None

    def is_type(self, object_type: str):
        return self.selected_type == object_type