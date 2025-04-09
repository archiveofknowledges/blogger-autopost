import os
import datetime
import requests
import openai
import time
import random

from categories import scholar, economy, minecraft
from categories import html, css, javascript, python, react, nodejs, health
from post_logger import log_post, save_log_to_gist
from email_reporter import send_email_report

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")
UNSPLASH_KEY = os.environ.get("UNSPLASH_KEY")
BLOG_ID = "2146078384292830084"

# ✅ Unsplash 썸네일 이미지 검색

def fetch_unsplash_image(keyword):
    if not UNSPLASH_KEY:
        print("❌ UNSPLASH_KEY missing")
        return None, None

    url = "https://api.unsplash.com/photos/random"
    params = {
        "query": keyword,
        "orientation": "landscape",
        "client_id": UNSPLASH_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()["urls"]["regular"], response.json()["user"]["name"]
        else:
            print("❌ Unsplash fetch failed:", response.text)
            return None, None
    except Exception as e:
        print(f"❌ Unsplash exception: {e}")
        return None, None

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

    # ✅ Unsplash 이미지 삽입
    image_url, photographer = fetch_unsplash_image(title)
    if image_url and photographer:
        image_html = f"""
<img src="{image_url}" alt="{title}" style="width:100%;max-width:720px;margin-bottom:20px;border-radius:8px;">
<p style="font-size:0.9em;color:#888;">Photo by {photographer} on <a href="https://unsplash.com" target="_blank">Unsplash</a></p><br>
"""
        content = image_html + content

    # ✅ 코드 블록 삽입
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
        log_post(title, category)
    else:
        print(f"❌ Failed: {title} → {response.text}")

# ✅ main(): 무작위 순서 + 무작위 지연 간격 (KST 기준)
def main():
    print("🚀 Starting randomized daily auto-post")

    now = datetime.datetime.utcnow()
    if not (now.hour == 0 and now.minute <= 10):
        print("⏳ Not close enough to 00:00 UTC. Skipping run.")
        return

    post_generators = []
    categories = [scholar, economy, minecraft, html, css, javascript, python, react, nodejs, health]

    for category in categories:
        count = random.randint(1, 3) if category in [scholar, python, economy, health] else 1
        generator = (
            category.generate_health_post if category == health
            else category.generate_scholar_post if category == scholar
            else category.generate_economy_post if category == economy
            else category.generate_python_post if category == python
            else category.generate_minecraft_post if category == minecraft
            else category.generate_html_post if category == html
            else category.generate_css_post if category == css
            else category.generate_javascript_post if category == javascript
            else category.generate_react_post if category == react
            else category.generate_nodejs_post
        )
        post_generators.extend([generator] * count)

    random.shuffle(post_generators)
    delays = sorted(random.sample(range(30, 180), len(post_generators)))
    start_time = time.time()

    for i, generator in enumerate(post_generators):
        if i > 0:
            delay_minutes = delays[i] - delays[i - 1]
            print(f"⏱ Waiting {delay_minutes} minutes...")
            time.sleep(delay_minutes * 60)

        try:
            post = generator()
            formatted_content = format_post_content(post["content"])
            create_post(
                title=post["title"],
                content=formatted_content,
                category=post["category"],
                tags=post["tags"],
                code_block=post.get("code")
            )
        except Exception as e:
            print(f"❌ Error posting from generator '{generator.__name__}':", e)

        if time.time() - start_time > 86400:
            print("❌ Exceeded 24-hour limit. Exiting...")
            break

    save_log_to_gist()
    send_email_report()

def format_post_content(content):
    content = content.replace("\n", "<br>")
    content = "<p>" + content.replace("<br><br>", "</p><p>") + "</p>"
    return content

if __name__ == "__main__":
    main()
