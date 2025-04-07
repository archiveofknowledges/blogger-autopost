from datetime import datetime

# 블로그 설정
BLOG_ID = "archiveofknowledges"  # blogspot 주소 앞부분

# 카테고리별 포스팅 개수 및 키워드 설정
POST_SETTINGS = {
    "scholar": {
        "enabled": True,
        "count": 10,
        "keywords": ["machine learning", "neuroscience", "climate change"]
    },
    "economy": {
        "enabled": True,
        "count": 1,
        "countries": ["United States"]
    }
}

# 오늘 날짜 (제목에 활용)
TODAY = datetime.today().strftime("%Y-%m-%d")
