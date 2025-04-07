def fetch_posts(count=2):
    insurance_topics = [
        "Best pet insurance plans in the US",
        "Top car insurance for young drivers",
        "Dental insurance options for 2025",
        "Lemonade vs HealthyPaws comparison",
        "Is travel insurance worth it in 2025?"
    ]

    posts = []
    for i in range(min(count, len(insurance_topics))):
        posts.append({
            "title": insurance_topics[i],
            "summary": f"This post explores: {insurance_topics[i]}. It compares available plans, costs, coverage, and benefits for U.S. users seeking practical insurance choices.",
            "source": "https://example.com",  # optional placeholder
            "topics": ["insurance", "finance", "consumer choice"],
            "category": "insurance"
        })

    return posts
