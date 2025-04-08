import os
import requests
import json
from formatter import format_post

# Refresh Token을 사용하여 새로운 Access Token을 발급받는 함수
def get_new_access_token():
    refresh_token = os.getenv("REFRESH_TOKEN")  # GitHub Secrets에서 환경변수로 받아옴
    client_id = os.getenv("CLIENT_ID")           # GitHub Secrets에서 환경변수로 받아옴
    client_secret = os.getenv("CLIENT_SECRET")   # GitHub Secrets에서 환경변수로 받아옴

    # 디버깅: 환경변수 값 확인
    print(f"REFRESH_TOKEN: {refresh_token}")
    print(f"CLIENT_ID: {client_id}")
    print(f"CLIENT_SECRET: {client_secret}")

    if not refresh_token or not client_id or not client_secret:
        print("❌ Missing required credentials.")
        return None

    # Access Token 갱신을 위한 URL
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    # POST 요청을 보내서 새로운 Access Token을 받음
    response = requests.post(url, data=data)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("✅ New Access Token received!")
        return access_token
    else:
        print(f"❌ Failed to refresh token: {response.text}")
        return None

# Blogger에 포스트를 올리는 함수
def post_to_blogger(blog_id, title, content):
    # 새로운 Access Token을 발급받고 사용
    access_token = get_new_access_token()
    if not access_token:
        print("❌ No access token available.")
        return False

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

# 포스트를 가져오는 함수 (예시로 더미 데이터를 반환)
def fetch_posts(category, count=10, countries=None, keywords=None):
    # 이 부분은 실제로 데이터를 가져오는 로직으로 교체해야 해
    papers = [
        {"title": "Hide and Seek in Noise Labels: Noise-Robust Collaborative Active Learning with LLM-Powered Assistance", "abstract": "This paper explores..."},
        {"title": "Robustly identifying concepts introduced during chat fine-tuning using crosscoders", "abstract": "The research investigates..."},
        # 더 많은 논문들 추가
    ]
    return papers

# 전체 자동 포스팅 프로세스를 관리하는 함수
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
