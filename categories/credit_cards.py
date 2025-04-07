def fetch_posts(count=2):
    credit_card_topics = [
        "Best cashback credit cards in 2025",
        "Top travel rewards cards with no annual fee",
        "Student credit card comparison: Discover vs Chase",
        "How to build credit with secured cards",
        "Business credit cards for startups"
    ]

    posts = []
    for i in range(min(count, len(credit_card_topics))):
        posts.append({
            "title": credit_card_topics[i],
            "summary": f"This article analyzes: {credit_card_topics[i]}. It covers APR, annual fees, rewards programs, and eligibility to help US consumers choose the right card.",
            "source": "https://example.com",  # optional placeholder
            "topics": ["credit cards", "finance", "personal banking"],
            "category": "credit_cards"
        })

    return posts
