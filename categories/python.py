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
        "Using External Libraries with pip"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are a Python instructor writing for learners who are new to programming. Topic: '{selected_topic}'. "
        "Write in a slightly casual tone that’s easy to follow, with paragraph length variation to feel more human. "
        "Use only HTML tags (not Markdown). Use <h2> for title, <h3> for sections, and <p> for explanations. "
        "Include a <pre><code class='language-python'>...</code></pre> code block for one clear example. "
        "Ensure the content is ready to be posted on Blogger without further formatting."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an experienced Python developer writing accessible tutorials for beginners."},
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
            "category": "python",
            "tags": ["Python", "Programming", "Tutorial", "Automation", "Development"]
        }

    except Exception as e:
        print(f"❌ Error generating python post: {e}")
        return None
