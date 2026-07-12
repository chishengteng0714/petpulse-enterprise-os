import json
import csv
import os
from datetime import datetime

# 讀取分析結果
with open("data/analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

today = datetime.now().strftime("%Y-%m-%d")

positive = data.get("positive", 0)
neutral = data.get("neutral", 0)
negative = data.get("negative", 0)

risk_count = len(data.get("risks", []))

health = 100
health -= negative * 8
health -= risk_count * 3
health += positive * 2
health = max(0, min(100, health))

csv_file = "database/history.csv"

file_exists = os.path.exists(csv_file)

# 避免同一天重複寫入
if file_exists:
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        if len(reader) > 1:
            last_date = reader[-1][0]
            if last_date == today:
                print("今天已經紀錄過")
                exit()

with open(csv_file, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow([
            "date",
            "health",
            "positive",
            "neutral",
            "negative"
        ])

    writer.writerow([
        today,
        health,
        positive,
        neutral,
        negative
    ])

print("歷史資料已更新")