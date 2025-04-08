import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_html_post():
    # ✅ 다양한 HTML 주제 리스트
    topics = [
        "Creating a Basic HTML Document",
        "Understanding HTML Headings and Paragraphs",
        "Working with Images in HTML",
        "Creating Lists and Tables in HTML",
        "Building Forms with Input Fields",
        "Using Links and Anchor Tags",
        "Understanding HTML Semantics",
        "Embedding Videos and Media",
        "Structuring Web Pages with HTML5 Elements",
        "Best Practices for Accessible HTML"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a helpful web development tutor. Write a detailed HTML tutorial blog post on the topic: '{selected_topic}'. "
        "Respond using only raw HTML, not Markdown. Use <h2> for title, <h3> for section headings, and wrap each paragraph in <p> tags. "
        "Include a single <pre><code class='language-html'>...</code></pre> code block separately. Do not use triple backticks. "
        "This output should be usable directly in a Blogger HTML post."
    )

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )

    full_content = response.choices[0].message.content.strip()

    if "<pre><code" in full_content:
        parts = full_content.split("<pre><code", 1)
        content = parts[0].strip()
        code_block = "<pre><code" + parts[1]
    else:
        content = full_content
        code_block = ""

    post = {
        "title": selected_topic,
        "content": content,
        "code": code_block,
        "category": "html",
        "tags": ["HTML", "Web Development", "Tutorial", "Beginner", "Frontend"]
    }
    return post
