import requests
import json
import os

def post_to_blogger(blog_id, title, content):
    access_token = os.getenv("ACCESS_TOKEN")
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
        return True
    else:
        print(f"❌ Failed to post: {title}")
        print(f"📬 Status code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        return False
