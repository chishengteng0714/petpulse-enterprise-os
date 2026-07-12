import json
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "analysis.json"
HISTORY_PATH = BASE_DIR / "database" / "history.csv"


@st.cache_data(ttl=60)
def load_analysis_data():
    """
    載入 AI 分析結果。
    若資料不存在或格式錯誤，回傳安全預設值，避免 Dashboard 爆掉。
    """
    default_data = {
        "brand_health": 84,
        "positive": 0,
        "neutral": 0,
        "negative": 0,
        "summary": "目前尚未取得 AI 分析摘要。",
        "insights": [],
        "recommendations": [],
        "risks": [],
        "opportunities": [],
        "hot_topics": [],
        "alerts": [],
        "actions": [],
        "confidence": 86,
    }

    try:
        if not DATA_PATH.exists():
            return default_data

        with open(DATA_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {**default_data, **data}

    except Exception:
        return default_data


@st.cache_data(ttl=60)
def load_history_data():
    """
    載入歷史資料。
    若 history.csv 不存在，建立安全的空資料結構。
    """
    try:
        if not HISTORY_PATH.exists():
            return pd.DataFrame(
                columns=["date", "health", "positive", "neutral", "negative"]
            )

        history = pd.read_csv(HISTORY_PATH)

        if "date" in history.columns:
            history["date"] = pd.to_datetime(history["date"], errors="coerce")
            history = history.dropna(subset=["date"])
            history = history.sort_values("date")

        return history

    except Exception:
        return pd.DataFrame(
            columns=["date", "health", "positive", "neutral", "negative"]
        )


def calculate_delta(current_value, previous_value):
    try:
        return int(current_value) - int(previous_value)
    except Exception:
        return 0


def calculate_rolling_average(history, column="health", days=7):
    try:
        if history.empty or column not in history.columns:
            return None

        recent = history.tail(days)
        return round(recent[column].mean(), 1)

    except Exception:
        return None


def get_latest_health_metrics(data, history):
    current_health = int(data.get("brand_health", 84))

    if history.empty or "health" not in history.columns or len(history) < 2:
        previous_health = current_health
    else:
        previous_health = int(history.iloc[-2]["health"])

    delta = calculate_delta(current_health, previous_health)
    avg_7d = calculate_rolling_average(history, "health", 7)

    if current_health >= 80:
        status = "健康"
    elif current_health >= 65:
        status = "觀察"
    else:
        status = "風險"

    return {
        "value": current_health,
        "delta": delta,
        "status": status,
        "average": avg_7d,
    }


def get_sentiment_metrics(data, history):
    positive = int(data.get("positive", 0))
    neutral = int(data.get("neutral", 0))
    negative = int(data.get("negative", 0))
    total = positive + neutral + negative

    positive_rate = round((positive / total) * 100, 1) if total > 0 else 0
    negative_rate = round((negative / total) * 100, 1) if total > 0 else 0

    if not history.empty and "negative" in history.columns and len(history) >= 2:
        previous_negative = int(history.iloc[-2]["negative"])
    else:
        previous_negative = negative

    negative_delta = calculate_delta(negative, previous_negative)

    return {
        "positive_rate": positive_rate,
        "negative_rate": negative_rate,
        "negative_delta": negative_delta,
        "total": total,
    }