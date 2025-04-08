import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_html_post():
    prompt = (
        "You are a helpful web development tutor. Write a detailed HTML tutorial blog post "
        "on a useful beginner topic. Format the post in HTML using <h2>, <h3>, and <p> tags. "
        "Also include a separate <pre><code> block with a code example that readers can copy easily. "
        "Do not use Markdown. Use clean formatting that can be posted directly to a blog."
    )

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )

    content = response.choices[0].message.content.strip()

    post = {
        "title": "Getting Started with HTML Forms",
        "content": content,
        "category": "html",
        "tags": ["HTML", "Forms", "Beginner", "Web Development", "Tutorial"]
    }
    return post
