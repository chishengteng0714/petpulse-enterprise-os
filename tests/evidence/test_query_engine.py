from modules.evidence_center.query_engine import EvidenceQueryEngine
from modules.evidence_center.repository import EvidenceRepository


def main():
    repository = EvidenceRepository()
    query_engine = EvidenceQueryEngine()

    items = repository.list_all()

    platform_results = query_engine.filter_by_platform(
        items,
        platform="Facebook",
    )

    topic_results = query_engine.filter_by_topic(
        items,
        topic="腸胃敏感",
    )

    sentiment_results = query_engine.filter_by_sentiment(
        items,
        sentiment="Positive",
    )

    keyword_results = query_engine.search(
        items,
        keyword="保健品",
    )

    sorted_results = query_engine.sort_by_engagement(items)

    combined_results = query_engine.query(
        items,
        platform="Instagram",
        topic="寵物保健品",
        sentiment="Positive",
        keyword="保健品",
        sort_by="Engagement",
    )

    all_results = query_engine.query(
        items,
        platform="All",
        topic="All",
        sentiment="All",
        keyword="",
        sort_by=None,
    )

    print("Platform filter count:", len(platform_results))
    print("Topic filter count:", len(topic_results))
    print("Sentiment filter count:", len(sentiment_results))
    print("Keyword search count:", len(keyword_results))
    print("Top engagement:", sorted_results[0].engagement)
    print("Combined query count:", len(combined_results))
    print("All query count:", len(all_results))

    assert len(items) > 0
    assert len(platform_results) == 1
    assert platform_results[0].platform == "Facebook"

    assert len(topic_results) == 1
    assert topic_results[0].topic == "腸胃敏感"

    assert len(sentiment_results) >= 1
    assert all(item.sentiment == "Positive" for item in sentiment_results)

    assert len(keyword_results) >= 1
    assert any("保健品" in item.content or "保健品" in item.ai_summary for item in keyword_results)

    assert sorted_results[0].engagement >= sorted_results[-1].engagement

    assert len(combined_results) == 1
    assert combined_results[0].platform == "Instagram"
    assert combined_results[0].topic == "寵物保健品"
    assert combined_results[0].sentiment == "Positive"

    assert len(all_results) == len(items)

    print("Evidence Query Engine regression test passed.")


if __name__ == "__main__":
    main()