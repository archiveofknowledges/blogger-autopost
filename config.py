from datetime import datetime

# 블로그 설정 (너의 블로그 주소 앞부분만 적기)
BLOG_ID = "archiveofknowledges"

# 카테고리별 포스팅 개수 및 키워드 설정
POST_SETTINGS = {
    "scholar": {
        "enabled": True,
        "count": 3,  # ← 테스트용으로 3개만 요청
        "keywords": ["AI"]  # ← 확실히 잘 나오는 키워드!
    },
    "economy": {
        "enabled": True,
        "count": 1,
        "countries": ["United States"]
    }
}

# 오늘 날짜 (포스트 제목에 들어감)
TODAY = datetime.today().strftime("%Y-%m-%d")
