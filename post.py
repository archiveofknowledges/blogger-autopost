import os
from formatter import format_post  # formatter에서 함수 호출

def fetch_posts(category, count=10, countries=None, keywords=None):
    # 여기에 arXiv 또는 경제 지표 등 데이터를 가져오는 코드 작성
    # 예시로 더미 데이터를 반환하는 코드
    papers = [
        {"title": "Hide and Seek in Noise Labels: Noise-Robust Collaborative Active Learning with LLM-Powered Assistance", "abstract": "This paper explores..."},
        {"title": "Robustly identifying concepts introduced during chat fine-tuning using crosscoders", "abstract": "The research investigates..."},
        # 여기에 다른 논문 추가
    ]
    return papers

def post_to_blogger(blog_id, title, content):
    # Blogger API를 통해 포스팅하는 함수 (앞서 설명한 대로)
    pass

def auto_post():
    categories = ['scholar_arxiv', 'economy', 'insurance', 'credit_cards']
    for category in categories:
        posts = fetch_posts(category)  # 데이터를 가져오는 부분
        for post in posts:
            title = post["title"]
            abstract = post["abstract"]

            # format_post를 통해 포스트 생성
            formatted_post = format_post(title, abstract, category=category, tags=["tag1", "tag2"], date="2025-04-08")
            
            if formatted_post:
                print(f"✅ Posting: {title}")
                post_to_blogger(blog_id="YOUR_BLOG_ID", title=formatted_post["title"], content=formatted_post["content"])
            else:
                print(f"❌ Failed to format post: {title}")

if __name__ == "__main__":
    auto_post()
