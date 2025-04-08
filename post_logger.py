import os
import datetime
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # GitHub Personal Access Token with gist scope

# ✅ 리포트 저장용 리스트
post_log = []

def log_post(title: str, category: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    post_log.append(f"- [{timestamp}] {title} ({category})")

def save_log_to_gist():
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN not found. Skipping log save.")
        return

    content = "\n".join(post_log)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"blogger-post-log-{today}.md"

    payload = {
        "description": f"Auto Blog Post Log - {today}",
        "public": False,
        "files": {
            filename: {"content": content}
        }
    }

    response = requests.post(
        "https://api.github.com/gists",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        json=payload
    )

    if response.status_code == 201:
        print(f"✅ Log saved to gist: {response.json()['html_url']}")
    else:
        print(f"❌ Failed to save gist: {response.status_code} - {response.text}")
