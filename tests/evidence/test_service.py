from modules.evidence_center.service import EvidenceService


def main():
    service = EvidenceService()

    all_items = service.get_all_evidence()
    recent_items = service.get_recent_evidence(limit=2)
    negative_items = service.get_negative_evidence()
    positive_items = service.get_positive_evidence()

    platform_summary = service.get_platform_summary()
    sentiment_summary = service.get_sentiment_summary()
    topic_summary = service.get_topic_summary()

    first_item = all_items[0]
    found_item = service.get_evidence_by_id(first_item.evidence_id)

    facebook_items = service.get_evidence_by_platform("Facebook")
    topic_items = service.get_evidence_by_topic("腸胃敏感")

    print("All evidence count:", len(all_items))
    print("Recent evidence count:", len(recent_items))
    print("Negative evidence count:", len(negative_items))
    print("Positive evidence count:", len(positive_items))
    print("Platform summary:", platform_summary)
    print("Sentiment summary:", sentiment_summary)
    print("Topic summary:", topic_summary)
    print("Find by ID:", found_item.evidence_id if found_item else "Not found")
    print("Facebook evidence count:", len(facebook_items))
    print("Topic evidence count:", len(topic_items))

    assert len(all_items) > 0
    assert len(recent_items) == 2
    assert len(negative_items) >= 1
    assert len(positive_items) >= 1
    assert platform_summary.get("Facebook") == 1
    assert sentiment_summary.get("Positive") >= 1
    assert topic_summary.get("腸胃敏感") == 1
    assert found_item is not None
    assert len(facebook_items) == 1
    assert len(topic_items) == 1

    print("Evidence Service regression test passed.")


if __name__ == "__main__":
    main()