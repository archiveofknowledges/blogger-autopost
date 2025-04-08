import os
import datetime
import requests
import openai
import time
import random

from categories import scholar, economy, minecraft
from categories import html, css, javascript, python, react, nodejs

# ✅ 환경변수
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")
BLOG_ID = "2146078384292830084"

# ✅ Blogger Access Token 발급
def get_access_token():
    if not (CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN):
        print("❌ Missing CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN")
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
        print("✅ Access token received")
        return access_token
    else:
        print("❌ Failed to get access token:", response.text)
        return None

# ✅ Blogger 포스트 업로드
def create_post(title, content, category, tags, code_block=None):
    access_token = get_access_token()
    if not access_token:
        print("❌ Cannot post without access token.")
        return

    if code_block:
        content += f"""
<style>
.copy-code-block {{
  background: #f4f4f4;
  border: 1px solid #ccc;
  padding: 1em;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.95em;
  line-height: 1.5;
  font-family: monospace;
}}
.copy-button {{
  position: absolute;
  right: 0;
  top: 0;
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 0.9em;
  border-radius: 4px;
}}
</style>

<h3>Copyable Code Example</h3>
<div style='position: relative; margin-top: 1em;'>
  <button onclick=\"copyCode(this)\" class='copy-button'>Copy</button>
  <pre class='copy-code-block'>{code_block}</pre>
</div>

<script>
function copyCode(button) {{
  const code = button.nextElementSibling.innerText;
  navigator.clipboard.writeText(code).then(() => {{
    const original = button.innerText;
    button.innerText = "Copied!";
    setTimeout(() => button.innerText = original, 1500);
  }});
}}
</script>
"""

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
        print(f"✅ Posted: {title}")
    else:
        print(f"❌ Failed: {title} → {response.text}")

# ✅ main(): 무작위 순서 + 무작위 지연 간격 (KST 기준)
def main():
    print("🚀 Starting randomized daily auto-post")

    # 한국 기준 9시 (KST → UTC: -9시간)
    now = datetime.datetime.utcnow()
    if now.hour != 0:
        print("⏳ Not the scheduled UTC 00:00 (KST 09:00). Skipping run.")
        return

    post_generators = [
        scholar.generate_scholar_post,
        economy.generate_economy_post,
        minecraft.generate_minecraft_post,
        html.generate_html_post,
        css.generate_css_post,
        javascript.generate_javascript_post,
        python.generate_python_post,
        react.generate_react_post,
        nodejs.generate_nodejs_post
    ]

    random.shuffle(post_generators)  # 순서 섞기

    delays = sorted(random.sample(range(0, 180), len(post_generators)))  # 0~180분 중 랜덤 지연 (최대 3시간)

    for i, generator in enumerate(post_generators):
        if i > 0:
            delay_minutes = delays[i] - delays[i - 1]
            print(f"⏱ Waiting {delay_minutes} minutes...")
            time.sleep(delay_minutes * 60)

        try:
            post = generator()
            create_post(
                title=post["title"],
                content=post["content"],
                category=post["category"],
                tags=post["tags"],
                code_block=post.get("code")
            )
        except Exception as e:
            print(f"❌ Error posting from generator '{generator.__name__}':", e)

if __name__ == "__main__":
    main()
