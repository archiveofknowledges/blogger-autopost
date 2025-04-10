import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_javascript_post():
    topics = [
        "Understanding JavaScript Variables and Scope",
        "JavaScript Functions and Arrow Functions",
        "Event Handling in JavaScript",
        "DOM Manipulation Basics",
        "Working with Arrays and Objects",
        "Introduction to ES6 Features",
        "JavaScript Promises and Async/Await",
        "Form Validation with JavaScript",
        "Using Fetch API for HTTP Requests",
        "Best Practices in JavaScript Programming"
    ]

    selected_topic = random.choice(topics)

    prompt = f"""
You're a JavaScript instructor writing an engaging tutorial blog post on: "{selected_topic}".
Use only raw HTML formatting. Do NOT use Markdown or backticks.
Use <h2> for the title, <h3> for sections, and wrap all paragraphs in <p> tags.
Include one code example using <pre><code class='language-js'>...</code></pre>.
Make the tone friendly and informal — like explaining to a fellow developer.
Vary sentence and paragraph lengths for a human-like style.
Ensure this content can be posted directly on Blogger without modification.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You write JavaScript tutorials for beginner web developers."},
                {"role": "user", "content": prompt}
            ],
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
            "category": "javascript",
            "tags": ["JavaScript", "Frontend", "Web Development", "Async", "Tutorial"]
        }

    except Exception as e:
        return {
            "title": "JavaScript Post (Error)",
            "content": f"<p>⚠️ Failed to generate JavaScript post due to: {e}</p>",
            "category": "javascript",
            "tags": ["javascript", "error"]
        }
