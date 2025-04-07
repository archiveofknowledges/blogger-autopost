from datetime import datetime

BLOG_ID = "archiveofknowledges"

POST_SETTINGS = {
    # 기존 Scholar 비활성화 (남겨둬도 됨)
    "scholar": {
        "enabled": False,
        "count": 3,
        "keywords": ["transformer"]
    },
    # ✅ 새로운 arXiv 기반 수집기 활성화
    "scholar_arxiv": {
        "enabled": True,
        "count": 3
    },
    "economy": {
        "enabled": True,
        "count": 1,
        "countries": ["United States"]
    }
}

TODAY = datetime.today().strftime("%Y-%m-%d")
