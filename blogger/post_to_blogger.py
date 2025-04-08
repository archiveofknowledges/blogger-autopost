import requests
import json

def post_to_blogger(title, content, category, blogger_api_key, blog_id):
    """
    Blogger API를 통해 포스트를 업로드하는 함수
    """
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    headers = {
        "Authorization": f"Bearer {blogger_api_key}",
        "Content-Type": "application/json"
    }
    
    post_data = {
        "title": title,
        "content": content,
        "labels": [category],
        "status": "live"
    }
    
    response = requests.post(url, headers=headers, json=post_data)
    
    if response.status_code == 200:
        print(f"Successfully posted: {title}")
    else:
        print(f"Failed to post: {title}, Error: {response.text}")
