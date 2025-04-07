from config import TODAY

def format_post(data):
    category = data.get("category", "misc")

    title = data.get("title", "Untitled")
    summary = data.get("summary", "")
    source = data.get("source", "#")
    year = data.get("year", "")
    topics = data.get("topics", [])
    authors = data.get("authors", [])
    date = data.get("date", TODAY)

    # HTML content 구성
    content = f"<h2>{title}</h2>\n"
    content += f"<p><b>📅 Date:</b> {date}</p>\n"

    if authors:
        content += f"<p><b>👥 Authors:</b> {', '.join(authors)}</p>\n"
    if year:
        content += f"<p><b>📅 Published:</b> {year}</p>\n"
    if topics:
        content += f"<p><b>📌 Topics:</b> {', '.join(topics)}</p>\n"

    content += f"<p>{summary}</p>\n"
    content += f"<p><a href='{source}' target='_blank'>🔗 Source</a></p>"

    return {
        "title": title,
        "content": content,
        "labels": generate_tags(data),
        "category": category
    }

def generate_tags(data):
    tags = set()
    for field in ["topics", "authors"]:
        items = data.get(field, [])
        tags.update(items)
    for keyword in ["inflation", "CPI", "GDP", "unemployment"]:
        if keyword.lower() in data.get("summary", "").lower():
            tags.add(keyword.upper())
    return list(tags)
