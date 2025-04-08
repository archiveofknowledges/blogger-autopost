import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_python_post():
    # ✅ 다양한 Python 주제 리스트
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
        "Using External Libraries with pip"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a Python instructor. Write a detailed tutorial blog post on the topic: '{selected_topic}'. "
        "Use only HTML tags. Do NOT use Markdown or triple backticks. "
        "Use <h2> for title, <h3> for section headings, and wrap all explanation text in <p> tags. "
        "Include one <pre><code class='language-python'>...</code></pre> code block for the example. "
        "Ensure the HTML is clean and can be posted directly to a Blogger post."
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
        "category": "python",
        "tags": ["Python", "Programming", "Tutorial", "Automation", "Development"]
    }
    return post
