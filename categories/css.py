import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_css_post():
    topics = [
        "CSS Box Model Explained in Simple Terms",
        "How to Use Flexbox for Layouts",
        "Mastering CSS Grid: Beginner to Intermediate",
        "Styling Forms Like a Pro",
        "Responsive Design with Media Queries",
        "How to Create Smooth Transitions and Hover Effects",
        "CSS Variables and Theming for Scalable Design",
        "Organizing CSS for Large Projects",
        "Understanding Specificity and the Cascade",
        "Using Pseudo-elements for Fancy Effects"
    ]

    selected_topic = random.choice(topics)

    prompt = f"""
You are a CSS instructor writing an informal but helpful tutorial blog post for self-taught web developers.
Topic: "{selected_topic}".
Use clean HTML only: <h2> for the title, <h3> for section headings, <p> for content paragraphs.
Include exactly one example using <pre><code class='language-css'>...</code></pre>.
Avoid Markdown. Do not use triple backticks.
Make the writing flow naturally, like a dev blog you'd see on Dev.to or Medium.
Vary sentence and paragraph length for more human-like rhythm.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You write CSS tutorials for frontend learners."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
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
            "tags": ["CSS", "Frontend", "Web Development", "Styling", "Tutorial"]
        }

    except Exception as e:
        return {
            "title": "CSS Post (Error)",
            "content": f"<p>⚠️ Failed to generate CSS post due to: {e}</p>",
            "category": "css",
            "tags": ["css", "error"]
        }
