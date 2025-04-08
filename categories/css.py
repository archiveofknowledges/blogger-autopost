import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_css_post():
    # ✅ 다양한 CSS 주제 리스트
    topics = [
        "CSS Box Model Explained",
        "Flexbox Layout Tutorial",
        "Responsive Design with Media Queries",
        "CSS Grid: Building Modern Layouts",
        "Styling Forms with CSS",
        "Customizing Fonts and Typography",
        "Creating Transitions and Animations",
        "CSS Variables and Theming",
        "How to Use Pseudo-classes and Pseudo-elements",
        "Best Practices for CSS Organization"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a front-end development tutor. Write a detailed CSS tutorial blog post on the topic: '{selected_topic}'. "
        "Use only raw HTML, not Markdown. Avoid triple backticks. "
        "Structure the explanation using <h2>, <h3>, and <p> tags. Wrap any example code inside a <pre><code class='language-css'>...</code></pre> block. "
        "This post will be published on a Blogger blog. Ensure it's well-formatted and clean HTML only."
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
        "category": "css",
        "tags": ["CSS", "Web Development", "Frontend", "Tutorial", "Responsive Design"]
    }
    return post
