import os
import json
import datetime
import requests
import openai
import time
import random
import re
from google.oauth2 import service_account
from google.auth.transport.requests import Request

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

INDEXING_KEY_JSON = os.environ.get("INDEXING_KEY_JSON")
indexing_credentials = None
if INDEXING_KEY_JSON:
    indexing_credentials = service_account.Credentials.from_service_account_info(
        json.loads(INDEXING_KEY_JSON),
        scopes=["https://www.googleapis.com/auth/indexing"]
    )

def notify_google_indexing(url):
    if not indexing_credentials:
        print("❌ Missing INDEXING_KEY_JSON. Skipping indexing notification.")
        return

    indexing_endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {indexing_credentials.with_scopes(['https://www.googleapis.com/auth/indexing']).refresh(Request()).token}"
    }
    payload = {
        "url": url,
        "type": "URL_UPDATED"
    }
    response = requests.post(indexing_endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"🔎 Submitted to Google Indexing: {url}")
    else:
        print(f"❌ Indexing failed for {url}: {response.text}")

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

def rewrite_human_like(text):
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    rewritten = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if random.random() < 0.2:
            s = "You ever wonder about this? " + s.lower()
        elif random.random() < 0.3:
            s = "Honestly, " + s
        elif random.random() < 0.3:
            s = s + " Pretty cool, huh?"
        elif random.random() < 0.3:
            s = s.replace(" is ", " is kinda ")
        rewritten.append(s)

    paragraphs = []
    i = 0
    while i < len(rewritten):
        para_len = random.choice([1, 2, 3, 4])
        chunk = rewritten[i:i+para_len]
        if chunk:
            paragraphs.append(" ".join(chunk))
        i += para_len

    paragraphs.append("Source: based on community trends from Reddit and YouTube")
    return "\n\n".join(paragraphs)

def clean_markdown_syntax(text):
    text = re.sub(r"^### (.*)", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.*)", r"<h2>\1</h2>", text, flags=re.MULTILINE)
    text = re.sub(r"^# (.*)", r"<h1>\1</h1>", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
    text = re.sub(r"^- (.*)", r"<li>\1</li>", text, flags=re.MULTILINE)
    return text

def create_post(title, content, category, tags, code_block=None):
    access_token = get_access_token()
    if not access_token:
        print("❌ Cannot post without access token.")
        return

    image_url, photographer = fetch_unsplash_image(title)
    if image_url and photographer:
        image_html = f'<img src="{image_url}" alt="{title}" style="width:100%;max-width:720px;margin-bottom:20px;border-radius:8px;">\n<p style="font-size:0.9em;color:#888;">Photo by {photographer} on <a href="https://unsplash.com" target="_blank">Unsplash</a></p><br>'
        content = image_html + content

    if code_block:
        code_section = f'''
<style>
.copy-code-block {{ background: #f4f4f4; border: 1px solid #ccc; padding: 1em; border-radius: 6px; overflow-x: auto; font-size: 0.95em; line-height: 1.5; font-family: monospace; }}
.copy-button {{ position: absolute; right: 0; top: 0; background-color: #4CAF50; color: white; border: none; padding: 6px 12px; cursor: pointer; font-size: 0.9em; border-radius: 4px; }}
</style>
<h3>Copyable Code Example</h3>
<div style='position: relative; margin-top: 1em;'>
  <button onclick="copyCode(this)" class='copy-button'>Copy</button>
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
'''
        content += code_section

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    post_data = {"kind": "blogger#post", "title": title, "content": content, "labels": [category] + tags}
    response = requests.post(url, headers=headers, json=post_data)

    if response.status_code == 200:
        post_url = response.json()["url"]
        print(f"✅ Posted: {title}")
        log_post(title, category)
        notify_google_indexing(post_url)
    else:
        print(f"❌ Failed: {title} → {response.text}")

def format_post_content(content):
    cleaned = clean_markdown_syntax(content)
    paragraphs = [f"<p>{p.strip()}</p>" for p in cleaned.split("\n\n") if p.strip()]
    return "\n".join(paragraphs)

def main():
    print("🚀 Starting randomized daily auto-post")
    now = datetime.datetime.utcnow()
    if not (now.hour == 7 and now.minute >= 45 and now.minute < 50):
        print("⏳ Not within the 16:45–16:49 KST window. Skipping run.")
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
    delays = [0]
    for _ in range(1, len(post_generators)):
        delays.append(delays[-1] + random.randint(30, 180))

    start_time = time.time()

    for i, generator in enumerate(post_generators):
        if i > 0:
            delay_minutes = delays[i] - delays[i - 1]
            print(f"⏱ Waiting {delay_minutes} minutes...")
            time.sleep(delay_minutes * 60)

        try:
            post = generator()
            post["content"] = rewrite_human_like(post["content"])
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

    try:
        with open("post_log.json", "w", encoding="utf-8") as f:
            json.dump(post_log, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Failed to save post_log.json locally: {e}")

    send_email_report()

if __name__ == "__main__":
    main()
