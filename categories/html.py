import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_html_post():
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

    prompt = f"""
You're an HTML tutor writing a helpful blog post about: "{selected_topic}".
Use only HTML — no Markdown, no backticks.
Structure it cleanly using <h2> for the title, <h3> for section headers, and <p> for each paragraph.
Include one example in a <pre><code class='language-html'>...</code></pre> block.
Write in a friendly, beginner-focused tone like Dev.to or MDN tutorials.
Vary paragraph length and sentence tone to sound more human-like.
Ensure the HTML can be posted directly to a Blogger post and will render well.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.75,
            max_tokens=1600
        )

        full_content = response.choices[0].message.content.strip()

        if "<pre><code" in full_content:
            parts = full_content.split("<pre><code", 1)
            content = parts[0].strip()
            code_block = "<pre><code" + parts[1]
        else:
            content = full_content
            code_block = ""

        return {
            "title": selected_topic,
            "content": content,
            "code": code_block,
            "category": "html",
            "tags": ["HTML", "Frontend", "Web Development", "Beginner", "Markup"]
        }

    except Exception as e:
        return {
            "title": "HTML Post (Error)",
            "content": f"<p>⚠️ Failed to generate HTML post due to: {e}</p>",
            "category": "html",
            "tags": ["html", "error"]
        }
