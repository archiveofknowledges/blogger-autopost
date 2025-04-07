import datetime
import requests

def fetch_posts(count=1, countries=["United States"]):
    posts = []
    today = datetime.date.today().strftime("%Y-%m-%d")
    for country in countries:
        try:
            url = f"https://api.tradingeconomics.com/historical/country/{country.replace(' ', '%20')}?c=guest:guest&group=macro"
            response = requests.get(url)
            data = response.json()
            if not isinstance(data, list):
                continue
            latest = {}
            for item in data:
                category = item.get("Category")
                value = item.get("Value")
                latest[category] = value
            summary = f"Key economic indicators for {country} on {today}:\n"
            summary += "\n".join([f"- {k}: {v}" for k, v in list(latest.items())[:5]])
            posts.append({
                "title": f"{country} Economic Indicators ({today})",
                "summary": summary,
                "date": today,
                "source": "https://tradingeconomics.com",
                "category": "economy"
            })
        except Exception as e:
            print(f"[ERROR] Economy fetch failed: {e}")
    return posts[:count]
