import os
import datetime
import requests
from categories import scholar

# ▶️ 필수: Blogger 인증 정보
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
BLOG_ID = "2146078384292830084"

# ▶️ OpenAI
import openai
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_access_token():
    if not (CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN):
        print("❌ 환경변수 누락: CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN")
        return None

    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("✅ Access token 발급 성공")
        return access_token
    else:
        print("❌ Access token 발급 실패:", response.text)
        return None

def generate_scholar_post():
    prompt = """
    You are an academic writing assistant. Write a detailed, well-structured academic blog post
    about a current topic in AI research. Format the content using HTML. Use <h2> for the title,
    <h3> for headings, and wrap each paragraph in <p> tags. Avoid Markdown formatting.

    Include sections: Introduction, Literature Review, Methodology, Results and Discussion, Conclusion, References.
    """
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    content = response.choices[0].message.content.strip()
    return {
        "title": "Exploring Recent Advances in AI Research",
        "content": content,
        "category": "scholar",
        "tags": ["AI", "Research", "Machine Learning", "Academic", "Deep Learning"]
    }

def create_post(title, content, category, tags):
    access_token = get_access_token()
    if not access_token:
        print("❌ access token 없음 → 포스팅 불가")
        return

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": [category] + tags
    }

    response = requests.post(url, headers=headers, json=post_data)
    if response.status_code == 200:
        print(f"✅ 성공적으로 게시됨: {title}")
    else:
        print(f"❌ 게시 실패: {title} → {response.text}")

def main():
    print("🚀 Scholar 카테고리 단일 포스트 테스트 시작")
    post = generate_scholar_post()
    create_post(
        title=post["title"],
        content=post["content"],
        category=post["category"],
        tags=post["tags"]
    )

if __name__ == "__main__":
    main()
