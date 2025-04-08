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
        "Respond using only clean HTML formatting. DO NOT use any Markdown. DO NOT use triple backticks. "
        "Use <h2> for the main title, <h3> for section headings, and wrap all explanation text in <p> tags. "
        "Include one clearly separated code block using <pre><code class='language-html'>...</code></pre>. "
        "Ensure this output can be posted directly into a Blogger post and will render correctly."
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
