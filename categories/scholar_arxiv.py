import feedparser

def fetch_posts(count=3, keywords=None):
    feed_url = "https://export.arxiv.org/rss/cs.LG"  # 머신러닝 분야
    feed = feedparser.parse(feed_url)

    results = []
    entries = feed.entries[:count]

    for entry in entries:
        try:
            results.append({
                "title": entry.title,
                "summary": entry.summary,
                "year": entry.published[:4],
                "authors": [],  # RSS에서는 추출 어려움
                "topics": ["machine learning"],
                "source": entry.link,
                "category": "scholar_arxiv"
            })
        except Exception as e:
            print(f"[ERROR] arXiv RSS parsing failed: {e}")
            continue

    print(f"📚 Collected {len(results)} papers from arXiv RSS.")
    return results
