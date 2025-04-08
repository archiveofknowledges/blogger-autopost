import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_nodejs_post():
    # ✅ 다양한 Node.js 주제 리스트
    topics = [
        "Getting Started with Node.js",
        "Working with the File System Module",
        "Building a Simple HTTP Server",
        "Understanding Asynchronous JavaScript in Node.js",
        "Using Express.js for Routing",
        "Managing Packages with npm",
        "Handling JSON and APIs in Node.js",
        "Using Middleware in Express",
        "Creating RESTful APIs with Node.js",
        "Error Handling Best Practices"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a Node.js instructor. Write a detailed Node.js tutorial blog post on the topic: '{selected_topic}'. "
        "Use clean HTML formatting only. Do NOT use Markdown or triple backticks. "
        "Use <h2> for the main title, <h3> for section headings, and wrap all explanation text in <p> tags. "
        "Include one <pre><code class='language-js'>...</code></pre> code block for the example. "
        "Make sure the output is clean HTML suitable for Blogger posts."
    )

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
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

    post = {
        "title": selected_topic,
        "content": content,
        "code": code_block,
        "category": "nodejs",
        "tags": ["Node.js", "Backend", "JavaScript", "Web Development", "API"]
    }
    return post
