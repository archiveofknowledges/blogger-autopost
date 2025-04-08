import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_html_post():
    prompt = (
        "You are a helpful web development tutor. Write a detailed HTML tutorial blog post "
        "on a useful beginner topic. Format the post in HTML using <h2>, <h3>, and <p> tags. "
        "Also include a separate code block using <pre><code> with class 'language-html'. "
        "Output two fields: one for the main explanation text, and one only for the code block. "
        "Avoid using Markdown."
    )

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )

    full_content = response.choices[0].message.content.strip()

    # Split response into content and code block (rudimentary)
    if "<pre><code" in full_content:
        parts = full_content.split("<pre><code", 1)
        content = parts[0].strip()
        code_block = "<pre><code" + parts[1]
    else:
        content = full_content
        code_block = ""

    post = {
        "title": "Getting Started with HTML Forms",
        "content": content,
        "code": code_block,
        "category": "html",
        "tags": ["HTML", "Forms", "Beginner", "Web Development", "Tutorial"]
    }
    return post
