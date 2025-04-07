CONFIG = {
    "TIMEZONE": "Asia/Seoul",
    "POST_TIME_HOUR": 9,
    "POST_TIME_MINUTE": 0,

    "BLOG_ID": "archiveofknowledges",  # Blogger 주소: archiveofknowledges.blogspot.com

    "CATEGORIES": {
        "scholar_arxiv": {"count": 10},         # 학술 정보 (논문)
        "economy": {"count": 1, "countries": ["United States"]},  # 경제 지표
        "insurance": {"count": 1},              # 수익형: 보험 추천
        "credit_cards": {"count": 1},           # 수익형: 신용카드 추천
    },

    "OPENAI_MODEL": "gpt-3.5-turbo",  # 또는 gpt-4-turbo (활성화되었을 경우)
}
