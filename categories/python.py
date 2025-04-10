import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_python_post():
    topics = [
        "Introduction to Python Variables and Data Types",
        "Using Conditional Statements in Python",
        "Loops in Python: for and while",
        "Working with Lists and Dictionaries",
        "Functions and Arguments in Python",
        "Reading and Writing Files in Python",
        "Error Handling with try/except",
        "Python List Comprehensions Explained",
        "Object-Oriented Programming Basics",
        "Using External Libraries with pip",
        "Writing a Simple Web Scraper",
        "Making a CLI Tool with argparse"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a Python educator writing a casual, insightful blog post on: '{selected_topic}'. "
        "Structure the post in HTML: use <h2> for title, <h3> for section headers, and <p> for body text. "
        "Include one illustrative example using <pre><code class='language-python'>...</code></pre>. "
        "Keep the tone accessible and friendly, like a Medium tutorial. Avoid any Markdown or backticks."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.75,
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
            "category": "python",
            "tags": ["Python", "Programming", "Coding", "Development", "Tutorial"]
        }

    except Exception as e:
        return {
            "title": "Python Post (Error)",
            "content": f"<p>⚠️ Error generating Python post: {e}</p>",
            "category": "python",
            "tags": ["python", "error"]
        }
