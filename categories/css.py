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
        f"Write a casual, human-like blog post in HTML format explaining the topic '{selected_topic}' to beginner web developers. "
        "Structure it with <h2>, <h3>, and <p> tags. Include a mix of sentence lengths and tones. Add rhetorical questions if needed. "
        "Avoid markdown and triple backticks. Use <pre><code class='language-css'>...</code></pre> for code examples."
    )

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You're a CSS instructor writing fun and practical HTML tutorials for a blog."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
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
        "category": "css",
        "tags": ["css", "web design", "frontend", "responsive", "tutorial"]
    }
