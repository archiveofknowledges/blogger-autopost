import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_html_post():
    topics = [
        "Creating a Basic HTML Page from Scratch",
        "HTML Headings and Semantic Structure",
        "Embedding Images and Videos with HTML",
        "Creating Tables and Lists in HTML5",
        "How to Build Contact Forms in HTML",
        "Anchor Tags and Internal Linking",
        "Using HTML5 Semantic Tags: article, section, aside",
        "Forms and Input Types Explained",
        "Best Practices for HTML Accessibility",
        "Structuring Content for SEO with HTML"
    ]

    selected_topic = random.choice(topics)

    prompt = f"""
You are an HTML instructor for beginner web developers. 
Write a friendly and clearly structured blog post on: "{selected_topic}".
Use casual but helpful tone, like Dev.to or personal Medium blog.
Use only clean HTML formatting: <h2> for main title, <h3> for sections, <p> for explanations.
Wrap example code with <pre><code class='language-html'>...</code></pre>.
No Markdown, no triple backticks. This will be used directly on a Blogger blog.
Make sure to vary sentence and paragraph length to sound human-written.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You write HTML tutorials for beginner-friendly blogs."},
                {"role": "user", "content": prompt}
            ],
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

        return {
            "title": selected_topic,
            "content": content,
            "code": code_block,
            "category": "html",
            "tags": ["HTML", "Web Development", "Frontend", "Tutorial", "HTML5"]
        }

    except Exception as e:
        return {
            "title": f"HTML Post (Error)",
            "content": f"<p>⚠️ Failed to generate HTML post due to: {e}</p>",
            "category": "html",
            "tags": ["html", "error"]
        }
