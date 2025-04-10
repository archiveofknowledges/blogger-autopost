import os
import datetime
import json
import requests

GIST_TOKEN = os.environ.get("GIST_TOKEN")  # GitHub Personal Access Token with gist scope

# ✅ 리포트 저장용 리스트
post_log = []

def log_post(title: str, category: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "title": title,
        "category": category
    }

    # 리스트에 저장 (gist용)
    post_log.append(f"- [{timestamp}] {title} ({category})")

    # JSON 파일에도 저장 (GitHub Artifact용)
    log_file = "post_log.json"
    try:
        existing = []
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.append(entry)
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
        print(f"📁 Saved log to local JSON: {log_file}")
    except Exception as e:
        print(f"❌ Failed to save log file: {e}")

def save_log_to_gist():
    if not GIST_TOKEN:
        print("❌ GIST_TOKEN not found. Skipping log save.")
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
        headers={"Authorization": f"Bearer {GIST_TOKEN}"},
        json=payload
    )

    if response.status_code == 201:
        print(f"✅ Log saved to gist: {response.json()['html_url']}")
    else:
        print(f"❌ Failed to save gist: {response.status_code} - {response.text}")
