import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_nodejs_post():
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
        f"You are a Node.js instructor writing for backend developers learning Node. Topic: '{selected_topic}'. "
        "The tone should be natural and slightly conversational, with varying paragraph lengths. "
        "Use only HTML (no Markdown or backticks). Use <h2> for title, <h3> for sections, and <p> for text. "
        "Include a <pre><code class='language-js'>...</code></pre> block for the main code example. Keep it Blogger-compatible."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an experienced web backend engineer writing Node.js blog posts for learners."},
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
            "category": "nodejs",
            "tags": ["Node.js", "Backend", "JavaScript", "Web Development", "API"]
        }

    except Exception as e:
        print(f"❌ Error generating nodejs post: {e}")
        return None
