import requests

def fetch_posts(count=5, keywords=["machine learning"]):
    results = []
    for keyword in keywords:
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={keyword}&limit={count}&fields=title,abstract,year,authors,url,topics"
        try:
            response = requests.get(url)
            data = response.json().get("data", [])
            for item in data:
                results.append({
                    "title": item.get("title", "Untitled"),
                    "summary": item.get("abstract", "No abstract available."),
                    "year": item.get("year"),
                    "authors": [a.get("name") for a in item.get("authors", [])],
                    "topics": [t.get("topic") for t in item.get("topics", [])],
                    "source": item.get("url"),
                    "category": "scholar"
                })
        except Exception as e:
            print(f"[ERROR] Scholar fetch failed: {e}")
    return results[:count]
