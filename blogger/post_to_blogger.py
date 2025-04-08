import requests
import datetime

def post_to_blogger(title, content, category, blog_id, access_token):
    post_data = {
        "title": title,
        "content": content,
        "labels": [category],
        "published": datetime.datetime.now().isoformat()
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/",
        headers=headers,
        json=post_data
    )

    if response.status_code == 200:
        print(f"Successfully posted: {title}")
    else:
        print(f"Failed to post: {title}, Error: {response.text}")
