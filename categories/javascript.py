import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_javascript_post():
    # ✅ 다양한 JavaScript 주제 리스트
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

    prompt = (
        f"You are a JavaScript instructor. Write a detailed JavaScript tutorial blog post on the topic: '{selected_topic}'. "
        "Respond using only HTML tags. Do NOT use Markdown or triple backticks. "
        "Use <h2> for title, <h3> for section headings, and wrap all explanation text in <p> tags. "
        "Include a single example using <pre><code class='language-js'>...</code></pre> block. "
        "Make sure the HTML is clean and can be published directly on a Blogger post."
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
        "category": "javascript",
        "tags": ["JavaScript", "Web Development", "Frontend", "Tutorial", "Coding"]
    }
    return post
