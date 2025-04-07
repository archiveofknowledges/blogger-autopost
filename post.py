import os
import importlib
from datetime import datetime
import pytz

from config import POST_SETTINGS, BLOG_ID, CATEGORIES, OPENAI_MODEL
from formatter import format_post
from blogger import post_to_blogger

print("🚀 Starting auto-posting...")

# 시간 확인
tz = pytz.timezone(POST_SETTINGS["TIMEZONE"])
now = datetime.now(tz)
print(f"🕒 Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 카테고리별 자동 포스팅 처리
for category, options in CATEGORIES.items():
    if not isinstance(options, dict) or not options.get("enabled", True):
        continue

    print(f"\n📚 Fetching posts from category: {category}")
    fetch_args = {k: v for k, v in options.items() if k != "enabled"}
    print(f"📄 Fetch args: {fetch_args}")

    try:
        collector = importlib.import_module(f"categories.{category}")
        raw_posts = collector.fetch_posts(**fetch_args)
    except Exception as e:
        print(f"❌ Failed to fetch posts for {category}: {e}")
        continue

    print(f"🔎 Number of posts fetched: {len(raw_posts)}")

    for post in raw_posts:
        title = post.get("title", "Untitled")
        summary = post.get("summary", "")
        body = post.get("body", post.get("summary", ""))
        source = post.get("source", "")
        topics = post.get("topics", [])

        try:
            formatted_content = format_post(title, summary, body, source, topics)
            success = post_to_blogger(BLOG_ID, title, formatted_content)
            if success:
                print(f"✅ Posted: {title}")
            else:
                print(f"❌ Failed to post: {title}")
        except Exception as e:
            print(f"❌ Error posting {title}: {e}")
