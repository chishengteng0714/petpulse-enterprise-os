# PetPulse Enterprise OS

# Enterprise Design System

Version

v1.0 Golden Master

Status

🔒 Frozen

---

# Design Philosophy

PetPulse Enterprise OS

是一套

Enterprise Decision Operating System

不是 Dashboard。

所有設計都應該降低主管的認知負擔。

每一個元件都應回答：

主管現在需要知道什麼？

而不是：

系統有哪些資料？

---

# Product Experience Principles

所有 Workspace

遵守：

Executive First

Information First

Action First

Data Second

先回答決策。

再展示資料。

---

# Standard Workspace Layout

所有 Workspace

固定結構：

Header

↓

Executive Summary

↓

KPI

↓

Main Content

↓

Next Action

不得任意改變。

---

# Page Header

每頁：

```python
st.markdown("# 頁面名稱")
st.caption("頁面定位")
```

例如：

今日企業首頁

證據中心

企業工作區

---

# Executive Summary

位置：

Header 下方。

目的：

主管 10 秒內知道：

今日狀態

是否需要介入

決策信心

建議：

```python
with st.container(border=True):
```

---

# KPI

使用：

```python
st.metric(...)
```

每列：

4 個 KPI

保持一致。

避免：

不同頁面不同樣式。

---

# Card

所有資訊卡：

```python
with st.container(border=True):
```

禁止：

自訂大量 HTML Card。

---

# Columns

建議：

2 欄

```python
st.columns(2)
```

3 欄

```python
st.columns(3)
```

4 KPI

```python
st.columns(4)
```

避免：

超過四欄。

---

# Typography

頁面：

#

區塊：

##

卡片：

###

Caption：

說明

Label：

metric

保持一致。

---

# Divider

所有區塊：

```python
st.divider()
```

分隔。

避免：

大量空白。

---

# Theme

所有顏色：

Theme 控制。

Workspace

不得：

指定品牌色。

不得：

覆蓋 Theme。

---

# Buttons

Primary：

重要決策。

Secondary：

一般操作。

Danger：

避免使用。

---

# Tables

優先：

st.dataframe()

避免：

HTML Table。

---

# Status

建議使用：

健康

注意

可控

需追蹤

高風險

避免：

大量顏色表示。

優先文字。

---

# Product Language

全部：

繁體中文。

例如：

搜尋

平台

工作區

企業健康

證據

負向

正向

中立

排序

篩選

更新

避免英文。

---

# Empty State

沒有資料：

必須提供：

原因

下一步

例如：

目前沒有符合條件的證據。

請調整搜尋條件或時間範圍。

---

# Next Action

所有 Workspace

最後一區：

下一步行動。

說明：

主管完成閱讀後，

下一步去哪裡。

---

# Accessibility

避免：

過小文字

大量色彩

過多動畫

保持：

高可讀性。

---

# Enterprise UX Principles

任何頁面：

主管：

10 秒內

知道：

目前狀態

是否需要介入

下一步

這就是

PetPulse Enterprise UX。

---

# Golden Master Definition

符合：

一致性

可維護性

低認知負擔

Streamlit Native First

Theme First

Information First

即可視為：

PetPulse Enterprise Design System v1.0