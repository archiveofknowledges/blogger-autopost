import requests
from bs4 import BeautifulSoup

def fetch_posts(count=3, keywords=None):
    url = "https://arxiv.org/list/cs.LG/recent"  # 최근 머신러닝 분야 논문
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    entries = soup.find_all("dd")
    titles = soup.find_all("div", class_="list-title mathjax")
    abstracts = soup.find_all("p", class_="mathjax")

    for i in range(min(count, len(entries))):
        try:
            title = titles[i].text.replace("Title:", "").strip()
            summary = abstracts[i].text.strip()
            link_tag = entries[i].find_previous_sibling("dt").find("a", title="Abstract")
            link = f"https://arxiv.org{link_tag['href']}" if link_tag else "#"

            results.append({
                "title": title,
                "summary": summary,
                "year": "2025",
                "authors": [],
                "topics": ["machine learning"],
                "source": link,
                "category": "scholar_arxiv"
            })
        except Exception as e:
            print(f"[ERROR] arXiv parsing failed: {e}")
            continue

    print(f"📚 Collected {len(results)} papers from arXiv.")
    return results
