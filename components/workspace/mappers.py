def map_topic_to_signal(topic):
    return {
        "title": topic.get("topic", "未知主題"),
        "description": "近期熱門討論主題",
        "status": "New",
        "source": "Topic Signal",
        "count": topic.get("count", 0),
    }


def map_competitor_to_feed_item(competitor):
    return {
        "title": competitor.get("name", "未知競品"),
        "description": competitor.get("summary", "尚未提供競品摘要。"),
        "status": competitor.get("status", "Watching"),
        "source": "Competitor Intelligence",
        "count": competitor.get("mentions", 0),
    }


def map_source_to_intelligence_item(source):
    sentiment = source.get("sentiment", "Neutral")

    if sentiment == "Positive":
        variant = "success"
    elif sentiment == "Negative":
        variant = "danger"
    else:
        variant = "default"

    engagement = source.get("engagement", 0)

    return {
        "platform": source.get("platform", "Unknown Source"),
        "title": source.get("title", "未命名來源訊號"),
        "description": source.get("summary", "尚未提供摘要。"),
        "topic": source.get("topic", "未分類"),
        "sentiment": sentiment,
        "engagement": engagement,
        "engagement_label": f"{engagement} interactions",
        "published_at": source.get("published_at", "Unknown"),
        "url": source.get("url", ""),
        "variant": variant,
    }


def map_sources_to_intelligence_items(sources):
    return [
        map_source_to_intelligence_item(source)
        for source in sources
    ]