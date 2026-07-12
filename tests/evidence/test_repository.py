from modules.evidence_center.repository import EvidenceRepository


def main():
    repository = EvidenceRepository()

    all_items = repository.list_all()
    print("All evidence count:", len(all_items))

    facebook_items = repository.get_by_platform("Facebook")
    print("Facebook evidence count:", len(facebook_items))

    positive_items = repository.get_by_sentiment("Positive")
    print("Positive evidence count:", len(positive_items))

    topic_items = repository.get_by_topic("腸胃敏感")
    print("Topic evidence count:", len(topic_items))

    recent_items = repository.get_recent(limit=2)
    print("Recent evidence count:", len(recent_items))

    first_item = all_items[0]
    found_item = repository.get_by_id(first_item.evidence_id)

    print("Find by ID:", found_item.evidence_id if found_item else "Not found")

    assert len(all_items) > 0
    assert len(facebook_items) == 1
    assert len(positive_items) >= 1
    assert len(topic_items) == 1
    assert len(recent_items) == 2
    assert found_item is not None

    print("Evidence Repository regression test passed.")


if __name__ == "__main__":
    main()