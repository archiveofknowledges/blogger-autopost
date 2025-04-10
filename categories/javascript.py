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

    prompt = (
        f"You are a friendly and humorous JavaScript instructor writing a casual, helpful blog post on the topic: '{selected_topic}'. "
        "Use only clean HTML (no Markdown or backticks). Structure with <h2> for the main title, <h3> for sections, and <p> for body text. "
        "Include one example using <pre><code class='language-js'>...</code></pre>. Your tone should feel like a smart but funny developer on Stack Overflow explaining things in plain English."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a witty JavaScript tutor writing HTML-formatted tutorials for a tech-savvy but casual audience."},
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
            "category": "javascript",
            "tags": ["javascript", "web development", "frontend", "tutorial", "coding"]
        }

    except Exception as e:
        print(f"❌ Error generating javascript post: {e}")
        return None
