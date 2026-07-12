# PetPulse Enterprise OS

版本：v1.0 Golden Master

---

## 產品定位

PetPulse Enterprise OS 是一套 Enterprise Decision Operating System。

協助企業主管在最短時間內：

- 理解今日企業狀態
- 完成重要決策
- 推動後續工作執行

---

## 快速啟動

```bash
streamlit run app.py
```

---

## Golden Master 原則

目前版本為 Golden Master。

允許：

- Code Cleanup
- Product Language Cleanup
- Visual Consistency Audit
- Docstring Polish
- Readability Polish
- Bug Fix（不得影響 Runtime Behavior）

禁止：

- 新增 Runtime
- 新增 Engine
- 新增 Layer
- 新增 Domain
- 新增 Registry
- 新增 API
- 新增 Folder Architecture
- 新增功能

---

## 平台架構

PetPulse Enterprise OS 主要由以下工作區組成：

- Platform Layer
- Enterprise Home
- Evidence Center
- Platform Specification

平台統一入口：

```python
from modules.platform import render_platform
```

---

## Demo 流程

主管 Demo 建議順序：

1. 今日企業狀態
2. 今日待決策事項
3. 下一步工作入口
4. Evidence Center 證據查核

---

## 專案狀態

PetPulse Enterprise OS v1.0 Golden Master

Architecture：🔒 Permanent Frozen