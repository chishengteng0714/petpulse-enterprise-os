from modules.evidence_center.service import EvidenceService


def main():
    service = EvidenceService()

    platforms = [
        "All",
        "Facebook",
        "Instagram",
        "PTT",
        "Google Review",
    ]

    print("========== Platform Filter Test ==========")

    for platform in platforms:

        if platform == "All":
            items = service.get_all_evidence()
        else:
            items = service.query_evidence(platform=platform)

        print(f"{platform:<15}: {len(items)} item(s)")

        if platform != "All":
            assert all(
                item.platform == platform
                for item in items
            )

    print("------------------------------------------")
    print("Platform Filter regression test passed.")


if __name__ == "__main__":
    main()