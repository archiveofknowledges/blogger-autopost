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
        "Error Handling Best Practices",
        "Deploying Node.js Apps to Heroku",
        "Common Node.js Performance Tips"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a Node.js developer writing a tutorial on the topic: '{selected_topic}'. "
        "Write in a practical, informal tone like you'd find in a real developer blog. "
        "Format only in HTML using <h2>, <h3>, <p> and one <pre><code class='language-js'>...</code></pre>. "
        "Avoid any use of Markdown or backticks. Output should be ready for Blogger."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=1600
        )

        content = response.choices[0].message.content.strip()

        if "<pre><code" in content:
            parts = content.split("<pre><code", 1)
            main = parts[0].strip()
            code = "<pre><code" + parts[1]
        else:
            main, code = content, ""

        return {
            "title": selected_topic,
            "content": main,
            "code": code,
            "category": "nodejs",
            "tags": ["Node.js", "Backend", "JavaScript", "Express", "Tutorial"]
        }

    except Exception as e:
        return {
            "title": "Node.js Post (Error)",
            "content": f"<p>⚠️ Failed to generate post due to: {e}</p>",
            "category": "nodejs",
            "tags": ["nodejs", "error"]
        }
