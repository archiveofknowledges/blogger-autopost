from datetime import datetime

BLOG_ID = "archiveofknowledges"

POST_SETTINGS = {
    "scholar": {
        "enabled": True,
        "count": 3,
        "keywords": ["transformer"]
    },
    "economy": {
        "enabled": True,
        "count": 1,
        "countries": ["United States"]
    }
}

TODAY = datetime.today().strftime("%Y-%m-%d")
