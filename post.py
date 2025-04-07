import os
import requests
import json
from formatter import format_post

def get_new_access_token():
    # 환경변수에서 Refresh Token을 불러옴
    refresh_token = os.getenv("REFRESH_TOKEN")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # 토큰 갱신을 위한 POST 요청
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("✅ New Access Token received!")
        return access_token
    else:
        print(f"❌ Failed to refresh token: {response.text}")
        return None

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
    # 새로운 Access Token을 갱신하여 받음
    access_token = get_new_access_token()
    if not access_token:
        print("❌ No access token available.")
        return False

    # Blogger API 요청 URL
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(f"✅ Successfully posted: {title}")
        return True
    else:
        print(f"❌ Failed to post: {title}")
        print(f"📬 Status code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        return False

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
