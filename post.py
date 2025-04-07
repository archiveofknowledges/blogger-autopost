import importlib
from config import POST_SETTINGS, BLOG_ID
from formatter import format_post
import os
import json
import requests

def get_access_token():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise Exception("CLIENT_ID, CLIENT_SECRET, or REFRESH_TOKEN not found in environment variables.")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")
    
    return response.json().get("access_token")

def post_to_blogger(blog_id, access_token, title, content, labels=[], category=None):
    url = f"https://www.googleapis.com/blogger/v3/blogs/byurl?url=https://{blog_id}.blogspot.com"
    blog_info = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}).json()
    blog_id = blog_info.get("id")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": labels
    }

    post_url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    response = requests.post(post_url, headers=headers, data=json.dumps(post_data))

    if response.status_code in [200, 201]:
        print(f"✅ Posted: {title}")
    else:
        print(f"\n❌ Failed to post: {title}")
        print(f"📬 Status code: {response.status_code}")
        print(f"📄 Response: {response.text}\n")

if __name__ == "__main__":
    print("🚀 Starting auto-posting...")

    access_token = get_access_token()

    for category, options in POST_SETTINGS.items():
        if not options.get("enabled", False):
            continue

        try:
            module_path = f"categories.{category}"
            module = importlib.import_module(module_path)

            fetch_func = getattr(module, "fetch_posts", None)
            if not fetch_func:
                print(f"⚠️ Skipping: No fetch_posts function in {module_path}")
                continue

            fetch_args = {"count": options.get("count", 1)}
            if "keywords" in options:
                fetch_args["keywords"] = options["keywords"]
            elif "countries" in options:
                fetch_args["countries"] = options["countries"]

            print(f"\n📚 Fetching posts from category: {category}")
            print(f"📄 Fetch args: {fetch_args}")

            posts = fetch_func(**fetch_args)

            print(f"🔎 Number of posts fetched: {len(posts)}")

            for post_data in posts:
                formatted = format_post(post_data)
                post_to_blogger(
                    blog_id=BLOG_ID,
                    access_token=access_token,
                    title=formatted["title"],
                    content=formatted["content"],
                    labels=formatted["labels"],
                    category=formatted["category"]
                )

        except Exception as e:
            print(f"[ERROR] Failed category {category}: {e}")
